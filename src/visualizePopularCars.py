import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from config import DBCommands
from checkDB import get_all_cars
from utils import getPriceFromDB

def fetch_data(command):
    """
    Получает данные из базы данных.
    """
    data = get_all_cars(command)
    return data

import seaborn as sns

def prepare_data(data, status):
    """
    Подготавливает данные, преобразуя даты и цены в формат, подходящий для анализа.
    """
    models = []
    marks = []

    for item in data:
        #if item["Детали"]["Marka"] != "BMW":
        #    continue

        price = getPriceFromDB(item['Цена'])
        if price == None:
            continue

        if price < 1000:
            continue


        mark = item["Детали"]["Marka"]
        model = "-"
        if "Детали" in item and "Model" in item["Детали"]:
            model = item["Детали"]["Model"]


        marks.append(mark)
        models.append(model)

    df = pd.DataFrame({'Mark': marks, 'Model': models})
    return df


def main():
    """
    Основная функция для выполнения всех операций.
    """
    plt.figure(figsize=(32, 16))

    # Для автомобилей в продаже
    command = DBCommands.select_in_cars
    data = fetch_data(command)
    df_in_cars = prepare_data(data, 'В продаже')

    top_cars = df_in_cars.groupby(['Mark', 'Model']).size().sort_values(ascending=False).head(10)
    top_cars_list = [(mark, model, count) for (mark, model), count in top_cars.items()]

    return top_cars_list

if __name__ == "__main__":
    main()
