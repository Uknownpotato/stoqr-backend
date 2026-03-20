from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.scan import DeviceRegisterRequest, DeviceRegisterResponse, ClaimDeviceRequest, ClaimDeviceResponse, LinkDeviceRequest, PollDeviceResponse
from app.database.crud import create_device, get_user_by_email, create_claimed_device, get_claimed_device_by_mac, get_claimed_device_by_token, link_claimed_device, get_device_by_id
from app.database.deps import get_db, get_current_user
import secrets

router = APIRouter()

@router.post("/claim", response_model=ClaimDeviceResponse)
async def claim_device(request: ClaimDeviceRequest, db: AsyncSession = Depends(get_db)):
    existing = await get_claimed_device_by_mac(db, request.mac_address)
    if existing and not existing.linked:
        return ClaimDeviceResponse(claim_token=existing.claim_token)
    
    claim_token = secrets.token_hex(16)
    await create_claimed_device(db, request.mac_address, claim_token)
    return ClaimDeviceResponse(claim_token=claim_token)

@router.post("/link", response_model=DeviceRegisterResponse)
async def link_device(request: LinkDeviceRequest, current_user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    email = current_user["sub"]
    user = await get_user_by_email(db, email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    claimed = await get_claimed_device_by_token(db, request.claim_token)
    if claimed is None:
        raise HTTPException(status_code=404, detail="Claim token not found")
    if claimed.linked:
        raise HTTPException(status_code=400, detail="Device already linked")
    
    api_key = secrets.token_hex(32)
    device = await create_device(db, user.id, request.name, api_key)
    await link_claimed_device(db, request.claim_token, device.id)

    return DeviceRegisterResponse(device_id=device.id, name=device.name, api_key=device.api_key)

@router.get("/poll/{claim_token}", response_model=PollDeviceResponse)
async def poll_device(claim_token: str, db: AsyncSession = Depends(get_db)):
    claimed = await get_claimed_device_by_token(db, claim_token)
    if claimed is None:
        raise HTTPException(status_code=404, detail="Claim token not found")
    
    if not claimed.linked or claimed.device_id is None:
        return PollDeviceResponse(linked=False, device_id=None, api_key=None)

    device = await get_device_by_id(db, claimed.device_id)
    return PollDeviceResponse(linked=True, device_id=device.id, api_key=device.api_key)