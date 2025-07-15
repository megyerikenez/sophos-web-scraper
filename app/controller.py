from flask import jsonify
from app.constants import ROUTE_SCRAPE_URLS, ROUTE_LIST_URLS, COLLECTION_NAME

class ScraperController:
    def __init__(self, app, scraper, mongo_connector):
        self.app = app
        self.scraper = scraper
        self.mongo = mongo_connector
        self.setup_routes()

    def setup_routes(self):
        @self.app.route(ROUTE_SCRAPE_URLS, methods=['POST'])
        def scrape_urls():
            try:
                urls_data, timestamp = self.scraper.scrape()
                collection = self.mongo.get_collection(COLLECTION_NAME)
                if urls_data:
                    collection.insert_many(urls_data)
                return jsonify({
                    "message": f"Collected and saved {len(urls_data)} URLs",
                    "timestamp": timestamp.isoformat()
                }), 201
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @self.app.route(ROUTE_LIST_URLS, methods=['GET'])
        def list_urls():
            try:
                collection = self.mongo.get_collection(COLLECTION_NAME)
                urls = list(collection.find({}, {"_id": 0}))
                return jsonify(urls)
            except Exception as e:
                return jsonify({"error": str(e)}), 500
