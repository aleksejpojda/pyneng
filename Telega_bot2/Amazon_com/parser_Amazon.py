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

URL = "https://www.amazon.com/s?bbn=16225020011&rh=n%3A7141123011%2Cn%3A16225020011%2Cn%3A1040664%2Cp_n_size_six_browse-vebin%3A4940398011&dc&fst=as%3Aoff&pf_rd_i=16225020011&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=2a239f2b-0318-4c5d-be33-9cc1f0eed9b3&pf_rd_r=D6XXPNYAK78V3WF5X6S2&pf_rd_s=merchandised-search-3&pf_rd_t=101&qid=1489098061&rnid=4940396011&ref=s9_acss_bw_cg_AEGFVN2E_1a1_w"
if not FILE_NAME:
    FILE_NAME = f"Amazon{date.today()}.csv"

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
    items = soup.find_all("div", class_='a-section')
    goods = []
    for item in items:
        #print(item)
        if item.find('a', class_='a-link-normal') and item.find('span', class_='a-size-base-plus') and item.find('img', class_='s-image'):
            link = urljoin(URL, item.find('a', class_='a-link-normal').get('href'))
            #print(link)
        #elif item.find('img', class_='s-image'):
            title = item.find('span', class_='a-size-base-plus').get_text()
            #print(title)
            img = item.find('img', class_='s-image').get('src')
            price = 'Цену уточняйте, зависит от размера вещи'
            old_price = ''
            #print(img)
            if item.find('span', class_='a-price'):
                if item.find('span', class_='a-price').get('data-a-size') == 'l':
                    price = item.find('span', class_='a-offscreen').get_text()
                    if item.find('span', class_='a-price').get('data-a-size') == 'b':
                        old_price = item.find('span', class_='a-offscreen').get_text()
                        #print('old price ', old_price)
                    #else: old_price = ''

            goods.append({
                        'title': title,
                        'price': price,
                        'old_price': old_price,
                        'link': link,
                        'img': img
                    })
    #print(goods)
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
