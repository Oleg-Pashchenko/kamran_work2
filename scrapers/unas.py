import requests
from bs4 import BeautifulSoup

import db
import excel

headers = {
    "User-Agent": "python-requests/2.24.0",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "*/*",
    "Connection": "keep-alive",
}


def load_data():
    print("Loading data")
    response = requests.get("https://unas.ru/personal/price-lists/", headers=headers)
    soup = BeautifulSoup(response.text, features="lxml")
    cards = soup.find_all("div", {"class": "item_block lg col-lg-20 col-md-4 col-xs-6"})
    idx = 0
    for card in cards:
        if card.find('img').get('alt') == 'Семена и посадочный материал':
            continue
        idx += 1
        print(f"Loaded data {idx}/{len(cards)}")
        download_link = "https://unas.ru/" + card.find("a").get("href")
        response = requests.get(download_link)
        output = open("dependencies/test.xlsx", "wb")
        output.write(response.content)
        output.close()
        data = excel.read_file("dependencies/test.xlsx")
        db.write_unas_data(data)
