from bs4 import BeautifulSoup
from car_page_parser import parse_car_page
import requests
import sqlite3
import json
import hashlib
from config import DBTableName, BASE_URL, WEB_HEADERS, DBCommands, get_params, TEST_BRAND
import time
import threading
from tqdm import tqdm

def generate_db_name(params):
    params_str = params["brand"]

    hash_object = hashlib.md5(params_str.encode())
    return f"cars_{hash_object.hexdigest()}.db"

def getPrice(car):
    price_block = car.find('div', class_='price')

    # Пытаемся найти цену со скидкой
    discount_price = price_block.find('span', class_='priceDiscount')

    # Если есть цена со скидкой, используем её, иначе ищем обычную цену
    if discount_price:
        price = discount_price.get_text(strip=True)
    else:
        # Если есть старая цена, используем её как резервный вариант
        old_price = price_block.find('span', class_='oldPrice')
        if old_price:
            price = old_price.get_text(strip=True)
        else:
            # Попытка извлечь любую другую цену, если структура сложнее
            price = price_block.get_text(strip=True)
    return price

def create_database(DB_NAME):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute(DBCommands.create_cars_DB)

    conn.commit()
    conn.close()

def reset_session_status(DB_NAME):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(DBCommands.update_session_in_cars)
    conn.commit()
    conn.close()

def check_car_in_db(url, DB_NAME):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Создаем строку SQL запроса для обновления поля session_updated
    query_update = "UPDATE cars SET session_updated=1 WHERE url=?"

    # Выполняем запрос для обновления session_updated
    c.execute(query_update, (url,))

    # Проверяем сколько строк было обновлено
    if c.rowcount > 0:
        print("Машина уже есть в базе данных и поле session_updated успешно обновлено.")
        # Коммитим изменения в базе данных
        conn.commit()
        conn.close()
        return True
    else:
        print("Машины в базе данных нет.")
        conn.close()
        return False

def save_car_to_db(car_data, DB_NAME):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    details_str = json.dumps(car_data['details'])
    c.execute(DBCommands.insert_in_cars,
              (car_data['url'], car_data['city'], car_data['price'], details_str))

    c.execute(DBCommands.update_data_in_cars,
              (car_data['city'], car_data['price'], details_str, car_data['url']))

    conn.commit()
    conn.close()
    print(f"Обработана машина: {car_data['url']}")

class TimeoutException(Exception):
    pass

def run_with_timeout(func, timeout_seconds):
    result = [None]
    exception = [None]

    def target():
        try:
            result[0] = func()
        except Exception as e:
            exception[0] = e

    thread = threading.Thread(target=target)
    thread.start()
    thread.join(timeout_seconds)

    if thread.is_alive():
        raise TimeoutException("Функция заняла слишком много времени")
    if exception[0] is not None:
        raise exception[0]

    return result[0]

def parse_data(params):
    DB_NAME = "master_database.db"
    page = 1  # Начальная страница
    cars_found = True  # Флаг для проверки, нашлись ли автомобили на странице
    cur_car_num = 1
    new_car_num = 1

    create_database(DB_NAME)
    reset_session_status(DB_NAME)

    session = requests.Session()
    while cars_found:
        try:
            if new_car_num % 250 == 0: # Сайт ограничивает число запросов.
                print("wait to calm down the server")
                time.sleep(5)

            print(f"Обрабатываем страницу {page}...")
            params['page'] = str(page)  # Установка текущей страницы в параметрах запроса

            get_with_timeout = lambda: requests.get(BASE_URL, headers=WEB_HEADERS, params=params)
            response = run_with_timeout(get_with_timeout, 5)

            #response = requests.get(BASE_URL, headers=WEB_HEADERS, params=params)
            html = response.text

            # Парсинг страницы
            soup = BeautifulSoup(html, 'html.parser')
            all_cars_num = soup.find_all("div", class_="table")[0].find("small").get_text(strip=True).split(" ")[-1]

            # Поиск элементов с информацией об автомобилях
            cars = soup.find_all('article', class_='classified')

            if not cars:  # Если автомобили не найдены, прекращаем обработку
                cars_found = False
                print("Достигнут конец списка объявлений.")
                break

            # Если автомобили найдены, обработка каждого из них
            tmp_i = 0
            with tqdm(total=len(cars)) as pbar:
                while tmp_i < len(cars):
                    car = cars[tmp_i]
                    try:
                        title_element = car.find('a', class_='ga-title')
                        if title_element:
                            cur_car_num += 1
                            price = getPrice(car)
                            car_url = 'https://www.polovniautomobili.com' + title_element['href']
                            car_url = car_url.split("?")[0]
                            print(car_url)
                            if check_car_in_db(car_url, DB_NAME):
                                print("Машина уже была обработана ранее")
                                tmp_i += 1
                                continue

                            new_car_num += 1
                            car_details = parse_car_page(car_url, session, WEB_HEADERS)

                            city = car.find("div", class_="city").get_text(strip=True)

                            # Вывод или обработка информации
                            print(f"{cur_car_num}/{all_cars_num}: URL: {car_url}, Город: {city}, Цена: {price}, Детали: {car_details}")
                            save_car_to_db({
                                'url': car_url,
                                'city': city,
                                'price': price,
                                'details': car_details
                            }, DB_NAME)
                            print('________________________________')
                        else:
                            print('no title_element')
                            print('________________________________')
                    except:
                        print(error)
                        print("wait to calm down the server after error")
                        time.sleep(5)
                        continue
                    tmp_i += 1
                    pbar.update(1)

        except Exception as error:
            print(error)
            print("wait to calm down the server after error")
            time.sleep(5)
            continue
                #break
            #break
        page += 1  # Переход к следующей странице
    return DB_NAME, cur_car_num

