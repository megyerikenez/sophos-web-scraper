import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from app.scraper import WebScraper

MOCK_HTML = """
<html>
  <body>
    <a href="sophospage1.html">Sophos Page 1</a>
    <a href="/sophospage2.html">Sophos Page 2</a>
    <a href="http://external.com/sophospage3.html">Sophos External Page 3</a>
  </body>
</html>
"""

@pytest.fixture
def mock_requests_get():
    with patch("app.scraper.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = MOCK_HTML
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        yield mock_get

def test_extract_urls(mock_requests_get):
    scraper = WebScraper(base_url="http://testserver.com")

    urls = scraper.extract_urls()
    expected_urls = {
        "http://testserver.com/sophospage1.html",
        "http://testserver.com/sophospage2.html",
        "http://external.com/sophospage3.html"
    }
    assert urls == expected_urls
    mock_requests_get.assert_called_once_with("http://testserver.com")

def test_scrape_returns_correct_format(mock_requests_get):
    scraper = WebScraper(base_url="http://testserver.com")

    docs, timestamp = scraper.scrape()
    assert isinstance(docs, list)
    assert all("url" in doc and "collected_at" in doc for doc in docs)
    assert all(isinstance(doc["collected_at"], datetime) for doc in docs)
    assert isinstance(timestamp, datetime)
