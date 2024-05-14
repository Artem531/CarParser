BOT_TOKEN = '6534132720:AAHEPEvwu9pcvf1Hdv3B3SM94fCkV7mCzBk'
BRAND_SPLIT_CHAR = ":"
PRICE_SPLIT_CHAR = "-"
TEST_BRAND = "bmw"
BASE_URL = 'https://www.polovniautomobili.com/auto-oglasi/pretraga'
TIME_DELTA = 0


WEB_HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    # 'cookie': '_gcl_au=1.1.1812305014.1711667902; _pbjs_userid_consent_data=3524755945110770; pa-cookie-message=accepted; _fbp=fb.1.1711667902228.1059682735; am-uid-f=f2781a61-36db-4813-aff9-96cf83c28e8c; device_view=full; _gid=GA1.2.692487532.1711816226; global-notification-dont-check=1; __gads=ID=926c8f11489d4c43:T=1711667902:RT=1711817849:S=ALNI_MZKifYf4XR9uLPzineP93TwCcTxIw; __gpi=UID=00000d85678ffc7f:T=1711667902:RT=1711817849:S=ALNI_MZjdH3IyPyXdS_sxF44a9NOD8R_SQ; __eoi=ID=cbca17bc096223fa:T=1711667902:RT=1711817849:S=AA-AfjacPtpgIngTRFRLUGw6HSTt; stpdOrigin={"origin":"direct"}; cto_bidid=gHpEYF85Nlc4RGRDWEgzNWdSZkZrTDdnNyUyQmxha3BTdUYwQzZWWEJLNUZiQzJHd1hHempMZDdjaW14Vm1Ia1J1cGd1bEFTQ0pQN05tRDFFMGhBSWlGM1NrJTJCaDdPamJsMHM3WThKYzJOcXU4ZUZOSnZMOCUyRjBoaXN5TmxDRDdZbmV3c1dXRg; cto_bundle=atWuAl9xamJ6WEJPbWpscmNlcTFpRWt5bGlQb0gzcmFnNHc3TklJTEhVS2xlWmJsVCUyRnpMWUt2OE1Xb3NyM3FVc241QTlRNWZYamNzUUZrNFEwNUJlSE1RVGdPT2NiZTI1UVRmbEtsaVBaUmZqZ0slMkZxTTZtUXZPNnFsdkFER2RiaEt5UHc4bFVSaEIlMkY2Z3lWaGs3VEE1VlFTcFclMkZVSDdrS1pQSFRjQm9JZTA2UmQ3ekFpdVNwQld0SnIzV2VPZ29abGxsczZ0JTJGc2dCVlE2SW95ZmJrTTY1Y0kyMyUyQm1OdjJuVlQ4ZSUyRmNDUWhYY01yUWclM0Q; _ga=GA1.1.1440224938.1711667902; FCNEC=%5B%5B%22AKsRol9Qrg27-yY-AmISykzVoNATFQeFU1UVvgmH9OBQF1lpJrDSQPsbPpxG0BVh5QPgGqJAKp96asT6WmjmDZXUn167QO8g4J9QDUXKJjFaMTIsvZ4n0z_20SBIchKgzLtaxJpdF65dtFQZV52KUzBZpfmT64v7fw%3D%3D%22%5D%5D; _ga_QBY7EP0X15=GS1.1.1711816226.2.1.1711818125.60.0.0',
    'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
}

