import requests


def scrape(q: str, c: int):
    if len(q.split()) > c:
        q = ' '.join(q.split()[:c])
    try:
        url = f'https://search.wb.ru/exactmatch/ru/common/v4/search?appType=1&couponsGeo=12,7,3,6,5,18,21&curr=rub&dest=-1216601,-337422,-1114902,-1198055&emp=0&lang=ru&locale=ru&pricemarginCoeff=1.0&query={q}&reg=0&regions=80,64,83,4,38,33,70,68,69,86,30,40,48,1,66,31,22&resultset=catalog&sort=popular&spp=0&suppressSpellcheck=false'
        answer_ids = []
        answer_photos = []
        answer_names = []
        r = requests.get(url).json()
        for i in r['data']['products'][:10]:
            if len(str(i['id'])) == 9:
                vol = str(i['id'])[:4]
            else:
                vol = str(i['id'])[:3]

            for j in range(1, 10):
                photo_url = f'https://basket-0{j}.wb.ru/vol{vol}/part{str(i["id"])[:5]}/{i["id"]}/images/c516x688/1.jpg'
                res = requests.get(photo_url)
                if res.status_code == 200:
                    answer_ids.append(i['id'])
                    answer_names.append(i['name'])
                    answer_photos.append(photo_url)
                    break
        return answer_ids, answer_photos, answer_names
    except Exception as e:
        print(e)
        return [], [], []

