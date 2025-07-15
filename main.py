from flask import Flask
from app.mongo_connector import MongoConnector
from app.scraper import WebScraper
from app.controller import ScraperController
from app.constants import FLASK_PORT

def create_app():
    app = Flask(__name__)
    
    mongo = MongoConnector()
    mongo.connect()

    scraper = WebScraper()
    ScraperController(app, scraper, mongo)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=FLASK_PORT)