def get_params( brand = "" ):
    PARAMS = {
        'brand': brand,

        #'price_from': '0',
        #'price_to': '10000000',

        #'year_from': '2024',
        #'year_to': '2025',

        #'engine_volume_from': '0',
        #'engine_volume_to': '100000',

        #'fuel[0]': '45', # Benzin
        #'fuel[1]': '2309', # Dizel

        #'door_num': '3012',

        'city_distance': '0',
        'region[0]': 'Beograd',
        'region[1]': 'Centralna Srbija',
        'region[2]': 'Istočna Srbija',
        'region[3]': 'Južna Srbija',
        'region[4]': 'Kosovo i Metohija',
        'region[5]': 'Vojvodina',
        'region[6]': 'Zapadna Srbija',
        'region[7]': '2544', # Beograd (uži)
        'region[8]': '2543', # Beograd (širi)
        'region[9]': '2557', # Borski
        'region[10]': '2554', # Braničevski
        'region[11]': '2566', # Jablanički
        'region[12]': '2550', # Južno-bački
        'region[13]': '2548', # Južno-banatski
        'region[14]': '2553', # Kolubarski
        'region[15]': '2568', # Kosovski
        'region[16]': '3017', # Kosovsko-pomoravski
        'region[17]': '2571', # Kosovsko-mitrovački
        'region[18]': '2552', # Mačvanski
        'region[19]': '2560', # Moravički
        'region[20]': '2563', # Nišavski
        'region[21]': '2567', # Pčinjski
        'region[22]': '2569', # Pećki
        'region[23]': '2565', # Pirotski
        'region[24]': '2542', # Podunavski
        'region[25]': '2556', # Pomoravski
        'region[26]': '2570', # Prizrenski
        'region[27]': '2562', # Rasinski
        'region[28]': '2561', # Raški
        'region[29]': '2545', # Severno-bački
        'region[30]': '2547', # Severno-banatski
        'region[31]': '2546', # Srednje-banatski
        'region[32]': '2551', # Sremski
        'region[33]': '2555', # Šumadijski
        'region[34]': '2564', # Toplički
        'region[35]': '2558', # Zaječarski
        'region[36]': '2549', # Zapadno-bački
        'region[37]': '2559', # Zlatiborski
        'region[38]': '25', # Inostranstvo

        'sort': 'price_asc',

        'showOldNew': 'all',
        'without_price': '1',

        'page': '0'
    }
    return PARAMS

