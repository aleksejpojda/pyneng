import  requests
from bs4 import BeautifulSoup
import logging
from urllib.parse import urljoin
import csv
from datetime import date, time
from pprint import pprint
#import Telegram_send


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("site")

#URL = ""
#while not URL:
#    URL = input(
#        "Введита адресы ссылки нужного раздела\n"
#        "Для этого перейдите на нужную страницу, нажмите 'Show all' внизу страницы\n"
#        "и вставьте результат, скопированый с адресной строки браузера:"
#        )
FILE_NAME = '' #input(
#    "Введите имя файла для сохранения результата.\n"
#    "Файл должен иметь расширение CSV и будет сохранен в текущем каталоге\n"
#    "По умолчанию файл будет называться out.csv:"
#    )
if not FILE_NAME:
    FILE_NAME = f"Columbia{date.today()}.csv"
URL = "https://www.columbia.com/c/womens-jackets/"
HEADERS = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
            "Accept-Language": "ru", "accept": "*/*"
        }


def get_html(url, params=None):
    """загружаем страницу"""
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html):
    """парсим загруженную страницу"""
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all("div", class_="product-tile__wrapper")
    goods = []
    for item in items:
        if item.find("span", class_="discounted"):
            price = item.find("span", class_="discounted").get("content")
            if item.find("span", class_="strike-through"):
                old = item.find("span", class_="strike-through")
                old_price = "$" + old.find("span", class_="value").get("content")
        elif item.find("span", class_="value"):
            price = item.find("span", class_="value").get("content")
            old_price = None
        else:
            continue
        goods.append({
            "title": item.find("a", class_="link").get_text(strip=True),
            "link": urljoin(URL, (item.find("a", class_="link").get("href"))),
            "price": "$" + price,
            "old_price": old_price,
            "img": item.find("img", class_="tile__image--primary").get("data-src"),
        })
    print("Получено результатов:", len(goods))
    return goods


def parse():
    print("Начинаем работать")
    html = get_html(URL)
    if html.status_code == 200:
        out_list = get_content(html.text)
        write_file(FILE_NAME, out_list)
    else:
        logger.error(f"Не удалось загрузить страницу {URL}")
        return
    #return out_list


def write_file(file_name, out_list):
    with open(file_name, "w", newline='') as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["Название товара", "Цена", "Цена без скидки", "Ссылка", "Ссылка на изображение"])
        for line in out_list:
            writer.writerow(
                [line["title"], line["price"], line["old_price"], line["link"], line["img"]]
            )


if __name__ == '__main__':
    message = "Какое-то сообщение для людей"
    result = parse()
    #write_file(FILE_NAME, result)
    #Telegram_send.generate_text(result, message)