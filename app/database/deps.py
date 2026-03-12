from app.database.database import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator
from fastapi import Depends, HTTPException, Header
from app.services.auth import verify_access_token
from app.database.crud import get_device_by_api_key

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

async def get_current_user(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")
    token = authorization.split(" ")[1]
    payload = verify_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload

async def get_current_device(x_api_key: str = Header(...), db: AsyncSession = Depends(get_db)):
    device = await get_device_by_api_key(db, x_api_key)
    if device is None:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return device