from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .db import get_observations, get_summary, init_db

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="EcoMap Global API",
    description="Lightweight environmental data API and map viewer.",
    version="0.1.0",
    lifespan=lifespan,
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", include_in_schema=False)
def homepage() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/v1/observations")
def observations(
    metric: str | None = Query(default=None, description="Optional metric filter, e.g. temperature or pm25"),
    limit: int = Query(default=500, ge=1, le=2000),
) -> dict:
    rows = get_observations(metric=metric, limit=limit)
    return {"count": len(rows), "items": rows}


@app.get("/api/v1/summary")
def summary() -> dict:
    rows = get_summary()
    return {"metrics": rows}
