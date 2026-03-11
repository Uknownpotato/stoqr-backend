from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database.models import Product, ScanEvent
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