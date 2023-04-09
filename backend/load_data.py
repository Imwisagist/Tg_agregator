import bson

from pymongo import MongoClient
from pymongo.collection import Collection

collection: Collection = MongoClient('mongo_db', 27017)['task']['salary']
if not collection.find_one():
    with open('salary_collection.bson', 'rb') as bson_file:
        collection.insert_many(bson.decode_all(bson_file.read()))
    print('Database has become full')
else:
    print('The script didn\'t work. Cuz database not empty.')
