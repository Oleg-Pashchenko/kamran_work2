from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import lxml  # noqa: F401

def scrape(q: str, c: int):
    if len(q.split()) > c:
        q = " ".join(q.split()[:c])
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
        browser = webdriver.Chrome("../dependencies/chromedriver", options=options)
        browser.get(f"https://www.ozon.ru/search/?text={q}&from_global=true")
        with open("html.html", "w") as f:
            f.write(browser.page_source)
        data = BeautifulSoup(browser.page_source, features="lxml")
        browser.close()
        cards = data.find_all("div", {'class': "x1j xj2"})
        for i in cards:
            result_id.append(i.find("img").get("src").split("/")[-1].split(".")[0])
            result_name.append(i.find_all('a')[-1].find('span').text.strip())
            result_photo.append(i.find("img").get("src"))
        return result_id, result_photo, result_name
    except Exception as e:
        print(e, "err")
        return [], [], []

