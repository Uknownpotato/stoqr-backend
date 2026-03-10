from fastapi import APIRouter
from ..models.scan import ScanEvent, ScanResponse, ActionResponse
from ..services.product import get_product_name
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/scan", response_model=ScanResponse)
async def scan(event: ScanEvent):
    logger.info(f"Scan received: {event.barcode} - {event.action}")

    product_name = await get_product_name(event.barcode)

    if product_name is None:
        return ScanResponse(
            product_name=None,
            status=ActionResponse.FAIL,
            message="Product not found"
        )

    return ScanResponse(product_name=product_name, status=ActionResponse.OK)