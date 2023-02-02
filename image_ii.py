import tensorflow as tf
import numpy as np


def compare_images(img1, img2):
    import excel
    img1 = excel.download_image(img1, 3)
    img2 = excel.download_image(img2, 4)
    img1 = tf.keras.preprocessing.image.load_img(img1)
    img2 = tf.keras.preprocessing.image.load_img(img2)
    img1 = tf.keras.preprocessing.image.img_to_array(img1)
    img2 = tf.keras.preprocessing.image.img_to_array(img2)
    img1 = tf.image.resize(img1, (224, 224))
    img2 = tf.image.resize(img2, (224, 224))
    img1 = np.array(img1)
    img2 = np.array(img2)
    model = tf.keras.applications.MobileNetV2(
        include_top=False, weights="imagenet", input_shape=(224, 224, 3)
    )
    features1 = model.predict(img1[tf.newaxis, ...])
    features2 = model.predict(img2[tf.newaxis, ...])
    comparison = tf.reduce_mean(tf.square(features1 - features2))
    print(comparison)
    return bool(comparison < 0.8)
