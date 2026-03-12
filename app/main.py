from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routes import scan, inventory, auth, devices
from app.database.database import init_db
import logging
import os
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(scan.router)
app.include_router(inventory.router)
app.include_router(auth.router, prefix="/auth")
app.include_router(devices.router, prefix="/devices")

@app.get("/")
async def root():
    return {"status": "Stoqr backend running"}