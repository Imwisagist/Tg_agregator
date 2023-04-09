"""
0)Ваш алгоритм должен принимать на вход:
Дату и время старта агрегации в ISO формате (далее dt_from)
Дату и время окончания агрегации в ISO формате (далее dt_upto)
Тип агрегации (далее group_type). Типы агрегации могут быть следующие: hour, day, month. То есть группировка всех данных за час, день, неделю, месяц.

Пример входа:
{"dt_from": "2022-09-01T00:00:00", "dt_upto": "2022-12-31T23:59:00", "group_type": "month"}


1)Комментарий к входным данным: вам необходимо агрегировать выплаты с 1 сентября 2022 года по 31 декабря 2022 года, тип агрегации по месяцу

На выходе ваш алгоритм формирует ответ содержащий:
Агрегированный массив данных (далее dataset)
Подписи к значениям агрегированного массива данных в ISO формате (далее labels)

Пример ответа:
{"dataset": [5906586, 5515874, 5889803, 6092634], "labels": ["2022-09-01T00:00:00", "2022-10-01T00:00:00", "2022-11-01T00:00:00", "2022-12-01T00:00:00"]}


2)После разработки алгоритма агрегации, вам необходимо создать телеграм бота, который будет принимать
от пользователей текстовые сообщения содержащие JSON с входными данными и отдавать агрегированные данные
в ответ. Посмотрите @rlt_testtaskexample_bot - в таком формате должен работать и ваш бот.

Ваш telegram id - 848561520
"""

from datetime import datetime as dt, timedelta

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.command_cursor import CommandCursor

GROUP_TYPE_FORMATS: dict = {
    'month': '%Y-%m-01T00:00:00',
    'day':   '%Y-%m-%dT00:00:00',
    'hour':  '%Y-%m-%dT%H:00:00',
}


def aggregate_payments(dt_from: str, dt_upto: str, group_type: str) -> dict:
    collection: Collection = MongoClient('localhost', 27017)['task']['salary']

    dt_from, dt_upto = dt.fromisoformat(dt_from), dt.fromisoformat(dt_upto)
    dt_format: str = GROUP_TYPE_FORMATS.get(group_type)

    aggregated_result: CommandCursor = collection.aggregate([
        {
            "$densify": {
                "field": "dt",
                "range": {
                    "step": 1,
                    "unit": group_type,
                    "bounds": [dt_from, dt_upto + timedelta(days=1)]
                }
            }
        },
        {"$match": {"dt": {"$gte": dt_from, "$lte": dt_upto}}},
        {
            "$group": {
                "_id": {
                    "$dateToString": {"format": dt_format, "date": "$dt"}},
                "totalValue": {"$sum": "$value"},
            },
        },
        {"$sort": {"_id": 1}},
    ])

    dataset, labels = [], []
    for r in aggregated_result:
        dataset.append(r.get('totalValue'))
        labels.append(dt.strptime(r.get('_id'), dt_format).isoformat())

    return {'dataset': dataset, 'labels': labels}


print(aggregate_payments("2022-09-01T00:00:00", "2022-12-31T23:59:00", "month"))
