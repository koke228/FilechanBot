from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import requests

from config import TOKEN


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Send me any file and i upload it to filechan.org")

@dp.message_handler(content_types='document')
async def unknown_message(message: types.Message):
    if document := message.document:
        await document.download(
        destination_file=f'{document.file_name}')
        url = 'https://api.filechan.org/upload'
        fp = open(document.file_name, 'rb')
        files = {'file': fp}
        resp = requests.post(url, files=files)
        fp.close()
        print(resp.text)
        kakashki = resp.text
        kakashki = kakashki.replace('\/', '/')
        await message.reply(kakashki)

if __name__ == '__main__':
    print('bot started!')
    executor.start_polling(dp)
#bot by koke228 :D