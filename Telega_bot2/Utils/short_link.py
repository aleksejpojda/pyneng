import urllib
import requests
import json

"""
тут получаем короткую ссылку
"""

key = '22ac2576e27cad74d77acbf204dce087d19ea'

def short_url(url):
    link = urllib.parse.quote(f'{url}')
    r = requests.get('http://cutt.ly/api/api.php?key={}&short={}'.format(key, link))
    return json.loads(r.text)['url']['shortLink']


if __name__ == '__main__':
    print(short_url("https://privatbank.ua"))