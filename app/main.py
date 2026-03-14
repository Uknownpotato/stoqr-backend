from contextlib import asynccontextmanager
from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.routes import scan, inventory, auth, devices
from app.database.database import init_db
from app.limiter import limiter
from app.logger import setup_logging
from alembic.config import Config
from alembic import command
import logging
import os
from dotenv import load_dotenv
import asyncio

setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, run_migrations)
    yield

def run_migrations():
    try:
        import os
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        alembic_cfg = Config(os.path.join(base_dir,"alembic.ini"))
        command.upgrade(alembic_cfg, "head")
    except Exception as e:
        print(f"Migration error: {e}")
        raise

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