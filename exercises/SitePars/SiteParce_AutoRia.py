import  requests
import bs4
import logging
import csv
from collections import namedtuple
from pprint import pprint

InnerBlock = namedtuple('Block', 'title, price_usd, price_uah, date, url')

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

    def get_page(self, page: int=None):
        params = {
            'size': 10,
            'user': 1,
        }
        if page and page > 1:
            params['p'] = page
        url = "https://auto.ria.com/uk/legkovie/bmw/x5/"
        r = self.session.get(url, params=params)
        return r.text

    def get_blocks(self):
        text = self.get_page(page=2)
        soup = bs4.BeautifulSoup(text, 'lxml')
        container = soup.select("div.content-bar")
        for item in container:
            #pprint(item)
            block = self.parce_block(item=item)
            #print(block)

    def parce_block(self, item):
        url_block = item.select_one('a.m-link-ticket')
        href = url_block.get('href') # ссылка
        #if href:
        #    print(href) # = 'https://auto.ria.com' + href
        #else:
        #    herf = None

        t_block = item.select_one("div.item.ticket-title")
        title_block = t_block.select_one('a.address')
        title = title_block.get('title') # заголовок объявления

        val = item.select_one('div.price-ticket')
        #print(val.text)
        price_usd = val.text.split("$")[0]
        price_uah = val.text.split("$")[1][3:]
        print(price_uah)
        #valuta = item.select_one("span.bold.green.size22")
        #price = item.select_one("span.bold.green.size22")
        #price = price.text + "$"
        #print(price, title, href)



def main():
    p = Ria_parcer()
    p.get_blocks()

if __name__ == '__main__':
    main()