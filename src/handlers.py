import telebot
from datetime import datetime, timedelta
from tqdm import tqdm

from config import (
    get_cities,
    BOT_TOKEN,
    Commands,
    TIME_DELTA)

from telebot.types import InlineKeyboardMarkup

import visualizePopularCars
import visualizePriceRangePlot
from utils import getPriceFromDB, filterGarbageFromDigital

bot = telebot.TeleBot(BOT_TOKEN)
MAIN_PIPLINE = ""
private_group_chat_id = -1002008465600
print("Привет!")

@bot.message_handler(commands=[Commands.start])
def send_welcome(message):
    bot.reply_to(message, Messages.hi_message)
    bot.reply_to(message, Messages.hi_message1)
    bot.reply_to(message, Messages.hi_message2)

num_rows = 5
def get_brands_keyboard(prefix):
    keyboard = InlineKeyboardMarkup(row_width=num_rows)
    buttons = [InlineKeyboardButton(car_brand[0], callback_data=car_brand[1]) for car_brand in get_car_brands(prefix)]
    while buttons:
        keyboard.row(*buttons[:num_rows])
        buttons = buttons[num_rows:]
    return keyboard

def get_city_keyboard(prefix):
    keyboard = InlineKeyboardMarkup(row_width=num_rows)
    buttons = [InlineKeyboardButton(city[0], callback_data=city[1]) for city in get_cities(prefix)]
    while buttons:
        keyboard.row(*buttons[:num_rows])
        buttons = buttons[num_rows:]
    return keyboard

def get_start_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [InlineKeyboardButton("Start", callback_data="Start:Start")]
    keyboard.row(*buttons[:1])

    return keyboard

def get_confirm_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [InlineKeyboardButton("Yes", callback_data="Confirm:Yes"),
               InlineKeyboardButton("No", callback_data="Confirm:No")]

    while buttons:
        keyboard.row(*buttons[:2])
        buttons = buttons[2:]
    return keyboard

@bot.message_handler(commands=[Commands.get_general_info_graph], func=lambda message: message.chat.id == private_group_chat_id)
def get_general_info_graph(message):
    global MAIN_PIPLINE

    MAIN_PIPLINE = \
        f'Init/{Commands.ask_brand}/{Commands.ask_city}/{Commands.ask_price}/{Commands.get_general_info_graph}'

    keyboard = get_start_keyboard()
    bot.send_message(message.chat.id, "Нажмите старт для начала работы", reply_markup=keyboard)

def printPopularCars(chat_id, price_thresh, top_n):
    result = visualizePopularCars.main(price_thresh, top_n)
    bot.send_message(chat_id, "Марки/Модели/Кол-во")
    result_str = ""
    for i, car in enumerate(result):
        print(car)
        result_str += f"#{i}: {str(car)}\n"

    bot.send_message(chat_id, result_str)

@bot.message_handler(commands=[Commands.get_popular_models], func=lambda message: message.chat.id == private_group_chat_id)
def get_popular_models(message):
    global MAIN_PIPLINE

    MAIN_PIPLINE = f'Init/{Commands.ask_price_threshold}/{Commands.ask_top_n}/{Commands.get_popular_models}'

    keyboard = get_start_keyboard()
    bot.send_message(message.chat.id, "Нажмите старт для начала работы", reply_markup=keyboard)

@bot.message_handler(commands=[Commands.get_price_range_models], func=lambda message: message.chat.id == private_group_chat_id)
def get_price_range_models(message):
    global MAIN_PIPLINE

    MAIN_PIPLINE = \
        f'Init/{Commands.ask_brand}/{Commands.ask_price_threshold}/{Commands.ask_group_by_month}/{Commands.get_price_range_models}'

    keyboard = get_start_keyboard()
    bot.send_message(message.chat.id, "Нажмите старт для начала работы", reply_markup=keyboard)

########################################################################################################################

from config import (
    get_car_brands,
    BRAND_SPLIT_CHAR,
    PRICE_SPLIT_CHAR,
    Messages,
    Commands,
    ErrorMessages)

from telebot.types import InlineKeyboardButton
from checkDB import get_all_cars

from config import DBCommands
from vis import draw_general_data, filter_data, calculate_statistics, prepare_value_tables

params = {}

