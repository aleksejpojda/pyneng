import requests
import bs4
import logging
import collections
from urllib.parse import urljoin
import csv
from sys import argv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("site")

link = argv[1]

ParceResult = collections.namedtuple(
    "ParceResult", (
        "brand_name",
        "goods_name",
        "price",
        "url",
    ),
)

HEADERS = (
    "Бренд",
    "Товар",
    "ЦЕНА",
    "Ссылка",
)

class Client:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
                                "Accept-Language": "ru"
                                }
        self.result = []

    def load_page(self):
        url = link #"https://www.wildberries.ru/catalog/elektronika/avtoelektronika"
        res = self.session.get(url=url)
        res.raise_for_status()
        return res.text

    def parce_page(self, text: str):
        soup = bs4.BeautifulSoup(text, "lxml")
        container = soup.select("div.product-card__wrapper")
        for block in container:
            self.parce_block(block=block)

    def parce_block(self, block):
        #logger.info(block)
        #logger.info("="*50)
        url_block = block.select_one("a.product-card__main")
        if not url_block:
            logger.error("No URL-block")
            return

        url = url_block.get("href")
        #base = "https://www.wildberries.ru/catalog/elektronika/avtoelektronika"
        url = urljoin(link, url)
        if not url:
            logger.error("No 'href' in URL-block")
            return

        name_block = block.select_one("div.product-card__brand-name")
        if not name_block:
            logger.error(f"No name_block on {url}")
            return

        brand_name = name_block.select_one("strong.brand-name")
        if not brand_name:
            logger.error(f"No brand_name on {url}")
            return
        else: brand_name = brand_name.text.replace("/", "").rstrip()

        good_name = name_block.select_one("span.goods-name")
        if not good_name:
            logger.error(f"No good_name on {url}")
            return
        else: good_name = good_name.text

        price_block = block.select_one("div.product-card__price")
        if not price_block:
            logger.error(f"No price_block on {url}")
            return

        price = price_block.select_one("span.lower-price")
        if not price:
            price = price_block.select_one("ins.lower-price")
            if not price:
                logger.error(f"No price on {url}")
                return
            else:
                price = price.text.replace("\u20bd", "")
                price = f"{price}руб."
        else:
            price = price.text.replace("\u20bd", "")
            price = f"{price}руб."


        logger.debug("%s, %s, %s, %s", url, brand_name, good_name, price)
        logger.debug("*"*50)

        self.result.append(ParceResult(
            url = url,
            brand_name = brand_name,
            price = price,
            goods_name = good_name
        ))

    def save_result(self):
        path = "C:/Users/dz220883pap/PycharmProjects/pyneng/exercises/SitePars/result.csv"
        with open(path, "w") as f:
            writer = csv.writer(f, quoting = csv.QUOTE_MINIMAL)
            writer.writerow(HEADERS)
            for line in self.result:
                writer.writerow(line)


    def run(self):
        text = self.load_page()
        self.parce_page(text=text)
        logger.info(f"Получили {len(self.result)} результатов")
        self.save_result()

if __name__ == '__main__':
    parser = Client()
    parser.run()