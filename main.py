import db
import image_ii
from scrapers import unas, ozon, wildberries


def main():
    print("Program started!")
    # unas.load_data()
    print("Loaded data from Unas!")
    while True:
        data = db.get_new_article()
        id, article, name, img = data[0], data[1], data[2], data[3]
        words_count = int(open("dependencies/count", "r").read())
        try:
            # Scrape block start
            id_ozon, photo_ozon, ozon_names = ozon.scrape(name, words_count)
            id_wildberries, photo_wildberries, wildberries_names = wildberries.scrape(name, words_count)
            #  Scrape block end

            # AI block start
            ozon_photos_to_write, wildberries_photos_to_write, ozon_names_to_write, wildberries_names_to_write, \
                ozon_ids_to_write, wildberries_ids_to_write = [], [], [], [], [], []
            for photo in range(len(photo_ozon)):
                if image_ii.compare_images(photo_ozon[photo], img):
                    ozon_photos_to_write.append(photo_ozon[photo])
                    ozon_names_to_write.append(ozon_names[photo])
                    ozon_ids_to_write.append(id_ozon[photo])

            for photo in range(len(photo_wildberries)):
                if image_ii.compare_images(photo_wildberries[photo], img):
                    wildberries_photos_to_write.append(photo_wildberries[photo])
                    wildberries_names_to_write.append(wildberries_names[photo])
                    wildberries_ids_to_write.append(id_wildberries[photo])
            # AI block end

            # Write block start
            db.write_row(article, name, img, "ozon", ozon_ids_to_write, ozon_photos_to_write, "parsed",
                         ozon_names_to_write)
            db.write_row(article, name, img, "wildberries", wildberries_ids_to_write, wildberries_photos_to_write,
                         "parsed",
                         wildberries_names_to_write)
            # Write block end
            print('success')
            db.delete_row_by_id(id)
        except:
            db.delete_row_by_id(id)

if __name__ == "__main__":
    main()
