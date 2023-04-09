"""Entry point of project."""
from json import loads
from os import getenv
from re import match

from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message
from aiohttp import ClientSession, ClientResponse

REQUEST_PATTERN: str = (
        '^{\"dt_from\": \"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\", ' +
        '\"dt_upto\": \"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\", ' +
        '\"group_type\": \"(?P<group_type>hour|day|month)\"}$'
)
RESPONSE_TO_INVALID_REQUEST: str = (
        'Невалидный запрос. Пример запроса:\n' +
        '{"dt_from": "2022-09-01T00:00:00", ' +
        '"dt_upto": "2022-12-31T23:59:00", "group_type": "month"}'
)
ENDPOINT: str = 'http://fastapi_backend:8010/aggregate_payments'
MESSAGE_MAX_LENGTH: int = 4096
REDUSE_THE_SELECTION: str = (
        'Ответ превышает максимальную длину сообщения. ' +
        'Уменьшите выборку.'
)
dp: Dispatcher = Dispatcher(Bot(token=getenv('TELEGRAM_BOT_TOKEN')))


@dp.message_handler(commands=['start'])
async def welcome(message: Message):
    user_mention: str = message.from_user.get_mention(as_html=True)
    await message.answer(f'Hi {user_mention}!', parse_mode='HTML')


@dp.message_handler()
async def print_response_from_db(message: Message):
    if not match(REQUEST_PATTERN, message.text):
        return await message.answer(RESPONSE_TO_INVALID_REQUEST)

    async with ClientSession() as session:
        request: dict = loads(message.text)
        response: ClientResponse = await session.get(
            '{api}/{dt_from}/{dt_upto}/{group_type}'.format(
                api=ENDPOINT, **request,
            )
        )
    answer: str = await response.text()
    await message.answer(
        answer if len(answer) < MESSAGE_MAX_LENGTH else REDUSE_THE_SELECTION
    )


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
