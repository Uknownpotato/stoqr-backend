from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database.models import Product, ScanEvent, User, Device
from datetime import datetime, timezone

async def get_product(db: AsyncSession, barcode: str) -> Product | None:
    result = await db.execute(select(Product).where(Product.barcode == barcode))
    return result.scalar_one_or_none()

async def save_product(db: AsyncSession, barcode: str, product_name: str, brand: str | None):
    product = Product(
        barcode=barcode,
        product_name=product_name,
        brand=brand,
        cached_at=datetime.now(timezone.utc)
    )
    db.add(product)
    await db.commit()
    return product

async def save_scan_event(db: AsyncSession, device_id: str, barcode: str, action: str, source: str):
    event = ScanEvent(
        device_id=device_id,
        barcode=barcode,
        action=action,
        timestamp=datetime.now(timezone.utc),
        source=source
    )
    db.add(event)
    await db.commit()
    return event

async def get_inventory(db: AsyncSession, device_id: str):
    result = await db.execute(
        select(ScanEvent).where(ScanEvent.device_id == device_id)
    )
    events = result.scalars().all()

    quantities = {}

    for event in events:
        if event.barcode not in quantities:
            quantities[event.barcode] = 0
        if event.action == "add":
            quantities[event.barcode] += 1
        elif event.action == "remove":
            quantities[event.barcode] -= 1
    
    quantities = {k: v for k, v in quantities.items() if v > 0}

    return quantities

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()

async def create_user(db: AsyncSession, email: str, password_hash: str):
    user = User(
        email=email,
        password_hash=password_hash,
        created_at=datetime.now(timezone.utc)
    )
    db.add(user)
    await db.commit()
    return user

async def create_device(db: AsyncSession, user_id: int, name: str, api_key: str):
    device = Device(
        user_id=user_id,
        name=name,
        api_key=api_key,
        created_at=datetime.now(timezone.utc)
    )
    db.add(device)
    await db.commit()
    return device

async def get_device_by_api_key(db: AsyncSession, api_key: str):
    result = await db.execute(select(Device).where(Device.api_key == api_key))
    return result.scalar_one_or_none()

async def get_device_by_id(db: AsyncSession, device_id: int):
    result = await db.execute(select(Device).where(Device.id == device_id))
    return result.scalar_one_or_none()