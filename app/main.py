from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routes import scan
from app.database.database import init_db
import logging

logging.basicConfig(level=logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(scan.router)

@app.get("/")
async def root():
    return {"status": "Stoqr backend running"}