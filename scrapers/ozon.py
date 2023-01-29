import time

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options


def scrape(q: str, c: int):
    if len(q.split()) > c:
        q = ' '.join(q.split()[:c])
    try:
        result_id = []
        result_name = []
        result_photo = []
        options = Options()
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        browser = webdriver.Chrome('../dependencies/chromedriver', options=options)
        browser.get(f'https://www.ozon.ru/search/?text={q}&from_global=true')
        data = BeautifulSoup(browser.page_source, features='lxml')
        browser.close()
        data = data.find_all('div', {'class': 'lm1 ml1'})
        for i in data:
            result_id.append(i.find('img').get('src').split('/')[-1].split('.')[0])
            result_name.append(i.find('div', {'class': 'l2m'}).find('a').find('span').text)
            result_photo.append(i.find('img').get('src'))
        return result_id, result_photo, result_name
    except Exception as e:
        print(e)
        return [], [], []
import time

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options


def scrape(q: str, c: int):
    if len(q.split()) > c:
        q = ' '.join(q.split()[:c])
    try:
        result_id = []
        result_name = []
        result_photo = []
        options = Options()
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        browser = webdriver.Chrome('../dependencies/chromedriver', options=options)
        browser.get(f'https://www.ozon.ru/search/?text={q}&from_global=true')
        data = BeautifulSoup(browser.page_source, features='lxml')
        browser.close()
        data = data.find_all('div', {'class': 'lm1 ml1'})
        for i in data:
            result_id.append(i.find('img').get('src').split('/')[-1].split('.')[0])
            result_name.append(i.find('div', {'class': 'l2m'}).find('a').find('span').text)
            result_photo.append(i.find('img').get('src'))
        return result_id, result_photo, result_name
    except Exception as e:
        print(e)
        return [], [], []
