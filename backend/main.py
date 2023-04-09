"""This script contains the basic logic of the bot."""

from datetime import datetime as dt

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.command_cursor import CommandCursor

app: FastAPI = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)
GROUP_TYPE_FORMATS: dict = {
    "month": "%Y-%m-01T00:00:00",
    "day":   "%Y-%m-%dT00:00:00",
    "hour":  "%Y-%m-%dT%H:00:00",
}


@app.get("/aggregate_payments/{dt_from}/{dt_upto}/{group_type}")
async def aggregate_payments(dt_from, dt_upto, group_type):
    """The function returns the amounts of salaries for a given period.

        The function accepts the date and time of the start and end of aggregation
        in ISO format, as well as the type of aggregation.
        And returns a list of amounts and date labels."""

    collection: Collection = MongoClient("mongo_db", 27017)["task"]["salary"]

    dt_from, dt_upto = dt.fromisoformat(dt_from), dt.fromisoformat(dt_upto)
    dt_format: str = GROUP_TYPE_FORMATS.get(group_type)

    aggregated_results: CommandCursor = collection.aggregate([
        {"$match": {"dt": {"$gte": dt_from, "$lte": dt_upto}}},
        {"$group": {
            "_id": {"$dateToString": {"format": dt_format, "date": "$dt"}},
            "total": {"$sum": "$value"},
        }},
        {"$sort": {"_id": 1}},
    ])

    dataset, labels = zip(*[[
        result["total"],
        dt.strptime(result["_id"], dt_format).isoformat()
    ] for result in aggregated_results])

    return {"dataset": dataset, "labels": labels}

# Second version
    # dataset, labels = [], []
    # for result in aggregated_results:
    #     dataset.append(result.get("total"))
    #     labels.append(dt.strptime(result.get("_id"), dt_format).isoformat())
