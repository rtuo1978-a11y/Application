from pymongo import MongoClient
from django.conf import settings

class MongoDB:
    _instance = None
    _client = None
    _db = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDB, cls).__new__(cls)
            cls._client = MongoClient(settings.MONGO_URL, tz_aware=True)
            cls._db = cls._client[settings.DB_NAME]
        return cls._instance

    @property
    def db(self):
        return self._db

    def get_collection(self, collection_name):
        return self._db[collection_name]

def get_db():
    return MongoDB().db
