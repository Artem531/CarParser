import requests
from bs4 import BeautifulSoup
import threading

class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException("Функция заняла слишком много времени")

def run_with_timeout(func, timeout_seconds):
    result = [None]
    exception = [None]

    def target():
        try:
            result[0] = func()
        except Exception as e:
            exception[0] = e

    thread = threading.Thread(target=target)
    thread.start()
    thread.join(timeout_seconds)

    if thread.is_alive():
        raise TimeoutException("Функция заняла слишком много времени")
    if exception[0] is not None:
        raise exception[0]

    return result[0]

def parse_car_page(url, session, headers):
    """
    Парсит страницу автомобиля и возвращает информацию о нем в виде словаря.
    """
    #response = session.get(url, headers=headers)
    get_with_timeout = lambda: session.get(url, headers=headers)
    response = run_with_timeout(get_with_timeout, 5)

    soup = BeautifulSoup(response.text, 'html.parser')

    # Базовая информация об автомобиле
    base_info_keys = ["Stanje:", "Marka", "Model", "Godište", "Kilometraža", "Karoserija", "Gorivo", "Atestiran"]
    base_info = {}
    for key in base_info_keys:
        element = soup.find("div", string=key)
        if element:  # Проверка, что элемент найден
            next_div_text = element.find_next("div").text.strip() if element.find_next("div") else "N/A"
            base_info[key.strip(':')] = next_div_text

    # Дополнительная информация об автомобиле
    dodatne_informacije = {}
    dividers = soup.find_all("div", class_="divider")
    for divider in dividers:
        key = divider.find("div", class_="uk-width-1-2").text.strip()
        value_div = divider.select_one(".uk-width-1-2.uk-text-bold")
        if value_div:
            value = value_div.text.strip()
            dodatne_informacije[key] = value

    # Объединяем базовую и дополнительную информацию в один словарь
    car_info = {**base_info, **dodatne_informacije}

    return car_info

def main():
    # URL страницы, которую нужно распарсить
    url = 'https://www.polovniautomobili.com/auto-oglasi/23258824/lada-niva-lada-niva-4x4'

    headers = {
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

    # Использование функции для парсинга страницы
    car_details = parse_car_page(url, headers)

    # Вывод информации об автомобиле
    for key, value in car_details.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()


