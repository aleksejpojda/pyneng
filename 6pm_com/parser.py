import  requests
from bs4 import BeautifulSoup
import logging
from urllib.parse import urljoin
import csv
import Telegram_send
from pprint import pprint


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("site")


URL = ""
while not URL:
    URL = input(
        "Введита адресы ссылки нужного раздела. Для этого перейдите в нужный раздел\n"
        "и вставьте результат, скопированый с адресной строки браузера:"
        )

FILE_NAME = input(
    "Введите имя файла для сохранения результата.\n"
    "Файл должен иметь расширение CSV и будет сохранен в текущем каталоге\n"
    "По умолчанию файл будет называться out.csv:"
    )

#URL = "https://www.6pm.com/women-clothing/CKvXAcABAeICAgEY.zso?s=isNew/desc/goLiveDate/desc/recentSalesStyle/desc/"
if not FILE_NAME:
    FILE_NAME = "out.csv"

HEADERS = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
            "Accept-Language": "ru", "accept": "*/*"
        }


def get_html(url, params=None):
    """загружаем страницу"""
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_pages_count(html):
    soup = BeautifulSoup(html, "html.parser")
    pagination_block = soup.find("span", class_="Lr-z")
    pagination = pagination_block.find_all("a", class_=None)[-1].get_text()
    if pagination:
        return int(pagination)
    else: return 0


def get_content(html):
    """парсим загруженную страницу"""
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all("article", class_="yl-z")

    goods = []
    for item in items:
        text = item.find("a", class_="Ej-z").get_text()
        title = text.split(" On sale for ")[0]
        if item.find("dd", class_="Ql-z"):
            msrp = item.find("dd", class_="Ql-z").text.split(":")[0][0:-4]
        else: msrp = "no MSRP price"
        goods.append({
            "link": urljoin(URL, (item.find("a", class_="Ej-z").get("href"))),
            "title": title,
            "price": item.find("span", class_="Pl-z").get_text(),
            "price_msrp": msrp,
            "img": item.find("meta", class_=None).get("content")
        })
    return goods


def parse():
    print("Начинаем работать")
    html = get_html(URL)
    if html.status_code == 200:
        goods = []
        page_count = get_pages_count(html.text)
        goods.extend(get_content(html.text))
        #page_count = 0  #для отладки, загружать только 1 страницу
        if page_count > 1:
            for page in range(1, page_count + 1):
                print(f"Парсинг страницы {page} из {page_count} страниц...")
                html = get_html(URL, params={"p": page})
                goods.extend(get_content(html.text))
            print("Получено результатов:", len(goods))
        else:
            print("Получено результатов:", len(goods))
            return goods
    else:
        logger.error(f"Не удалось загрузить страницу {URL}")
        return
    return goods


def write_file(file_name, out_list):
    with open(file_name, "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["Title", "Price", "Price MSRP", "Link", "Image link"])
        for line in out_list:
            writer.writerow(
                [line["title"], line["price"], line["price_msrp"], line["link"], line["img"]]
            )


if __name__ == '__main__':
    result = parse()
    write_file(FILE_NAME, result)
    Telegram_send.generate_text(result)
