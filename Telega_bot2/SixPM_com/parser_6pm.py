import  requests
from bs4 import BeautifulSoup
import logging
from urllib.parse import urljoin
import csv
from pprint import pprint
from datetime import date


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("site")


#URL = ""
#while not URL:
#    URL = input(
#        "Введита адресы ссылки нужного раздела. Для этого перейдите в нужный раздел\n"
#        "и вставьте результат, скопированый с адресной строки браузера:"
#        )

FILE_NAME = ''#input(
#    "Введите имя файла для сохранения результата.\n"
#    "Файл должен иметь расширение CSV и будет сохранен в текущем каталоге\n"
#    "По умолчанию файл будет называться out.csv:"
#    )

URL = "https://www.6pm.com/women-clothing/CKvXAcABAeICAgEY.zso?s=isNew/desc/goLiveDate/desc/recentSalesStyle/desc/"
if not FILE_NAME:
    FILE_NAME = f"SixPM{date.today()}.csv"

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
    pagination_block = soup.find("span", class_="Tu-z")
    #print(pagination_block)
    #pagination = pagination_block.find_all("a", class_=None)
    if pagination_block.find_all("a", class_=None):
        return int(pagination_block.find_all("a", class_=None)[-1].get_text())

    else: return 0


def get_content(html):
    """парсим загруженную страницу"""
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all("article")
    goods = []
    for item in items:
        if item.get("data-style-id"):
            if 'On sale for' in item.get_text():
                title = item.get_text().split("On sale for")[0].strip()
                price = item.get_text().split("On sale for")[1].split('MSRP')[0].strip().strip('.')
                old_price = item.get_text().split("On sale for")[1].split('MSRP')[1].strip().split('..')[0]
            else:
                title = item.get_text().split('$')[0]
                price = "$" + item.get_text().split('$')[1].split('. ')[0]
                old_price = ''
            goods.append({
                'title': title,
                'price': price,
                'old_price': old_price,
                'link': urljoin(URL, item.find('a').get("href")),
                'img': item.find('meta', class_=None).get("content")
            })
    return goods


def parse():
    print("Начинаем работать")
    html = get_html(URL)
    if html.status_code == 200:
        goods = []
        #page_count = get_pages_count(html.text)
        goods.extend(get_content(html.text))
        page_count = 0  #для отладки, загружать только 1 страницу
        if page_count > 1:
            for page in range(1, page_count + 1):
                print(f"Парсинг страницы {page} из {page_count} страниц...")
                html = get_html(URL, params={"p": page})
                goods.extend(get_content(html.text))
        else:
            write_file(FILE_NAME, goods)
    else:
        logger.error(f"Не удалось загрузить страницу {URL}")
        return
    print("Получено результатов:", len(goods))
    write_file(FILE_NAME, goods)
    return goods


def write_file(file_name, out_list):
    with open(file_name, "w", newline='') as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["title", "price", "old_price", "link", "img"])
        for line in out_list:
            writer.writerow(
                [line["title"], line["price"], line["old_price"], line["link"], line["img"]]
                            )


if __name__ == '__main__':
    message = "Какое-то сообщение для людей"
    result = parse()
    pprint(result)
    write_file(FILE_NAME, result)
    #Telegram_send.generate_text(result, message)
