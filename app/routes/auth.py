from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.deps import get_db
from app.database.crud import get_user_by_email, create_user, create_refresh_token as create_refresh_token_db, delete_refresh_token, get_refresh_token, get_user_by_id
from app.services.auth import hash_password, verify_password, create_access_token, create_refresh_token
from app.models.scan import RegisterRequest, LoginRequest, TokenResponse
from app.utils import utcnow
from datetime import datetime, timezone, timedelta
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/register", response_model=TokenResponse)
async def register(request: RegisterRequest, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_email(db, request.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    password_hash = hash_password(request.password)
    user = await create_user(db, request.email, password_hash)
    logger.info(f"New user registered: {request.email}")

    expires_at = utcnow() #datetime.now(timezone.utc) + timedelta(days=30)
    refresh_token = create_refresh_token()
    await create_refresh_token_db(db, user.id, refresh_token, expires_at)

    token = create_access_token({"sub": user.email})
    return TokenResponse(access_token=token, refresh_token=refresh_token)


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_email(db, request.email)
    if user is None:
        logger.warning(f"Failed login attempt for: {request.email}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    password_verify = verify_password(request.password, user.password_hash)
    if password_verify is False:
        logger.warning(f"Failed login attempt for: {request.email}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    expires_at = utcnow() #datetime.now(timezone.utc) + timedelta(days=30)
    refresh_token = create_refresh_token()
    await create_refresh_token_db(db, user.id, refresh_token, expires_at)

    token = create_access_token({"sub": user.email})
    return TokenResponse(access_token=token, refresh_token=refresh_token)

@router.post("/refresh", response_model=TokenResponse)
async def refresh(refresh_token: str, db: AsyncSession = Depends(get_db)):
    token = await get_refresh_token(db, refresh_token)
    if token is None:
        logger.warning(f"Invalid refresh token attempt")
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    if token.expires_at < utcnow(): #.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        logger.warning(f"Expired refresh token attempt")
        raise HTTPException(status_code=401, detail="Refresh token expired")
    
    user = await get_user_by_id(db, token.user_id)
    await delete_refresh_token(db, refresh_token)

    expires_at = utcnow() #datetime.now(timezone.utc) + timedelta(days=30)
    new_refresh_token = create_refresh_token()
    await create_refresh_token_db(db, user.id, new_refresh_token, expires_at)

    token = create_access_token({"sub": user.email})
    return TokenResponse(access_token=token, refresh_token=new_refresh_token)

@router.post("/logout")
async def logout(refresh_token: str, db: AsyncSession = Depends(get_db)):
    await delete_refresh_token(db, refresh_token)
    return {"status": "logged out"}