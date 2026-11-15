import redis
from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.database import get_db

settings = get_settings()

app = FastAPI(title="CommerceFlow API", version="0.1.0")


@app.get("/health", tags=["system"])
def health() -> dict:
    return {"status": "ok", "env": settings.app_env}


@app.get("/health/db", tags=["system"])
def health_db(db: Session = Depends(get_db)) -> dict:
    db.execute(text("SELECT 1"))
    return {"status": "ok", "database": "connected"}


@app.get("/health/redis", tags=["system"])
def health_redis() -> dict:
    client = redis.Redis.from_url(settings.redis_url)
    client.ping()
    return {"status": "ok", "redis": "connected"}