import  requests
import bs4
import logging
import csv
from collections import namedtuple
from pprint import pprint
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("site")

InnerBlock = namedtuple('Block', 'title, price_usd, price_uah, date, url')
url = "https://auto.ria.com/uk/legkovie/audi/80/"

class Block(InnerBlock):

    def __str__(self):
        return f'{self.title}\t{self.price_usd}\t{self.price_uah}\t{self.date}\t{self.url}'

class Ria_parcer:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
            "Accept-Language": "ru"
        }

    def get_page(self, pages: int=None):
        params = {}
        list_cars = []
        if pages and pages > 1:
            html = (self.session.get(url)).text
            list_cars.append(self.get_blocks(html))
            for page in range(1, pages):
                print(f"Загрузка страницы {page} из {pages}...")
                html = (self.session.get(url, params={"page": page})).text
                list_cars.extend(self.get_blocks(html))
        else:
            html = self.session.get(url)
            list_cars.append(self.get_blocks(html))
        return list_cars
        #return html

    def get_blocks(self, html):
        out_list = []
        #text = self.get_page(pages=pages)
        soup = bs4.BeautifulSoup(html, 'lxml')
        container = soup.select("div.content-bar")
        for item in container:
            #pprint(item)
            block = self.parce_block(item=item)
            out_list.append(block)
            #print(out_list)
        return out_list

    def write_file(self, out_list):
        #print(out_list)
        with open("out_list.csv", "w", newline='') as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(["Заголовок", "Валюта", "Цена", "Дата публикации", "Ссылка"])
            for line in out_list:
                writer.writerow(
                    [line["title"], line["currency"], line["price_usd"], line["date"], line["url"]]
                )

    def parce_block(self, item):
        url_block = item.select_one('a.m-link-ticket')
        href = url_block.get('href').strip() # ссылка

        t_block = item.select_one("div.item.ticket-title")
        title = t_block.find('a', class_='address').text
        #print(title_block)
        #title = title_block.get('title') # заголовок объявления
        #print(title)
        #print(href)

        val = item.select_one('div.price-ticket')
        currency = val.get("data-main-currency")
        price_usd = val.get("data-main-price")
        #print(price_usd, currency)

        date_block = item.select_one("div.footer_ticket")
        if not date_block:
            logging.error(f"Не найден date_block в {href}")
            return
        else:
            date_info = date_block.text.strip()
            #print(date_info)

        result = {
            "title": title,
            "currency": currency,
            "price_usd": price_usd,
            "date": date_info,
            "url": href
        }
        return result


    def get_pages_count(self):
        html = self.session.get(url)
        #print(html.text)
        #html = self.get_page()
        soup = bs4.BeautifulSoup(html.text, "html.parser")
        page = soup.find_all("span", class_="page-item mhide")
        if page:
            self.pages = int(page[-1].text.strip())
            return self.pages
        else:
            return 1


def main():
    p = Ria_parcer()
    #pages = p.get_pages_count()
    #print(pages)
    d = p.get_page(2)
    #print(d)
    p.write_file(d)
    #print(pages)

if __name__ == '__main__':
    main()