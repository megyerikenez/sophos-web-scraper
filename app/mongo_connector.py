import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

class MongoConnector:
    def __init__(self, uri=None, db_name="scraperdb"):
        self.uri = uri or os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
        self.db_name = db_name
        self.client = None
        self.db = None

    def connect(self):
        try:
            self.client = MongoClient(self.uri, serverSelectionTimeoutMS=3000)
            self.client.admin.command("ping")
            self.db = self.client[self.db_name]
            print("Connection successful.")
        except ConnectionFailure as e:
            print("Connection failed:", str(e))
            raise

    def get_db(self):
        if self.db is None:
            raise Exception("Database is not connected!")
        return self.db

