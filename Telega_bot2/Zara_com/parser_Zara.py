import  requests
from bs4 import BeautifulSoup
import logging
from urllib.parse import urljoin
import csv
from datetime import date
import time
from pprint import pprint
#import Telegram_send


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("site")


FILE_NAME = f"Zara{date.today()}.csv"
URL = [
       "https://www.zara.com/us/en/woman-new-in-l1180.html?v1=2026572&regionGroupId=1&page=1",
       'https://www.zara.com/us/en/woman-new-in-l1180.html?v1=2026572&regionGroupId=1&page=2:1',
       "https://www.zara.com/us/en/woman-new-in-l1180.html?v1=2026572&regionGroupId=1&page=3:1",

       ]
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
    items = soup.find_all("li", class_="product-grid-block-dynamic")
    goods = []
    for item in items:
        if not item.find("span", class_=None):
            continue
        link = item.find("a", class_='product-link').get("href")
        html_img = get_html(link).text
        soup_img = BeautifulSoup(html_img, "html.parser")
        print(soup_img.find('source', class_=None).get("srcset").split()[-2])
        img = soup_img.find('source', class_=None).get("srcset").split()[-2]
        goods.append({
                "title": item.find("span", class_=None).get_text(),
                'link': link,
                "price": item.find("span", class_='price-current__amount').get_text(),
                "img": img
                #"img": item.find('img', class_='media-image__image').get('src'),
        })

    print("Получено результатов:", len(goods))
    return goods

def parse():
    print("Начинаем работать")
    result = []
    for link in URL:
        html = get_html(link)
        #time.sleep(5)
        if html.status_code == 200:
            out_list = get_content(html.text)
            result.extend(out_list)
        else:
            logger.error(f"Не удалось загрузить страницу {URL}")
            return
    write_file(FILE_NAME, result)

def unique_list_dict(out_list):
    result = []
    for line in out_list:
        if line not in result:
            result.append(line)
        else: print(line['title'], "удален")
    return result

def write_file(file_name, out_list):
    out_list = unique_list_dict(out_list)
    with open(file_name, "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["title", "price", "link", "img"])
        for line in out_list:
            writer.writerow(
                [line["title"], line["price"], line["link"], line["img"]]
            )

if __name__ == '__main__':
    parse()