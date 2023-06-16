from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import requests
import json
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
        filtered = json.loads(kakashki)
        print (filtered['status'])
        status = filtered['status']
        if status == True:
            filtered = filtered['data']
            filtered = filtered['file']
            filtered = filtered['url']
            shorten = filtered['short']
            filtered = filtered['full']
            endpoint = 'https://clck.ru/--'
            url = (shorten)
            resp = requests.get(endpoint, params = {'url' : url})
            clckrulink = resp.text
            print (clckrulink)
            print (filtered)
            print (shorten)
            await message.reply('Short: '+ shorten+'\n'+'Full: '+filtered+ '\n'+'clck.ru: '+clckrulink)
        else:
            errcode = json.loads(kakashki)
            errcode = errcode['error']
            errcode = errcode['message']
            await message.reply(errcode)
            
if __name__ == '__main__':
    print('bot started!')
    executor.start_polling(dp)
#bot by koke228 :D