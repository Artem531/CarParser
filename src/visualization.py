import pandas as pd
import matplotlib.pyplot as plt
import random
import matplotlib.patheffects as PathEffects
import matplotlib.lines as mlines

def round_to_nearest(number, step):
    return round(number / step) * step

region_of_interest = {'Модель' : "Focus", "Марка" : "BMW" }
#region_of_interest = {}

num_of_cars = 100000
# Расширим исходный словарь data, добавив 100 машин
raw_data = {
    'Цена': [random.randint(5000, 100000) for _ in range(num_of_cars)],
    'Город': [random.choice(['Москва', 'Санкт-Петербург', 'Новосибирск', 'Екатеринбург', 'Казань']) for _ in range(num_of_cars)],
    'Марка': [random.choice(['Toyota', 'Ford', 'Mercedes', 'BMW', 'Audi', 'Volkswagen', 'Hyundai', 'Kia']) for _ in range(num_of_cars)],
    'Модель': [random.choice(['Camry', 'Focus', 'C-Class', '3 Series', 'A4', 'Golf', 'Tucson', 'Sportage']) for _ in range(num_of_cars)],
    'Вид топлива': [random.choice(['бензин', 'дизель', 'электро', 'гибрид']) for _ in range(num_of_cars)],
    'Пробег': [random.randint(0, 30000) for _ in range(num_of_cars)],
    'Коробка передач': [random.choice(['автомат', 'механика']) for _ in range(num_of_cars)]
}

cars_status = [random.choice([False, True]) for _ in range(num_of_cars)]

data = {
    'Цена': [],
    'Город': [],
    'Марка': [],
    'Модель': [],
    'Вид топлива': [],
    'Пробег': [],
    'Коробка передач': []
}

num_stat_category = {"Цена": [], "Пробег": []}
for i in range(len(raw_data['Цена'])):
    needToSkip = False
    for category in raw_data:
        if not category in region_of_interest:
            continue

        if category in num_stat_category:
            bounders = region_of_interest[category].split("-")
            if not (raw_data[category][i] > int(bounders[0]) and raw_data[category][i] < int(bounders[1])):
                needToSkip = True
                break
        else:
            if not raw_data[category][i] in region_of_interest[category]:
                needToSkip = True
                break

    if needToSkip:
        continue

    for category in raw_data:
        if category in num_stat_category:
            discrete_value = raw_data[category][i]
            if category == "Цена":
                discrete_value = round_to_nearest(discrete_value, 5000)
            if category == "Пробег":
                discrete_value = round_to_nearest(discrete_value, 1000)

            data[category].append(discrete_value)
        else:
            data[category].append(raw_data[category][i])

# Считаем статистику для каждого атрибута
statistics = {category:
                  { car_status: {} for car_status in [True, False] }
              for category in ['Цена', 'Город', 'Марка', 'Модель', 'Вид топлива', 'Пробег', 'Коробка передач']}

for category in statistics.keys():
    for i, value in enumerate(data[category]):
        car_status = cars_status[i]  # Получаем статус автомобиля для текущего индекса
        # Используем метод get для получения текущего количества, устанавливаем 0 по умолчанию
        current_count = statistics[category][car_status].get(value, 0)
        # Увеличиваем счётчик для данного значения на 1
        statistics[category][car_status][value] = current_count + 1

print(statistics)

print("finish generate")
def normalize_value(value, min_value, max_value):
    """Нормализует числовое значение, если это необходимо."""
    if max_value - min_value != 0:
        return (value - min_value) / (max_value - min_value)
    else:
        return value / max_value

# Обновим создание словарей с учетом нормализации числовых значений
value_tables = {}
scale = 1000

for category, values in data.items():
    # Проверяем, является ли значение числовым
    if all(isinstance(value, (int, float)) for value in values):
        min_value, max_value = min(values), max(values)
        normalized_values = [normalize_value(value, min_value, max_value) for value in values]
        value_tables[category] = {value: normalized * scale for value, normalized in zip(values, normalized_values)}
    else:
        set_values = set(values)
        value_tables[category] = {value: (index + 1) / len(set_values) * scale  for index, value in enumerate(set_values)}