def get_car_brands( prefix="scheduled_fetch" ):
    CAR_BRANDS = [
        ('acura', f'{prefix}{BRAND_SPLIT_CHAR}acura'),
        ('alfa-romeo', f'{prefix}{BRAND_SPLIT_CHAR}alfa-romeo'),
        ('ac', f'{prefix}{BRAND_SPLIT_CHAR}ac'),
        ('audi', f'{prefix}{BRAND_SPLIT_CHAR}audi'),
        ('baw', f'{prefix}{BRAND_SPLIT_CHAR}baw'),
        ('bentley', f'{prefix}{BRAND_SPLIT_CHAR}bentley'),
        ('bmw', f'{prefix}{BRAND_SPLIT_CHAR}bmw'),
        ('buick', f'{prefix}{BRAND_SPLIT_CHAR}buick'),
        ('cadillac', f'{prefix}{BRAND_SPLIT_CHAR}cadillac'),
        ('chery', f'{prefix}{BRAND_SPLIT_CHAR}chery'),
        ('chevrolet', f'{prefix}{BRAND_SPLIT_CHAR}chevrolet'),
        ('chrysler', f'{prefix}{BRAND_SPLIT_CHAR}chrysler'),
        ('citroen', f'{prefix}{BRAND_SPLIT_CHAR}citroen'),
        ('cupra', f'{prefix}{BRAND_SPLIT_CHAR}cupra'),
        ('dacia', f'{prefix}{BRAND_SPLIT_CHAR}dacia'),
        ('daewoo', f'{prefix}{BRAND_SPLIT_CHAR}daewoo'),
        ('daihatsu', f'{prefix}{BRAND_SPLIT_CHAR}daihatsu'),
        ('dodge', f'{prefix}{BRAND_SPLIT_CHAR}dodge'),
        ('dr', f'{prefix}{BRAND_SPLIT_CHAR}dr'),
        ('ds', f'{prefix}{BRAND_SPLIT_CHAR}ds'),
        ('ferrari', f'{prefix}{BRAND_SPLIT_CHAR}ferrari'),
        ('fiat', f'{prefix}{BRAND_SPLIT_CHAR}fiat'),
        ('ford', f'{prefix}{BRAND_SPLIT_CHAR}ford'),
        ('gaz', f'{prefix}{BRAND_SPLIT_CHAR}gaz'),
        ('geely', f'{prefix}{BRAND_SPLIT_CHAR}geely'),
        ('great-wall', f'{prefix}{BRAND_SPLIT_CHAR}great-wall'),
        ('honda', f'{prefix}{BRAND_SPLIT_CHAR}honda'),
        ('hummer', f'{prefix}{BRAND_SPLIT_CHAR}hummer'),
        ('hyundai', f'{prefix}{BRAND_SPLIT_CHAR}hyundai'),
        ('infiniti', f'{prefix}{BRAND_SPLIT_CHAR}infiniti'),
        ('isuzu', f'{prefix}{BRAND_SPLIT_CHAR}isuzu'),
        ('jaguar', f'{prefix}{BRAND_SPLIT_CHAR}jaguar'),
        ('jeep', f'{prefix}{BRAND_SPLIT_CHAR}jeep'),
        ('jinpeng', f'{prefix}{BRAND_SPLIT_CHAR}jinpeng'),
        ('kia', f'{prefix}{BRAND_SPLIT_CHAR}kia'),
        ('lada', f'{prefix}{BRAND_SPLIT_CHAR}lada'),
        ('lamborghini', f'{prefix}{BRAND_SPLIT_CHAR}lamborghini'),
        ('lancia', f'{prefix}{BRAND_SPLIT_CHAR}lancia'),
        ('land-rover', f'{prefix}{BRAND_SPLIT_CHAR}land-rover'),
        ('lexus', f'{prefix}{BRAND_SPLIT_CHAR}lexus'),
        ('lincoln', f'{prefix}{BRAND_SPLIT_CHAR}lincoln'),
        ('linzda', f'{prefix}{BRAND_SPLIT_CHAR}linzda'),
        ('mahindra', f'{prefix}{BRAND_SPLIT_CHAR}mahindra'),
        ('maserati', f'{prefix}{BRAND_SPLIT_CHAR}maserati'),
        ('mazda', f'{prefix}{BRAND_SPLIT_CHAR}mazda'),
        ('mercedes-benz', f'{prefix}{BRAND_SPLIT_CHAR}mercedes-benz'),
        ('mercury', f'{prefix}{BRAND_SPLIT_CHAR}mercury'),
        ('mg', f'{prefix}{BRAND_SPLIT_CHAR}mg'),
        ('mini', f'{prefix}{BRAND_SPLIT_CHAR}mini'),
        ('mitsubishi', f'{prefix}{BRAND_SPLIT_CHAR}mitsubishi'),
        ('moskvitch', f'{prefix}{BRAND_SPLIT_CHAR}moskvitch'),
        ('nissan', f'{prefix}{BRAND_SPLIT_CHAR}nissan'),
        ('oldsmobile', f'{prefix}{BRAND_SPLIT_CHAR}oldsmobile'),
        ('opel', f'{prefix}{BRAND_SPLIT_CHAR}opel'),
        ('peugeot', f'{prefix}{BRAND_SPLIT_CHAR}peugeot'),
        ('piaggio', f'{prefix}{BRAND_SPLIT_CHAR}piaggio'),
        ('polski-fiat', f'{prefix}{BRAND_SPLIT_CHAR}polski-fiat'),
        ('pontiac', f'{prefix}{BRAND_SPLIT_CHAR}pontiac'),
        ('porsche', f'{prefix}{BRAND_SPLIT_CHAR}porsche'),
        ('renault', f'{prefix}{BRAND_SPLIT_CHAR}renault'),

        ('rolls-royce', f'{prefix}{BRAND_SPLIT_CHAR}rolls-royce'),
        ('rover', f'{prefix}{BRAND_SPLIT_CHAR}rover'),
        ('saab', f'{prefix}{BRAND_SPLIT_CHAR}saab'),
        ('seat', f'{prefix}{BRAND_SPLIT_CHAR}seat'),
        ('shuanghuan', f'{prefix}{BRAND_SPLIT_CHAR}shuanghuan'),
        ('simca', f'{prefix}{BRAND_SPLIT_CHAR}simca'),
        ('smart', f'{prefix}{BRAND_SPLIT_CHAR}smart'),
        ('ssangyong', f'{prefix}{BRAND_SPLIT_CHAR}ssangyong'),
        ('subaru', f'{prefix}{BRAND_SPLIT_CHAR}subaru'),
        ('suzuki', f'{prefix}{BRAND_SPLIT_CHAR}suzuki'),
        ('talbot', f'{prefix}{BRAND_SPLIT_CHAR}talbot'),
        ('tata', f'{prefix}{BRAND_SPLIT_CHAR}tata'),
        ('tavria', f'{prefix}{BRAND_SPLIT_CHAR}tavria'),
        ('tesla', f'{prefix}{BRAND_SPLIT_CHAR}tesla'),
        ('toyota', f'{prefix}{BRAND_SPLIT_CHAR}toyota'),
        ('trabant', f'{prefix}{BRAND_SPLIT_CHAR}trabant'),
        ('uaz', f'{prefix}{BRAND_SPLIT_CHAR}uaz'),
        ('volkswagen', f'{prefix}{BRAND_SPLIT_CHAR}volkswagen'),
        ('volvo', f'{prefix}{BRAND_SPLIT_CHAR}volvo'),
        ('wartburg', f'{prefix}{BRAND_SPLIT_CHAR}wartburg'),
        ('zastava', f'{prefix}{BRAND_SPLIT_CHAR}zastava'),
        ('zhidou', f'{prefix}{BRAND_SPLIT_CHAR}zhidou'),
        ('škoda', f'{prefix}{BRAND_SPLIT_CHAR}skoda'),
        ('ostalo', f'{prefix}{BRAND_SPLIT_CHAR}ostalo')
    ]
    return CAR_BRANDS