def call_next_step_in_pipline(call):
    global MAIN_PIPLINE

    if MAIN_PIPLINE.startswith(f'{Commands.ask_brand}/'):
        keyboard = get_brands_keyboard(Commands.get_general_info_graph)
        keyboard.add(InlineKeyboardButton("All", callback_data=Commands.get_general_info_graph + ":All"))

        try:
            bot.send_message(call.chat.id, Messages.enter_city, reply_markup=keyboard)
        except:
            bot.send_message(call.message.chat.id, Messages.enter_city, reply_markup=keyboard)

    elif MAIN_PIPLINE.startswith(f'{Commands.ask_city}/'):
        keyboard = get_city_keyboard("")
        keyboard.add(
            InlineKeyboardButton("All", callback_data=":All"))

        try:
            bot.send_message(call.chat.id, Messages.enter_city, reply_markup=keyboard)
        except:
            bot.send_message(call.message.chat.id, Messages.enter_city, reply_markup=keyboard)

    elif MAIN_PIPLINE.startswith(f'{Commands.ask_price_threshold}/'):
        try:
            msg = bot.send_message(call.chat.id, Messages.enter_price_threshold)
        except:
            msg = bot.send_message(call.message.chat.id, Messages.enter_price_threshold)

        bot.register_next_step_handler(msg, callback_query)

    elif MAIN_PIPLINE.startswith(f'{Commands.ask_top_n}/'):
        try:
            msg = bot.send_message(call.chat.id, Messages.enter_top_n_threshold)
        except:
            msg = bot.send_message(call.message.chat.id, Messages.enter_top_n_threshold)

        bot.register_next_step_handler(msg, callback_query)

    elif MAIN_PIPLINE.startswith(f'{Commands.ask_price}/'):
        try:
            msg = bot.send_message(call.chat.id, Messages.enter_price)
        except:
            msg = bot.send_message(call.message.chat.id, Messages.enter_price)

        bot.register_next_step_handler(msg, callback_query)

    elif MAIN_PIPLINE.startswith(f'{Commands.ask_group_by_month}'):
        keyboard = get_confirm_keyboard()
        try:
            bot.send_message(call.chat.id, "Группировать данные по месяцам?", reply_markup=keyboard)
        except:
            bot.send_message(call.message.chat.id, "Группировать данные по месяцам?", reply_markup=keyboard)
        return

    elif MAIN_PIPLINE.startswith(f'{Commands.get_general_info_graph}'):
        try:
            bot.send_message(call.chat.id, "Обрабатываю данные")
        except:
            bot.send_message(call.message.chat.id, "Обрабатываю данные")

        callback_query(call)
        return
    elif MAIN_PIPLINE.startswith(f'{Commands.get_price_range_models}'):
        try:
            bot.send_message(call.chat.id, "Обрабатываю данные")
        except:
            bot.send_message(call.message.chat.id, "Обрабатываю данные")

        callback_query(call)
        return

    elif MAIN_PIPLINE.startswith(f'{Commands.get_popular_models}'):
        try:
            msg = bot.send_message(call.chat.id, "Обрабатываю данные")
        except:
            msg = bot.send_message(call.message.chat.id, "Обрабатываю данные")
        callback_query(call)
        return


