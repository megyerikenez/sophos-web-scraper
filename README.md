# Sophos Web Scraper

Sophos Web Scraper is a Python-based web scraping API designed to collect URLs from [sophostest.com/index.html](http://sophostest.com/index.html) and save them with timestamps in a MongoDB database. It exposes two endpoints:

- **POST /api/scrapeurls** — Scrapes the site and stores the URLs with timestamps in MongoDB.
- **GET /api/listurls** — Retrieves the stored URLs in JSON format.

---

## Features

- Scrapes all anchor tags (`<a>`) on the target page, resolving relative links to absolute URLs.
- Saves scraped URLs along with the UTC timestamp of collection.
- Simple Flask REST API for scraping and fetching data.
- Uses MongoDB for persistent storage.
- Dockerized for easy deployment.

---

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/megyerikenez/sophos-web-scraper.git
cd sophos-web-scraper
```

### 2. Run the app with Docker Compose

```bash
docker compose up --build
```

- The Flask API will be accessible on http://localhost:5001
- MongoDB runs in a separate container

## Testing

- The application does not come with any UI; it is a simple REST API.
- For manual testing, you can use `curl` commands as shown below.

### Trigger URL Scraping and display the stored data

```bash
curl -X POST http://localhost:5001/api/scrapeurls
curl http://localhost:5001/api/listurls
```

## Unit Tests

- The project includes unit tests written with pytest that mock external dependencies.
- To run the unit tests inside the Docker container, use:

```bash
docker compose run --rm app pytest tests/
```

### API Endpoints

#### /api/scrapeurls

```bash
POST /api/scrapeurls
```

Triggers scraping of URLs from the target website and saves them to MongoDB.

Response:

```bash
{
  "message": "Collected and saved 25 URLs",
  "timestamp": "2025-07-15T14:30:00Z"
}
```

#### /api/listurls

```bash
GET /api/listurls
```

Returns all scraped URLs stored in the database.

Response:

```bash
[
  {
    "collected_at": "Tue, 15 Jul 2025 21:37:40 GMT"
    "url": "http://sophostest.com/category/email",
  },
  ...
]
```

- **Author:** Kenez Megyeri
- **GitHub:** [@megyerikenez](https://github.com/megyerikenez)
- **LinkedIn:** [@megyerikenez](https://www.linkedin.com/in/megyeri-kenez-93b4341b0/)
