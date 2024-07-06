import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
from config import DBCommands
from checkDB import get_all_cars
from utils import getPriceFromDB, normalizeString
from config import Commands, TIME_DELTA

def fetch_data(command):
    """
    Получает данные из базы данных.
    """
    data = get_all_cars(command)
    return data

import seaborn as sns

def prepare_data(data, status, region_of_interest, group_by_month, price_thresh):
    """
    Подготавливает данные, преобразуя даты и цены в формат, подходящий для анализа.
    """
    dates = []
    prices = []

    for item in data:
        details_fields = ["Marka", "Цена"]
        missing_details_fields = [field for field in details_fields if field not in item['Детали']]

        if missing_details_fields:
            print(f"Missing fields: {missing_details_fields}")
            print(item)
            continue

        if normalizeString(item["Детали"]["Marka"]) != normalizeString(region_of_interest):
            continue

        date_str = item['Дата']
        price = getPriceFromDB(item['Цена'])
        if price == None:
            continue

        date = datetime.strptime(date_str.split()[0], '%Y-%m-%d')
        # Проверяем, если дата обновления меньше, чем текущая дата минус TIME_DELTA дня,
        # то пропускаем эту запись
        if date > datetime.now() - timedelta(days=TIME_DELTA):
            continue

        if price < price_thresh:
            continue

        if group_by_month:
            date = date.replace(day=1)

        dates.append(date)
        prices.append(price)

    df = pd.DataFrame({'Date': dates, 'Price': prices, 'Status': status})
    return df


def main(region_of_interest, group_by_month, price_thresh):
    """
    Основная функция для выполнения всех операций.
    """
    plt.figure(figsize=(32, 16))

    # Для автомобилей в продаже
    command = DBCommands.select_in_cars
    data = fetch_data(command)
    df_in_cars = prepare_data(data, 'В продаже', region_of_interest, group_by_month, price_thresh)

    # Для проданных автомобилей
    command = DBCommands.select_in_sold_cars
    data = fetch_data(command)
    df_in_sold_cars = prepare_data(data, 'Продано', region_of_interest, group_by_month, price_thresh)

    # Объединяем данные
    df = pd.concat([df_in_cars, df_in_sold_cars])
    print(len(df))

    # Используем Seaborn для построения бокс-плотов с разделением по статусу
    sns.boxplot(x='Date', y='Price', hue='Status', data=df, showfliers=False)

    plt.title('Средняя цена по дням')
    plt.xlabel('Дата')
    plt.ylabel('Средняя цена (€)')
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.legend()  # Добавляем легенду для различия наборов данных

    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.gca().yaxis.set_major_locator(plt.MultipleLocator(1000))  # Устанавливаем деления каждые 1000

    # Объединяем данные

    plt.tight_layout()
    plt.savefig(f"{Commands.get_price_range_models}.jpg", dpi=100)


if __name__ == "__main__":
    main("BMW", False, 10000)
