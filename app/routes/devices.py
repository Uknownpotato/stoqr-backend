from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.scan import DeviceRegisterRequest, DeviceRegisterResponse
from app.database.crud import create_device, get_user_by_email
from app.database.deps import get_db, get_current_user
import secrets

router = APIRouter()

@router.post("/register", response_model=DeviceRegisterResponse)
async def register_device(request: DeviceRegisterRequest, current_user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    email = current_user["sub"]
    user = await get_user_by_email(db, email)

    api_key = secrets.token_hex(32)
    device = await create_device(db, user.id, request.name, api_key)

    return DeviceRegisterResponse(device_id=device.id, name=device.name, api_key=device.api_key)