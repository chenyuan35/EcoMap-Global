# EcoMap Global

EcoMap Global is a lightweight, non-commercial open-source project for exploring environmental and geographic data on an interactive world map. It provides a small FastAPI backend, SQLite storage and a Leaflet-based web interface that can run on modest VPS hardware.

The repository currently includes a self-contained demo dataset so the project works immediately without API keys. The next development stage is to add adapters for public weather, air-quality and environmental datasets while preserving source attribution and collection timestamps.

## Features

- Interactive global map powered by Leaflet and OpenStreetMap
- Environmental observation API with metric filtering
- Temperature and PM2.5 demo observations across multiple regions
- SQLite persistence with automatic first-run initialization
- Health endpoint for uptime monitoring
- Docker and Docker Compose deployment
- Automatic OpenAPI documentation from FastAPI
- Designed for low-resource, long-running VPS hosting

## Project structure

```text
EcoMap-Global/
├── app/
│   ├── __init__.py
│   ├── db.py
│   └── main.py
├── docs/
│   └── data-sources.md
├── static/
│   └── index.html
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Quick start with Docker

```bash
git clone https://github.com/chenyuan35/EcoMap-Global.git
cd EcoMap-Global
docker compose up -d --build
```

Open `http://SERVER_IP:8000` in a browser.

API documentation is available at `http://SERVER_IP:8000/docs`.

## Run without Docker

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API

- `GET /health` — service health check
- `GET /api/v1/observations` — list observations
- `GET /api/v1/observations?metric=temperature` — filter by metric
- `GET /api/v1/summary` — aggregate metrics
- `GET /docs` — interactive OpenAPI documentation

Example:

```bash
curl http://localhost:8000/api/v1/observations?metric=pm25
```

## Server requirements

The application is intentionally small. A practical development/deployment target is:

- 2 vCPU
- 2–4 GB RAM
- 20–40 GB storage
- Debian 12 or Ubuntu LTS
- Docker Engine + Docker Compose

Lower specifications can also run the current version. Additional memory and disk space are useful for future public-data ingestion, caching and historical observations.

## Data sources

The bundled records are explicitly marked as demo data. Planned integrations include public environmental sources such as Open-Meteo, OpenAQ-compatible feeds and World Bank open datasets. See [`docs/data-sources.md`](docs/data-sources.md).

## Roadmap

- Public weather-data ingestion
- Air-quality feed adapters
- Scheduled background synchronization
- Historical charts and date-range filters
- Geographic search
- Data-source status page
- Export to CSV/GeoJSON

## Non-commercial use

EcoMap Global is developed as a non-commercial open-source learning and public-data project. It does not sell products or paid services.

## License

MIT License. See [`LICENSE`](LICENSE).
