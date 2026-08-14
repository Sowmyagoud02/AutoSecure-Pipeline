from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from backend.database.dependencies import get_db
from backend.database.init_db import init_db

from backend.api.auth import router as auth_router
from backend.api.users import router as users_router
from backend.api.ingestion import router as ingestion_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="AutoSecure Pipeline",
    description="Event-driven secure data processing and automation platform",
    version="0.1.0",
    lifespan=lifespan,
)


app.include_router(auth_router)
app.include_router(users_router)
app.include_router(ingestion_router)

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "autosecure-pipeline",
    }


@app.get("/health/db")
def database_health_check(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT 1"))

    return {
        "database": "connected",
        "result": result.scalar(),
    }