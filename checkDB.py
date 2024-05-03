import sqlite3
import json
import re
from config import DBCommands
import requests
from car_page_parser import parse_car_page
from config import WEB_HEADERS
from tqdm import tqdm
import time

def string_to_dict(input_string):
    # Удаление начальной части строки до фигурной скобки (если есть)
    dict_str = re.search(r"\{.*\}", input_string).group(0)

    # Парсинг строки в словарь с помощью безопасного метода eval
    # Создаем безопасный словарь окружения для eval
    safe_dict = {}
    try:
        # Используем eval с локальным и безопасным глобальным окружением
        # для преобразования строки словаря в реальный словарь Python
        vehicle_details = eval(dict_str, {"__builtins__": None}, safe_dict)
    except NameError:
        # В случае ошибки, например, если в строке есть непредвиденные символы
        print("Error parsing the string into a dictionary.")
        return {}

    return vehicle_details

def get_all_cars(SELECT_COMMAND):
    DB_NAME = "master_database.db"
    data = []

    print(DB_NAME)
    try:
        """Выводит все данные об автомобилях из базы данных."""
        conn = sqlite3.connect(DB_NAME)
    except Exception:
        print("Connect failed")
        return data
    c = conn.cursor()

    # Получаем информацию о столбцах таблицы cars
    c.execute("PRAGMA table_info(cars)")
    columns = c.fetchall()
    column_names = [column[1] for column in columns]
    print(column_names)

    try:
        c.execute(SELECT_COMMAND)
    except Exception:
        print(f"{SELECT_COMMAND} failed")

    cars = c.fetchall()
    if cars:
        for i, car in enumerate(cars):
            url, city, price, details, time = car
            details_dict = json.loads(details)
            data.append({"URL": url, "Город": city, "Цена": price, "Дата": time, "Детали": details_dict})

    conn.close()
    return data

if __name__ == "__main__":
    SELECT_COMMAND = DBCommands.select_in_sold_cars
    cars = get_all_cars(SELECT_COMMAND)

    DB_NAME = "master_database.db"
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    session = requests.Session()
    error = []
    car_i = 0
    with tqdm(total=len(cars)) as pbar:
        while car_i < len(cars):
            car = cars[car_i]
            try:
                car_details = parse_car_page(car["URL"], session, WEB_HEADERS)
            except Exception as e:
                print(e)
                continue
            car_i += 1


            if(len(list(car_details)) != 0):
                details_str = json.dumps(car['Детали'])
                error.append([car["URL"], details_str])

                # Вставка удаленной записи в таблицу cars
                try:
                    c.execute("INSERT INTO cars (url, city, price, details) VALUES (?, ?, ?, ?)",
                          (car["URL"], car["Город"], car["Цена"], details_str))
                except sqlite3.IntegrityError as e:
                    print(f"Пропущена запись для URL {car['URL']} из-за ошибки целостности: {e}")

                # Удаление записи из таблицы sold_cars
                c.execute("DELETE FROM sold_cars WHERE url = ?", (car["URL"],))

                # Если используется транзакция, не забудьте фиксировать изменения
                conn.commit()
            pbar.update(1)

    print(len(error))
    with open("errors.txt", "w") as f:
        for url in error:
            f.write(str(url) + "\n")