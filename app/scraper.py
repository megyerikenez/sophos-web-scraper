import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime, timezone
from app.constants import BASE_URL

class WebScraper:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url

    def extract_urls(self):
        response = requests.get(self.base_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        urls = set()

        for a in soup.find_all('a', href=True):
            href = a['href']
            full_url = urljoin(self.base_url, href)
            urls.add(full_url)

        return urls

    def scrape(self):
        urls = self.extract_urls()
        timestamp = datetime.now(timezone.utc)
        return [{"url": url, "collected_at": timestamp} for url in urls], timestamp
