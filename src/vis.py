import pandas as pd
import matplotlib.pyplot as plt
import random
import matplotlib.patheffects as PathEffects
import matplotlib.lines as mlines
from utils import normalizeString
import re
import numpy as np
from tqdm import tqdm

maxValuesNum = 10

def generate_raw_data(num_of_cars):
    return {
        'Цена': [random.randint(5000, 20000) for _ in range(num_of_cars)],
        'Город': [random.choice(['Москва', 'Санкт-Петербург', 'Новосибирск', 'Екатеринбург', 'Казань']) for _ in range(num_of_cars)],
        'Марка': [random.choice(['Toyota', 'Ford', 'Mercedes', 'BMW', 'Audi', 'Volkswagen', 'Hyundai', 'Kia']) for _ in range(num_of_cars)],
        'Модель': [random.choice(['Camry', 'Focus', 'C-Class', '3 Series', 'A4', 'Golf', 'Tucson', 'Sportage']) for _ in range(num_of_cars)],
        'Вид топлива': [random.choice(['бензин', 'дизель', 'электро', 'гибрид']) for _ in range(num_of_cars)],
        'Пробег': [random.randint(0, 300000) for _ in range(num_of_cars)],
        'Коробка передач': [random.choice(['автомат', 'механика']) for _ in range(num_of_cars)]
    }


def round_to_nearest(number, step):
    return round(number / step) * step

def filter_data(raw_data, raw_cars_status, region_of_interest, num_stat_category):
    data = {key: [] for key in raw_data.keys()}
    cars_status = []

    # Нормализуем значения по которым будем делать фильтрацию
    print("Нормализую данные")
    for category in region_of_interest.keys():
        if category in num_stat_category:
            continue
        else:
            values = region_of_interest[category]
            for i in tqdm(range(len(values))):
                values[i] = normalizeString(values[i])

    # Делаем фильтрацию
    print("Фильтрую данные")
    for i in tqdm(range(len(raw_data['Цена']))):
        if criteria_check(raw_data, region_of_interest, num_stat_category, i):
            continue
        for category in raw_data:
            append_filtered_data(data, raw_data, category, i)
        cars_status.append(raw_cars_status[i])
    return data, cars_status

def criteria_check(raw_data, region_of_interest, num_stat_category, i):
    for category in raw_data:
        if category in region_of_interest:
            if category in num_stat_category:
                bounders = region_of_interest[category].split("-")
                if not (int(bounders[0]) < raw_data[category][i] < int(bounders[1])):
                    return True
            else:
                if normalizeString(raw_data[category][i]) not in region_of_interest[category]:
                    return True
    return False

def append_filtered_data(data, raw_data, category, i):
    if category in ["Цена", "Пробег"]:
        discrete_value = round_to_nearest(raw_data[category][i], 5000 if category == "Цена" else 100000)
        if discrete_value == 115000:
            print(discrete_value, i, raw_data[category][i], category)
        data[category].append(discrete_value)
    else:
        data[category].append(raw_data[category][i])

def calculate_statistics(data, cars_status):
    statistics = {category: {car_status: {} for car_status in [True, False]} for category in data.keys()}
    for category in data:
        for i, value in enumerate(data[category]):
            car_status = cars_status[i]
            current_count = statistics[category][car_status].get(value, 0)
            statistics[category][car_status][value] = current_count + 1
    return statistics

def normalize_value(value, min_value, max_value, scale=10000):
    if max_value - min_value != 0:
        return (value - min_value) / (max_value - min_value) * scale
    else:
        if max_value == 0:
            max_value = 1
        return value / max_value * scale


def prepare_value_tables(data):
    value_tables = {}
    scale = 1000
    global maxValuesNum
    maxValuesNum = max([len(values) for category, values in data.items()])
    for category, values in data.items():
        if all(isinstance(value, (int, float)) for value in values):
            sorted_values = np.sort(values)

            cur_value_table = {}
            unique_index = 0
            for value in sorted_values:
                if value in cur_value_table:
                    continue
                cur_value_table[value] = 20 * maxValuesNum + unique_index * 100
                unique_index += 1
            value_tables[category] = cur_value_table
        else:
            set_values = set(values)
            value_tables[category] = {value: 20 * maxValuesNum + index * 80 for index, value in enumerate(set_values)}
    return value_tables

def check_and_annotate(x, y, text, sold, text_properties, drawn_annotations):
    annotation_key = (x, y, text, sold)
    if annotation_key not in drawn_annotations:
        plt.text(x, y, text, **text_properties)
        drawn_annotations.add(annotation_key)

