from fastapi import APIRouter
from ..models.scan import ScanEvent, ScanResponse, ActionResponse
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/scan", response_model=ScanResponse)
async def scan(event: ScanEvent):
    logger.info(f"Scan received: {event.barcode} - {event.action}")
    return ScanResponse(product_name="Test Product", status=ActionResponse.OK)
    