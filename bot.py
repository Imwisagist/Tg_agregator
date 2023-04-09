"""Entry point of project."""
from json import loads
from os import getenv
from re import match

from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv

import utils

load_dotenv()
dp: Dispatcher = Dispatcher(Bot(
    token=getenv('TELEGRAM_TOKEN'), parse_mode='HTML')
)
pattern: str = ("^{\"dt_from\": \"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:" +
                "\d{2}\", \"dt_upto\": \"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d" +
                "{2}\", \"group_type\": \"(?P<group_type>hour|day|month)\"}$")


@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    user_mention: str = message.from_user.get_mention(as_html=True)
    await message.answer(f"Hi {user_mention}!")


@dp.message_handler()
async def print_response_from_db(message: types.Message):
    if match(pattern, message.text):
        request: dict = loads(message.text)
        response: dict = utils.aggregate_payments(**request)
        await message.answer(str(response).replace('\'', '\"'))
    else:
        await message.answer('Невалидный запрос. Пример запроса:\n{"dt_from"' +
                             ': "2022-09-01T00:00:00", "dt_upto":' +
                             ' "2022-12-31T23:59:00", "group_type": "month"}')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
