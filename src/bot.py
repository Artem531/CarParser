import schedule
import time
import threading
import os
import sys
from datetime import datetime, timedelta

from handlers import start_polling
from main import (parse_data,
                  save_sold_cars_to_separate_table,
                  filter_selling_cars_from_sold_cars)

from config import get_params

def scheduled_fetch():
    print("Выполняю запланированную задачу...")
    params = get_params(brand="")
    DB_NAME, _ = parse_data(params)

    save_sold_cars_to_separate_table(DB_NAME)
    filter_selling_cars_from_sold_cars(DB_NAME)


# Функция для перезапуска приложения
def restart_program():
    print("Перезапуск программы...")
    os.execv(sys.executable, ['python'] + sys.argv)

# Настройка расписания
schedule.every().day.at("00:00").do(scheduled_fetch)

# Установка времени для перезапуска (например, каждые 1 дней)
restart_time = datetime.now() + timedelta(days=1)

# Функция для обработки запланированных задач в отдельном потоке
def start_scheduled_tasks():
    global restart_time
    while True:
        schedule.run_pending()
        if datetime.now() >= restart_time:
            restart_program()
        time.sleep(1)

# Запуск polling в отдельном потоке
threading.Thread(target=start_polling).start()

# Запуск выполнения запланированных задач в отдельном потоке
threading.Thread(target=start_scheduled_tasks).start()