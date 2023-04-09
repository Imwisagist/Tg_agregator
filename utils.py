"""This script contains the basic logic of the bot."""

from datetime import datetime as dt, timedelta

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.command_cursor import CommandCursor

GROUP_TYPE_FORMATS: dict = {
    "month": "%Y-%m-01T00:00:00",
    "day":   "%Y-%m-%dT00:00:00",
    "hour":  "%Y-%m-%dT%H:00:00",
}


def aggregate_payments(dt_from: str, dt_upto: str, group_type: str) -> dict:
    """The function returns the amounts of salaries for a given period.

    The function accepts the date and time of the start and end of aggregation
    in ISO format, as well as the type of aggregation.
    And returns a list of amounts and date labels."""

    collection: Collection = MongoClient("localhost", 27017)["task"]["salary"]

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
        dataset.append(r.get("totalValue"))
        labels.append(dt.strptime(r.get("_id"), dt_format).isoformat())

    return {"dataset": dataset, "labels": labels}