def print_potentially_sold_cars(DB_NAME):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(f"{DBCommands.select_in_cars} WHERE session_updated = 0")

    for car in c.fetchall():
        print(f"Потенциально продана: {car[0]}, Город:{car[1]}, Цена: {car[2]}, Детали: {json.loads(car[3])}")

    conn.close()

def filter_selling_cars_from_sold_cars(DB_NAME):
    """Удаляет проданные автомобили из таблицы sold_cars, которые есть в таблице cars."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    try:
        # Выбираем проданные автомобили из таблицы sold_cars
        c.execute(f"SELECT url FROM {DBTableName.sold_cars_table_name}")
        sold_cars_urls = [row[0] for row in c.fetchall()]

        not_sold_cars = 0
        # Проверяем наличие этих машин в таблице cars и удаляем их из sold_cars
        for url in sold_cars_urls:
            c.execute(f"SELECT url FROM {DBTableName.cars_table_name} WHERE url = ?", (url,))
            result = c.fetchone()
            if result:
                not_sold_cars += 1
                c.execute(f"DELETE FROM {DBTableName.sold_cars_table_name} WHERE url = ?", (url,))

        print(f"Удалено не проданных автомобилей из таблицы sold_cars: {not_sold_cars}")
    except Exception as e:
        print("Произошла ошибка при удалении проданных автомобилей из таблицы sold_cars:", e)

    # Фиксируем изменения и закрываем соединение
    conn.commit()
    conn.close()

def save_sold_cars_to_separate_table(DB_NAME):
    """Перемещает потенциально проданные автомобили в отдельную таблицу с предварительной очисткой."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Создаем новую таблицу для проданных автомобилей, если она не существует
    c.execute(DBCommands.create_sold_cars_DB)

    # Выбираем автомобили, которые не были обновлены в текущей сессии
    c.execute(f"{DBCommands.select_in_cars} WHERE session_updated = 0")
    sold_cars = c.fetchall()

    session = requests.Session()
    car_i = 0
    actually_sold_cars = []
    print("Проверяем проданные машины")
    with tqdm(total=len(sold_cars)) as pbar:
        while car_i < len(sold_cars):
            car = sold_cars[car_i]
            try:
                car_details = parse_car_page(car[0], session, WEB_HEADERS)
            except Exception as e:
                print(e)
                continue
            car_i += 1

            if(len(list(car_details)) == 0):
                actually_sold_cars.append(car)

            pbar.update(1)

    # Перемещаем эти автомобили в таблицу sold_cars
    print("Перемещаем эти автомобили в таблицу sold_cars")
    for car in tqdm(actually_sold_cars):
        url, city, price, details, _ = car
        try:
            c.execute(DBCommands.insert_in_sold_cars, (url, city, price, details))
        except sqlite3.IntegrityError as e:
            print(f"Пропущена запись для URL {url} из-за ошибки целостности: {e}")
            # Получаем содержимое конфликтующей строки
            conflicting_row = c.execute("SELECT * FROM sold_cars WHERE url = ?", (url,)).fetchone()
            print("Содержимое конфликтующей строки (уже в базе):", conflicting_row)
            print("Содержимое конфликтующей строки (пытаемся добавить):", car)

    print(f"Таблица проданных автомобилей обновлена. Новых записей: {len(actually_sold_cars)}")

    # Удаляем потенциально проданные автомобили из основной таблицы
    for car in actually_sold_cars:
        c.execute(f"DELETE FROM {DBTableName.cars_table_name} WHERE url = ?", (car[0],))

    print(f"Удалено потенциально проданных автомобилей: {actually_sold_cars}")

    # Фиксируем изменения и закрываем соединение
    conn.commit()
    conn.close()

if __name__ == "__main__":
    params = get_params(TEST_BRAND)

    DB_NAME, _ = parse_data(params=params)
    #DB_NAME = "master_database.db"

    print_potentially_sold_cars(DB_NAME)
    save_sold_cars_to_separate_table(DB_NAME)