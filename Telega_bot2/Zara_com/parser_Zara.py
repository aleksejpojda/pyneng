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

URL_NEW = [
        "https://www.zara.com/us/en/woman-new-in-l1180.html?v1=2026572&regionGroupId=1&page=1",
        "https://www.zara.com/us/en/man-new-in-l711.html?v1=2032934&regionGroupId=1&page1",
        #"https://www.zara.com/us/en/kids-girl-new-in-l391.html?v1=2013776&regionGroupId=1",
        #"https://www.zara.com/us/en/kids-boy-new-in-l228.html?v1=2020007&regionGroupId=1",
        #"https://www.zara.com/us/en/kids-babygirl-new-in-l127.html?v1=2021136&regionGroupId=1",
        #"https://www.zara.com/us/en/kids-babyboy-new-in-l43.html?v1=2021725&regionGroupId=1",
        #"https://www.zara.com/us/en/kids-accessories-new-in-l5256.html?v1=2090283&regionGroupId=1",
        #"https://www.zara.com/us/en/home-new-in-l2086.html?v1=2027170&regionGroupId=1",
        #"https://www.zara.com/us/en/woman-special-prices-l1314.html?v1=2026296&regionGroupId=1&page=1",
        #"https://www.zara.com/us/en/woman-special-prices-l1314.html?v1=2026296&regionGroupId=1&page=2",
        #"https://www.zara.com/us/en/man-special-prices-l806.html?v1=2032371&regionGroupId=1&page=1",
        #"https://www.zara.com/us/en/man-special-prices-l806.html?v1=2032371&regionGroupId=1&page=2",
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
    if soup.find_all("li", class_="product-grid-block-dynamic"):
        items = soup.find_all("li", class_="product-grid-block-dynamic")
    elif soup.find_all("li", class_="product-grid-product"):
        items = soup.find_all("li", class_="product-grid-product")
    goods = []
    for item in items:
        if not item.find("span", class_=None):
            continue
        link = item.find("a", class_='product-link').get("href")
        #print(link)
        html_img = get_html(link).text
        soup_img = BeautifulSoup(html_img, "html.parser")
        #print(soup_img.find('source', class_=None).get("srcset").split()[0])
        img = soup_img.find('source', class_=None).get("srcset").split()[0]
        if item.find("span", class_="price-old__amount"):
            old_price = item.find("span", class_="price-old__amount").get_text()
        else:
            old_price = ''
        if not item.find("span", class_='price-current__amount'):
            continue
        goods.append({
                "title": item.find("span", class_=None).get_text(),
                'link': link,
                "price": item.find("span", class_='price-current__amount').get_text(),
                'old_price': old_price,
                "img": img
        })
    print("Получено результатов:", len(goods))
    return goods


def parse():
    print("Начинаем работать")
    URL = URL_NEW
    #file_name = f'{FILE_NAME}n.csv'
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
        #else: print(line['title'], "удален")
    return result

def write_file(file_name, out_list):
    out_list = unique_list_dict(out_list)
    with open(file_name, "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["title", "price", "old_price", "link", "img"])
        for line in out_list:
            writer.writerow(
                [line["title"], line["price"], line['old_price'], line["link"], line["img"]]
            )

if __name__ == '__main__':
    parse()

