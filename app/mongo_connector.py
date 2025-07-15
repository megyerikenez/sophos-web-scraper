import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from app.constants import MONGO_URI_ENV_VAR, DEFAULT_MONGO_URI, DATABASE_NAME, MONGO_TIMEOUT_MS

class MongoConnector:
    def __init__(self, uri=None, db_name=DATABASE_NAME):
        self.uri = uri or os.environ.get(MONGO_URI_ENV_VAR, DEFAULT_MONGO_URI)
        self.db_name = db_name
        self.client = None
        self.db = None

    def connect(self):
        try:
            self.client = MongoClient(self.uri, serverSelectionTimeoutMS=MONGO_TIMEOUT_MS)
            self.client.admin.command("ping")
            self.db = self.client[self.db_name]
        except ConnectionFailure as e:
            print("Connection failed:", str(e))
            raise

    def get_collection(self, name):
        if self.db is None:
            raise Exception("Database not connected.")
        return self.db[name]