def get_cities(prefix):
    CITIES = [
        ('Beograd', f'{prefix}{BRAND_SPLIT_CHAR}Beograd'),
        ('Novi Beograd', f'{prefix}{BRAND_SPLIT_CHAR}Novi Beograd'),
        ('Zemun', f'{prefix}{BRAND_SPLIT_CHAR}Zemun'),
        ('Novi Sad', f'{prefix}{BRAND_SPLIT_CHAR}Novi Sad'),
        ('Niš', f'{prefix}{BRAND_SPLIT_CHAR}Niš')
    ]
    return CITIES

class DBTableName:
    cars_table_name: str = "cars"
    sold_cars_table_name: str = "sold_cars"

class Commands:
    start: str = "start"
    get_data: str = "get_data"
    get_general_info_graph: str = "get_general_info_graph"
    get_popular_models: str = "get_popular_models"
    get_price_range_models: str = "get_price_range_models"

    ask_price: str = "ask_price"
    ask_city: str = "ask_city"
    ask_brand: str = "ask_brand"
    ask_group_by_month: str = "ask_group_by_month"
    ask_price_threshold: str = "ask_price_threshold"
    ask_top_n: str = "ask_top_n"

class DBCommands:
    data_headers: str = "url, city, price, details, insert_time"

    create_cars_DB: str = f'''CREATE TABLE IF NOT EXISTS {DBTableName.cars_table_name}
                (url TEXT PRIMARY KEY, city TEXT, price TEXT, details TEXT, session_updated INTEGER DEFAULT 0,
                insert_time DATETIME DEFAULT (datetime('now', 'localtime')))'''

    create_sold_cars_DB: str = f'''CREATE TABLE IF NOT EXISTS {DBTableName.sold_cars_table_name} 
                (url TEXT PRIMARY KEY, city TEXT, price TEXT, details TEXT,
                insert_time DATETIME DEFAULT (datetime('now', 'localtime')))'''

    delete_from_cars: str = f"DELETE FROM {DBTableName.cars_table_name}"
    delete_from_sold_cars: str = f"DELETE FROM {DBTableName.sold_cars_table_name}"

    insert_in_cars: str = f'''INSERT OR IGNORE INTO {DBTableName.cars_table_name}
                ({data_headers}, session_updated) VALUES (?, ?, ?, ?, datetime('now', 'localtime'), 1)'''
    insert_in_sold_cars: str = f"INSERT INTO {DBTableName.sold_cars_table_name} ({data_headers}) VALUES (?, ?, ?, ?, datetime('now', 'localtime'))"

    select_in_cars: str = f"SELECT {data_headers} FROM {DBTableName.cars_table_name}"
    select_in_sold_cars: str = f"SELECT {data_headers} FROM {DBTableName.sold_cars_table_name}"

    update_session_in_cars: str = f"UPDATE {DBTableName.cars_table_name} SET session_updated = 0"
    update_data_in_cars: str = f'''UPDATE {DBTableName.cars_table_name} 
                SET city = ?, price = ?, details = ?, session_updated = 1 WHERE url = ?'''

class Messages:
    hi_message: str = f"Привет! Напишите /{Commands.get_general_info_graph}, чтобы вывести общую информацию о рынке."
    hi_message1: str = f"Напишите /{Commands.get_popular_models}, чтобы вывести топ 10 самых популярных моделей."
    hi_message2: str = f"Напишите /{Commands.get_price_range_models}, чтобы вывести ценовые диапазоны и динамику цен."

    enter_price: str = f"Введите диапазон цен автомобиля (например, /0{PRICE_SPLIT_CHAR}10000):"
    enter_price_threshold: str = f"Введите порог старта цен автомобиля (например, /10000):"
    enter_top_n_threshold: str = f"Введите кол-во машин в топе (например, /10):"
    enter_brand: str = "Выберите марку автомобиля:",
    enter_city: str = "Выберите город продажи:"

class ErrorMessages:
    no_data: str = "Нет данных по данному запросу"

    price_error_wrong_num: str = "Пожалуйста, введите корректный диапазон (Должно быть два значения)."
    price_error_wrong_range: str = "Пожалуйста, введите корректный диапазон (Значения больше 0)."
    price_error_wrong_swap: str = 'Пожалуйста, введите корректный диапазон (Первое значение должно быть меньше второго).'
