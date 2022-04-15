import certifi
from pymongo import MongoClient

from src.Util.CommonUtil import CommonUtil


class Database:

    def __init__(self):
        config = CommonUtil.read_properties()
        self._db_conn = MongoClient(config.get("DB_URL").data, tlsCAFile=certifi.where())
        self._db = self._db_conn[config.get("DB_NAME").data]
        self._connection_names = self._db.list_collection_names()

    def list_of_connections(self):
        return self._connection_names

    def insert_single_data(self, collection, data):
        db_collection = self._db[collection]
        document = db_collection.insert_one(data)
        return document.inserted_id

    # This method inserts multiple rows in collection
    def insert_multiple_data(self, collection, data):
        db_collection = self._db[collection]
        result = db_collection.insert_many(data)
        return result.inserted_ids


