from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..database.deps import get_db, get_current_device
from ..database.crud import get_product, save_product, save_scan_event
from ..models.scan import ScanEvent, ScanResponse, ActionResponse
from ..services.product import get_product_name
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/scan", response_model=ScanResponse)
async def scan(event: ScanEvent, db: AsyncSession = Depends(get_db), device = Depends(get_current_device)):
    logger.info(f"Scan received: {event.barcode} - {event.action}")

    product = await get_product(db, event.barcode)
    product_name = None

    if product:
        logger.info(f"Cache hit for barcode: {event.barcode}")
        product_name = product.product_name
    else:
        logger.info(f"Cache miss - calling OFF for: {event.barcode}")
        product_name = await get_product_name(event.barcode)
        if product_name:
            await save_product(db, event.barcode, product_name, None)

    await save_scan_event(db, event.device_id, event.barcode, event.action, event.source)

    if product_name is None:
        return ScanResponse(
            product_name=None,
            status=ActionResponse.FAIL,
            message="Product not found"
        )

    return ScanResponse(product_name=product_name, status=ActionResponse.OK)
