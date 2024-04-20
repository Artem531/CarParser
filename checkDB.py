import sqlite3
import json
import re
from config import DBCommands

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
    SELECT_COMMAND = DBCommands.select_in_cars

    print(get_all_cars(SELECT_COMMAND))
