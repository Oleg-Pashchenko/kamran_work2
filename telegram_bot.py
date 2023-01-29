import aiogram
from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ContentType, InputFile, InputMediaPhoto
import db
import excel

API_TOKEN = '5302029732:AAENrrdfY1-NprXCUd26UA1vbpXy3VUumk8'

bot = aiogram.Bot(token=API_TOKEN)
dp = aiogram.Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_message(message):
    kb = [
        [
            types.KeyboardButton(text="Обработать"),
            types.KeyboardButton(text="Статистика"),
        ],
        [
            types.KeyboardButton(text="Сменить лимит слов в запросе")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите способ подачи"
    )
    await message.answer("Привет!\nЗдесь ты можешь обработать заявки!", reply_markup=keyboard)


@dp.message_handler(lambda message: "обработать" in message.text.lower())
async def send_photos(message):
    try:
        position_data = db.get_unchecked_position()
        print(position_data)
        img1 = excel.download_image(position_data[3], 1)
        img2 = excel.download_image(position_data[6], 2)
        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton("✔️", callback_data=f"check_{position_data[0]}")
        button2 = InlineKeyboardButton("❌", callback_data=f"cross_{position_data[0]}")
        markup.add(button1, button2)
        photo1 = InputMediaPhoto(open(img1, 'rb'), caption='Unas')
        photo2 = InputMediaPhoto(open(img2, 'rb'), caption=position_data[4])
        await bot.send_media_group(message.chat.id, media=[photo1, photo2])
        await bot.send_message(message.chat.id, text=position_data[2] + "\n\n" + position_data[8], reply_markup=markup)

    except Exception as e:
        print(e)
        await message.answer("Ошибка при отправке позиции!")


@dp.callback_query_handler(lambda m: 'check' in m.data)
async def add_to_execute(data):
    db.update_status(int(data.data.split('_')[1]), 'approved')
    await send_photos(data.message)


@dp.callback_query_handler(lambda m: 'cross' in m.data)
async def remove_from_order(data):
    db.update_status(int(data.data.split('_')[1]), 'disliked')
    await send_photos(data.message)


@dp.message_handler(lambda m: 'статистика' in m.text.lower())
async def get_stats(message):
    stats = db.get_stats()
    await message.answer(
        f"Всего позиций: {stats[0]}\nНе обработано: {stats[1]}\nНе проверено: {stats[2]}\nСогласовано: {stats[3]}\nНе согласовано: {stats[4]}")


@dp.message_handler(lambda m: 'сменить лимит слов в запросе' in m.text.lower())
async def change_words_count_limit(message):
    await message.answer("Напишите лимит 10 (где 10 - число слов)")


@dp.message_handler(lambda m: 'лимит' in m.text.lower())
async def change_limit(message):
    message.text = message.text.split()
    if len(message.text) != 2:
        await message.answer("Некорректный формат ввода")
    elif not message.text[1].isdigit():
        await message.answer("Введено не число!")
    else:
        f = open('dependencies/count', 'w')
        f.write(message.text[1])
        f.close()
        await message.answer("Изменение произошло успешно!")


@dp.message_handler(lambda m: m.text == '/file')
async def send_accepted(message):
    d = db.get_approved()
    f = open('dependencies/file.txt', 'w')
    for i in d:
        f.write(f"{i[1]}(unas) - {i[5]}({i[4]})\n")
    f.close()
    await bot.send_document(message.chat.id, open('dependencies/file.txt', 'rb'))


if __name__ == '__main__':
    aiogram.executor.start_polling(dp, skip_updates=True)