def is_wrong_price_thresh(thresh_price):
    if not thresh_price.isdigit() or int(thresh_price) < 0:
        return True
    return False

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global params
    global MAIN_PIPLINE
    print(MAIN_PIPLINE)
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    if MAIN_PIPLINE.startswith(f'Init/'):
        MAIN_PIPLINE = MAIN_PIPLINE[len(f'Init/'):]
        params = {}
        call_next_step_in_pipline(call)
        return

    if MAIN_PIPLINE.startswith(f'{Commands.ask_brand}/'):
        # Если была выбран бренд автомобиля
        prefix_value = call.data.split(BRAND_SPLIT_CHAR)
        brand = prefix_value[1]

        try:
            bot.send_message(call.chat.id, f"Выбрано: {brand}")
        except:
            bot.send_message(call.message.chat.id, f"Выбрано: {brand}")

        params['Марка'] = [brand]
        print(f"Выбран: {brand}")

        MAIN_PIPLINE = MAIN_PIPLINE[len(f'{Commands.ask_brand}/'):]
        call_next_step_in_pipline(call)
        return

    elif MAIN_PIPLINE.startswith(f'{Commands.ask_price_threshold}/'):
        thresh = call.text.strip()[1:]

        if is_wrong_price_thresh(thresh):
            try:
                bot.send_message(call.chat.id, f"Выбрано: {thresh} - Исправьте ошибку")
            except:
                bot.send_message(call.message.chat.id, f"Выбрано: {thresh} - Исправьте ошибку")

            call_next_step_in_pipline(call)
            return

        params['Ценовой порог'] = int(thresh)

        try:
            bot.send_message(call.chat.id, f"Выбрано: {thresh}")
        except:
            bot.send_message(call.message.chat.id, f"Выбрано: {thresh}")

        MAIN_PIPLINE = MAIN_PIPLINE[len(f'{Commands.ask_price_threshold}/'):]
        call_next_step_in_pipline(call)

        return

    elif MAIN_PIPLINE.startswith(f'{Commands.ask_top_n}/'):
        thresh = call.text.strip()[1:]

        if is_wrong_price_thresh(thresh):
            try:
                bot.send_message(call.chat.id, f"Выбрано: {thresh} - Исправьте ошибку")
            except:
                bot.send_message(call.message.chat.id, f"Выбрано: {thresh} - Исправьте ошибку")

            call_next_step_in_pipline(call)
            return

        params['Кол-во в топе'] = int(thresh)

        try:
            bot.send_message(call.chat.id, f"Выбрано: {thresh}")
        except:
            bot.send_message(call.message.chat.id, f"Выбрано: {thresh}")

        MAIN_PIPLINE = MAIN_PIPLINE[len(f'{Commands.ask_top_n}/'):]
        call_next_step_in_pipline(call)

        return

    elif MAIN_PIPLINE.startswith(f'{Commands.ask_city}/'):
        # Если была выбран бренд автомобиля
        city = call.data.split(BRAND_SPLIT_CHAR)[1]
        params['Город'] = [city]
        print(f"Выбран: {city}")

        try:
            bot.send_message(call.chat.id, f"Выбрано: {city}")
        except:
            bot.send_message(call.message.chat.id, f"Выбрано: {city}")

        MAIN_PIPLINE = MAIN_PIPLINE[len(f'{Commands.ask_city}/'):]
        call_next_step_in_pipline(call)
        return

    elif MAIN_PIPLINE.startswith(f'{Commands.ask_price}/'):
        price = call.text.strip()[1:]
        price_from_to = price.split(PRICE_SPLIT_CHAR)

        if is_wrong_price(call.chat.id, price_from_to):
            call_next_step_in_pipline(call)
            return

        MAIN_PIPLINE = MAIN_PIPLINE[len(f'{Commands.ask_price}/'):]
        params['Цена'] = price

        call_next_step_in_pipline(call)
        return
    elif MAIN_PIPLINE.startswith(f'{Commands.ask_group_by_month}'):
        # Если был выбран бренд автомобиля

        result = call.data.split(BRAND_SPLIT_CHAR)[1]
        params['Группировка'] = result == "Yes"
        print(f"Выбран: {result}")

        MAIN_PIPLINE = MAIN_PIPLINE[len(f'{Commands.ask_group_by_month}/'):]
        call_next_step_in_pipline(call)

        return

    if MAIN_PIPLINE.startswith(f'{Commands.get_general_info_graph}'):
        params["Режим"] = Commands.get_general_info_graph
        handle_get_data(call, params)
        return

    if MAIN_PIPLINE.startswith(f'{Commands.get_price_range_models}'):
        visualizePriceRangePlot.main(params["Марка"][0], params['Группировка'], params['Ценовой порог'])

        photo_path = f"{Commands.get_price_range_models}.jpg"

        with open(photo_path, 'rb') as photo:
            try:
                bot.send_photo(call.message.chat.id, photo)
            except:
                bot.send_photo(call.chat.id, photo)
        return

    if MAIN_PIPLINE.startswith(f'{Commands.get_popular_models}'):
        try:
            printPopularCars(call.message.chat.id, params["Ценовой порог"], params["Кол-во в топе"])
        except:
            printPopularCars(call.chat.id, params["Ценовой порог"], params["Кол-во в топе"])

        return

