from aiogram import types, executor, Dispatcher, Bot
import requests

bot = Bot("5264280645:AAFXeIE_Iu-d6ENQZSATJ1g3GMuE_XLH7Fo")
dp = Dispatcher(bot)


# команда /start
@dp.message_handler(commands=['start'])
async def start(message: types.message):
    await bot.send_message(message.chat.id, """
Привет! Я бот, который позволит быстро находить нужные товары на <b><a href="https://www.wildberries.ru/">WildBerries</a></b>

Для того, чтобы я отправил тебе товар, введи в поле его название...""",
                           parse_mode="html", disable_web_page_preview=1)


# parser
@dp.message_handler(content_types=['text'])
async def parser(message: types.message):

    url = f"https://www.wildberries.ru/search/tags?searchQuery={message.text}isEmpty=false"
    try:
        response = requests.get(url)
    except:
        await bot.send_message(message.chat.id, "Ошибка получения ответа от сервера")

    if response.status_code != 200:
        await bot.send_message(message.chat.id, "Ошибка получения ответа от сервера")

    response = response.json()
    tagsViewModels = response['value']['topTags']['tagsViewModels']

    for item in tagsViewModels:
        await bot.send_message(message.chat.id,
                               f'{item["text"]}\n<a href="https://www.wildberries.ru{item["href"]}">Просмотреть</a>',
                               parse_mode="html",
                               disable_web_page_preview=True)


executor.start_polling(dp)
