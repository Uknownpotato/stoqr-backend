from contextlib import asynccontextmanager
from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.routes import scan, inventory, auth, devices
from app.database.database import init_db
from app.limiter import limiter
import logging
import os
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.include_router(scan.router)
app.include_router(inventory.router)
app.include_router(auth.router, prefix="/auth")
app.include_router(devices.router, prefix="/devices")

@app.get("/")
async def root():
    return {"status": "Stoqr backend running"}