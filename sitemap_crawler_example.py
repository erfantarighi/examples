import re

import requests
from bs4 import BeautifulSoup
import xmltodict

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0"
}

queue_pages = []
sitemap_links = []
musics = []


def print_links():
    url = "https://download1music.ir/sitemap_index.xml"
    a = xmltodict.parse(requests.get(url).text)
    for key, value in a.items():
        for key1, value1 in value.items():
            if key1 == 'sitemap':
                for item in value1:
                    if item['loc'] not in sitemap_links:
                        sitemap_links.append(item['loc'])
    for item in sitemap_links:
        a = xmltodict.parse(requests.get(item).text)
        for key, value in a.items():
            for key1, value1 in value.items():
                for item1 in value1:
                    try:
                        queue_pages.append(item1['loc'])
                    except:
                        pass
    for item in queue_pages:
        soup = BeautifulSoup(requests.get(item).content, "html.parser")
        for u in soup.findAll('a', href=re.compile('http.*\.mp3')):
            musics.append(u["href"])
            print(u["href"])
    print(len(musics))
