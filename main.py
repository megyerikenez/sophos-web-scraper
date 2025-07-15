from app.mongo_connector import MongoConnector

if __name__ == "__main__":
    connector = MongoConnector()
    connector.connect()
    db = connector.get_db()