def add_to_raw_data(raw_data, cars, isCarModelNeeded):
    print("Обрабатываю сырые данные")
    for data_i in tqdm(cars):
        try:
            details_fields = ["Marka", "Gorivo", "Kilometraža", "Menjač"]
            if isCarModelNeeded:
                details_fields.append("Model")

            missing_details_fields = [field for field in data_i['Детали'] if field not in details]

            if missing_details_fields:
                raise ValueError(f"Missing fields: {missing_details_fields}")

            # Получаем дату из поля "Дата"
            date_str = data_i["Дата"]
            date = datetime.strptime(date_str.split()[0], '%Y-%m-%d')

            # Проверяем, если дата обновления меньше, чем текущая дата минус TIME_DELTA дня,
            # то пропускаем эту запись
            if date > datetime.now() - timedelta(days=TIME_DELTA):
                continue

            price = getPriceFromDB(data_i["Цена"])
            if price == None:
                continue
            raw_data['Цена'].append(price)

        except Exception as error:
            print(error)
            print(data_i)
            continue

        raw_data['Город'].append(data_i["Город"].lower())

        details = data_i['Детали']

        raw_data['Марка'].append(details["Marka"])

        if isCarModelNeeded:
            try:
                raw_data['Модель'].append(details["Model"])
            except:
                raw_data['Модель'].append("None")

        raw_data['Вид топлива'].append(details["Gorivo"])
        raw_data['Пробег'].append(int(filterGarbageFromDigital(details["Kilometraža"])))
        raw_data['Коробка передач'].append(details["Menjač"])


def send_photo(message, region_of_interest):
    photo_path = 'general_info_graph.jpg'

    #region_of_interest = {"Город": ["Beograd"], "Model": ["Volvo"]}
    #region_of_interest = {}

    isCarModelNeeded = not "All" in region_of_interest["Марка"]

    if not isCarModelNeeded:
        del region_of_interest["Марка"]

    if "All" in region_of_interest["Город"]:
        region_of_interest["Город"].clear()
        for value in get_cities(""):
            city = value[1].split(BRAND_SPLIT_CHAR)[-1]
            region_of_interest["Город"].append(city)

    raw_data = {
        'Цена': [],
        'Город': [],
        'Марка': [],
        'Вид топлива': [],
        'Пробег': [],
        'Коробка передач': []
    }

    if isCarModelNeeded:
        raw_data['Модель'] = []

    num_stat_category = {"Цена": [], "Пробег": []}

    raw_cars_status = []

    SELECT_COMMAND = DBCommands.select_in_cars

    cars = get_all_cars(SELECT_COMMAND)
    print("Собрал все данные")

    add_to_raw_data(raw_data, cars, isCarModelNeeded)
    raw_cars_status.extend([False] * len(raw_data["Цена"]))

    SELECT_COMMAND = DBCommands.select_in_sold_cars
    sold_cars = get_all_cars(SELECT_COMMAND)
    add_to_raw_data(raw_data, sold_cars, isCarModelNeeded)
    print("Подготовил все данные")

    raw_cars_status.extend([True] * abs(len(raw_data["Цена"]) - len(raw_cars_status)))

    data, cars_status = filter_data(raw_data, raw_cars_status, region_of_interest, num_stat_category)
    print("Отфильтровал все данные")

    if len(data["Цена"]) == 0:
        bot.send_message(message.chat.id, ErrorMessages.no_data)
        return
    else:
        bot.send_message(message.chat.id, "Начинаю делать визуализацию")

    statistics = calculate_statistics(data, cars_status)
    value_tables = prepare_value_tables(data)

    print("Рисую")
    draw_general_data(data, cars_status, value_tables, statistics, photo_path)

    with open(photo_path, 'rb') as photo:
        bot.send_photo(message.chat.id, photo)

def is_wrong_price(chat_id, price_from_to):
    if len(price_from_to) != 2:
        bot.send_message(chat_id, ErrorMessages.price_error_wrong_num)
        return True

    if not price_from_to[0].isdigit() or int(price_from_to[0]) < 0:
        bot.send_message(chat_id, ErrorMessages.price_error_wrong_range)
        return True

    if not price_from_to[1].isdigit() or int(price_from_to[1]) < 0:
        bot.send_message(chat_id, ErrorMessages.price_error_wrong_range)
        return True

    if int(price_from_to[1]) < int(price_from_to[0]):
        bot.send_message(chat_id, ErrorMessages.price_error_wrong_swap)
        return True

    return False

def handle_get_data(message, params):
    print("handle_get_data")

    if params["Режим"] == Commands.get_data:
        del params["Режим"]
        # Assuming get_all_cars is modified to accept parameters, pass them as needed
        data = get_all_cars(params)
        for data_i in data:
            bot.send_message(message.chat.id, str(data_i))

    elif params["Режим"] == Commands.get_general_info_graph:
        del params["Режим"]
        send_photo(message, params)

# Функция для обработки polling в отдельном потоке
def start_polling():
    bot.polling(none_stop=True)