print("finish value_tables")
print(value_tables)
# Переведём в DataFrame и нормализуем числовые данные
df_data = pd.DataFrame(data)

# Создание графика
plt.figure(figsize=(32, 16))

text_effect = [PathEffects.withStroke(linewidth=3, foreground="black")]

# Подготовка данных перед циклом
headers = list(data.keys())  # Заголовки для упрощения доступа
x_values = range(len(headers))  # x координаты одинаковы для всех линий

# Предварительные вычисления для аннотаций
annotations = [
    ["Цена", "Город", "Марка", "Модель", "Вид топлива", "Пробег", "Коробка передач"],
    ["Цена", "Город", "Марка", "Модель", "Вид топлива", "Пробег", "Коробка передач"]
]

drawn_annotations = set()  # Множество для отслеживания аннотаций
drawn_segments = set()  # Для отслеживания уже нарисованных отрезков

def check_and_annotate(x, y, text, sold, text_properties):
    annotation_key = (x, y, text, sold)
    if annotation_key not in drawn_annotations:
        plt.text(x, y, text, **text_properties)
        drawn_annotations.add(annotation_key)

offset_y = 0.036

# Функция для проверки и добавления отрезка в набор
def check_and_draw(x1, y1, x2, y2, color='g', marker='o', linestyle='-'):
    segment = ((x1, y1), (x2, y2)) if (x1, y1) < (x2, y2) else ((x2, y2), (x1, y1))
    if segment not in drawn_segments:
        plt.plot([x1, x2], [y1, y2], color=color,  marker=marker, linestyle=linestyle)  # Отрисовка отрезка
        drawn_segments.add(segment)

print("Start draw")
for index, row in df_data.iterrows():
    y_values = [value_tables[header][row[header]] for header in data.keys()]
    sold = cars_status[index]
    color = 'g' if not sold else 'r'

    # Прорисовка отрезков линии, если они еще не были нарисованы
    for i in range(len(y_values) - 1):
        check_and_draw(i, y_values[i], i + 1, y_values[i + 1], color='grey')

    # Отрисовка аннотаций, если они ещё не были нарисованы
    for i, (x, y) in enumerate(zip(x_values, y_values)):
        basic_text = row[annotations[0][i]]  # Базовая аннотация
        stat_text = statistics[annotations[1][i]][sold][row[annotations[1][i]]]  # Статистика

        # Параметры отображения текста
        text_properties_basic = {'fontsize': 18, 'ha': 'right', 'va': 'bottom'}
        text_properties_stat = {'fontsize': 16, 'ha': 'center', 'path_effects': text_effect if not sold else 'center', 'va': 'top', 'color': color, 'path_effects': text_effect}

        # Аннотация базовой информации
        check_and_annotate(x, y, basic_text, sold, text_properties_basic)

        offset_x = 0.05 * len(str(stat_text)) / 2
        # Аннотация статистики
        check_and_annotate(x + (offset_x if not sold else -offset_x), y + offset_y, str(stat_text), sold, text_properties_stat)

# Добавление названия графика и осей
plt.title('Пример данных из DataFrame')
plt.xlabel('Атрибуты')
plt.ylabel('Нормализованное значение / Индекс для категориальных данных')

# Установим метки на оси X
plt.xticks(ticks=x_values, labels=['Цена', 'Город', 'Марка', 'Модель', 'Вид топлива', 'Пробег', 'Коробка передач'],
           rotation=45)

# Создаем пользовательские легенды
sold_handle = mlines.Line2D([], [], color='red', marker='o', linestyle='None', label='Продано')
for_sale_handle = mlines.Line2D([], [], color='green', marker='o', linestyle='None', label='На продаже')

# Добавляем легенду на график
plt.legend(handles=[sold_handle, for_sale_handle], loc='best')

# Отображение графика
plt.tight_layout()  # Автонастройка для предотвращения наложения текста

plt.savefig( "res.png", dpi=100)
plt.show()