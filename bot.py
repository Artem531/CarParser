import schedule
import time
import threading

from handlers import start_polling
from main import (parse_data,
                  save_sold_cars_to_separate_table)

from config import get_car_brands, get_params

def scheduled_fetch():
    print("Выполняю запланированную задачу...")
    params = get_params(brand="")
    DB_NAME, _ = parse_data(params)
    save_sold_cars_to_separate_table(DB_NAME)


# Настройка расписания
schedule.every().day.at("00:00").do(scheduled_fetch)
#scheduled_fetch()

# Функция для обработки запланированных задач в отдельном потоке
def start_scheduled_tasks():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Запуск polling в отдельном потоке
threading.Thread(target=start_polling).start()

# Запуск выполнения запланированных задач в отдельном потоке
threading.Thread(target=start_scheduled_tasks).start()