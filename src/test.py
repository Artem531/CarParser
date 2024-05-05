import sqlite3
from config import DBCommands

DB_NAME = "master_database.db"
conn = sqlite3.connect(DB_NAME)
c = conn.cursor()

# Создаем новую таблицу для проданных автомобилей, если она не существует
c.execute(DBCommands.create_sold_cars_DB)

# Выбираем автомобили, которые не были обновлены в текущей сессии
c.execute(f'{DBCommands.select_in_cars} WHERE url = "https://www.polovniautomobili.com/auto-oglasi/23743552/zastava-101-skala-55"')
sold_cars = c.fetchall()
print(sold_cars)