# Функция для проверки и добавления отрезка в набор
def check_and_draw(x1, y1, x2, y2, drawn_segments, color='g', marker='o', linestyle='-'):
    segment = ((x1, y1), (x2, y2)) if (x1, y1) < (x2, y2) else ((x2, y2), (x1, y1))
    if segment not in drawn_segments:
        plt.plot([x1, x2], [y1, y2], color=color,  marker=marker, linestyle=linestyle)  # Отрисовка отрезка
        drawn_segments.add(segment)

def draw_general_data(data, cars_status, value_tables, statistics, res_image_path="res.jpg"):
    drawn_annotations = set()  # Множество для отслеживания аннотаций
    drawn_segments = set()  # Для отслеживания уже нарисованных отрезков
    df_data = pd.DataFrame(data)

    # Подготовка данных перед циклом
    headers = list(data.keys())  # Заголовки для упрощения доступа
    x_values = range(len(headers))  # x координаты одинаковы для всех линий
    x_values = np.array(x_values) * 2

    text_effect = [PathEffects.withStroke(linewidth=3, foreground="black")]

    annotations = [
        headers,
        headers
    ]
    offset_y = 0.036

    plt.figure(figsize=(32, 64))
    # Настройка и отрисовка данных
    with tqdm(total=len(df_data)) as pbar:
        for index, row in df_data.iterrows():
            y_values = [value_tables[header][row[header]] for header in data.keys()]
            sold = cars_status[index]
            color = 'g' if not sold else 'r'

            # Прорисовка отрезков линии, если они еще не были нарисованы
            for i in range(len(y_values) - 1):
                check_and_draw(x_values[i], y_values[i], x_values[i + 1], y_values[i + 1], drawn_segments, color='grey')

            # Отрисовка аннотаций, если они ещё не были нарисованы
            for i, (x, y) in enumerate(zip(x_values, y_values)):
                basic_text = row[annotations[0][i]]  # Базовая аннотация
                stat_text = statistics[annotations[1][i]][sold][row[annotations[1][i]]]  # Статистика

                # Параметры отображения текста
                stat_size = 44
                text_properties_basic = {'fontsize': 30, 'ha': 'right', 'va': 'bottom'}
                text_properties_stat = {'fontsize': stat_size, 'ha': 'center',
                                        'path_effects': text_effect if not sold else 'center', 'va': 'top', 'color': color,
                                        'path_effects': text_effect}

                # Аннотация базовой информации
                check_and_annotate(x, y, basic_text, sold, text_properties_basic, drawn_annotations)

                offset_x = 0.2 * len(str(stat_text)) / 2
                stat_pixel_size = stat_size / 30
                # Аннотация статистики
                check_and_annotate(2*offset_x + x + (stat_pixel_size * offset_x if not sold else -stat_pixel_size * offset_x), y + offset_y, str(stat_text), sold,
                                   text_properties_stat, drawn_annotations)
            pbar.update(1)

    # Добавление названия графика и осей
    plt.title('Визуализация')
    plt.xlabel('Атрибуты')
    plt.ylabel('Нормализованное значение / Индекс для категориальных данных')

    # Установим метки на оси X
    plt.xticks(ticks=x_values, labels=annotations[0],
               rotation=45, fontsize=40)

    # Создаем пользовательские легенды
    sold_handle = mlines.Line2D([], [], color='red', marker='o', linestyle='None', label='Продано')
    for_sale_handle = mlines.Line2D([], [], color='green', marker='o', linestyle='None', label='На продаже')

    # Добавляем легенду на график
    plt.legend(handles=[sold_handle, for_sale_handle], loc='best')

    # Отображение графика
    plt.tight_layout()  # Автонастройка для предотвращения наложения текста

    plt.savefig(res_image_path, dpi=100)
    #plt.show()

if __name__ == "__main__":
    # Генерация данных
    num_of_cars = 100000
    region_of_interest = {'Модель': ["Focus"], "Марка": ["BMW"]}
    num_stat_category = {"Цена": [], "Пробег": []}

    raw_data = generate_raw_data(num_of_cars)
    cars_status = [random.choice([False, True]) for _ in range(num_of_cars)]

    data, cars_status = filter_data(raw_data, cars_status, region_of_interest, num_stat_category)

    statistics = calculate_statistics(data, cars_status)
    value_tables = prepare_value_tables(data)

    # Визуализация
    draw_general_data(data, cars_status, value_tables, statistics, "res.png")
