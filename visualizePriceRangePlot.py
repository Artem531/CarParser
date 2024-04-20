import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from config import DBCommands
from checkDB import get_all_cars
from utils import getPriceFromDB, normalizeString
from config import Commands

def fetch_data(command):
    """
    Получает данные из базы данных.
    """
    data = get_all_cars(command)
    return data

import seaborn as sns

def prepare_data(data, status, region_of_interest):
    """
    Подготавливает данные, преобразуя даты и цены в формат, подходящий для анализа.
    """
    dates = []
    prices = []

    for item in data:
        if normalizeString(item["Детали"]["Marka"]) != normalizeString(region_of_interest):
            continue

        date_str = item['Дата']
        price = getPriceFromDB(item['Цена'])
        if price == None:
            continue

        if price < 1000:
            continue
        date = datetime.strptime(date_str.split()[0], '%Y-%m-%d')

        dates.append(date)
        prices.append(price)

    df = pd.DataFrame({'Date': dates, 'Price': prices, 'Status': status})
    return df


def main(region_of_interest):
    """
    Основная функция для выполнения всех операций.
    """
    plt.figure(figsize=(32, 16))

    # Для автомобилей в продаже
    command = DBCommands.select_in_cars
    data = fetch_data(command)
    df_in_cars = prepare_data(data, 'В продаже', region_of_interest)

    # Для проданных автомобилей
    command = DBCommands.select_in_sold_cars
    data = fetch_data(command)
    df_in_sold_cars = prepare_data(data, 'Продано', region_of_interest)

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
    main("BMW")
