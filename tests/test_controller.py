import pytest
from flask import Flask
from unittest.mock import MagicMock
from app.controller import ScraperController
from app.constants import ROUTE_SCRAPE_URLS, ROUTE_LIST_URLS

@pytest.fixture
def app_and_mocks():
    app = Flask(__name__)

    mock_scraper = MagicMock()
    mock_mongo = MagicMock()
    mock_collection = MagicMock()
    mock_mongo.get_collection.return_value = mock_collection

    ScraperController(app, mock_scraper, mock_mongo)

    return app, mock_scraper, mock_mongo, mock_collection


def test_scrape_urls_success(app_and_mocks):
    app, mock_scraper, mock_mongo, mock_collection = app_and_mocks

    mock_scraper.scrape.return_value = (
        [{"url": "http://example.com", "collected_at": "timestamp"}],
        MagicMock(isoformat=lambda: "2024-01-01T00:00:00Z")
    )

    with app.test_client() as client:
        response = client.post(ROUTE_SCRAPE_URLS)
        assert response.status_code == 201
        json_data = response.get_json()
        assert "Collected and saved" in json_data["message"]
        assert json_data["timestamp"] == "2024-01-01T00:00:00Z"
        mock_collection.insert_many.assert_called_once()


def test_list_urls_success(app_and_mocks):
    app, _, mock_mongo, mock_collection = app_and_mocks

    mock_collection.find.return_value = [
        {"url": "http://example.com", "collected_at": "2024-01-01T00:00:00Z"}
    ]

    with app.test_client() as client:
        response = client.get(ROUTE_LIST_URLS)
        assert response.status_code == 200
        json_data = response.get_json()
        assert isinstance(json_data, list)
        assert json_data[0]["url"] == "http://example.com"
        mock_collection.find.assert_called_once_with({}, {"_id": 0})
