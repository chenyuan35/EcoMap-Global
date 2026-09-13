# Free server application notes

## Project description

EcoMap Global is a non-commercial open-source project for organizing and visualizing public environmental and geographic data. It provides an interactive world map and API for exploring measurements such as temperature and air quality. The project is intended for learning, technical research and open-source development, and does not sell products or paid services.

## Technical description

The server will host the public web application, FastAPI service and a lightweight SQLite database, and will later run scheduled tasks that synchronize selected public environmental datasets. The deployment uses Debian/Ubuntu, Docker, Python/FastAPI, SQLite and Nginx or a similar reverse proxy. Expected traffic is low during development.

Target resources: 2 vCPU, 2–4 GB RAM and 20–40 GB storage. These resources leave enough capacity for the web/API service, container runtime, cached datasets and future historical observations.

## Repository

https://github.com/chenyuan35/EcoMap-Global
