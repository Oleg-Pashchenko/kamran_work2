import db
from scrapers import unas, ozon, wildberries


def main():
    print("Program started!")
    unas.load_data()
    print("Loaded data from Unas!")
    while True:
        data = db.get_new_article()
        id, article, name, img = data[0], data[1], data[2], data[3]
        words_count = int(open('dependencies/count', 'r').read())
        id_ozon, photo_ozon, ozon_names = ozon.scrape(name, words_count)
        id_wildberries, photo_wildberries, wildberries_names = wildberries.scrape(name, words_count)
        print(article, name, img, 'ozon', id_ozon, photo_ozon, 'parsed', ozon_names)
        db.write_row(article, name, img, 'ozon', id_ozon, photo_ozon, 'parsed', ozon_names)
        db.write_row(article, name, img, 'wildberries', id_wildberries, photo_wildberries, 'parsed',
                     wildberries_names)
        db.delete_row_by_id(id)


if __name__ == '__main__':
    main()
