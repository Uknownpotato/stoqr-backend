from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.deps import get_db
from app.database.crud import get_user_by_email, create_user
from app.services.auth import hash_password, verify_password, create_access_token
from app.models.scan import RegisterRequest, LoginRequest, TokenResponse
import logging

router = APIRouter(prefix="/auth")
logger = logging.getLogger(__name__)

@router.post("/register", response_model=TokenResponse)
async def register(request: RegisterRequest, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_email(db, request.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    password_hash = hash_password(request.password)
    user = await create_user(db, request.email, password_hash)

    token = create_access_token({"sub": user.email})
    return TokenResponse(access_token=token)


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_email(db, request.email)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    password_verify = verify_password(request.password, user.password_hash)
    if password_verify is False:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": user.email})
    return TokenResponse(access_token=token)