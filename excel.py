import requests
from PIL import Image


def download_image(link: str, index):
    filename = f'dependencies/{index}.jpg'
    img_data = requests.get(link).content
    with open(filename, 'wb') as handler:
        handler.write(img_data)
    handler.close()

    image = Image.open(filename)
    sunset_resized = image.resize((250, 250))
    sunset_resized.save(filename)
    return filename


def read_file(filename: str):
    import pandas as pd
    df = pd.read_excel(filename)
    result = []
    for _, row in df.iterrows():
        values = row.values
        article = str(values[0])
        if not article.isdigit():
            continue
        name = values[1]
        image = f"https://unas.ru/scripts/images.php?product={article}"
        result.append([article, name, image])
    return result


