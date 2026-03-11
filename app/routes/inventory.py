from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..database.deps import get_db
from ..database.crud import get_inventory, get_product
from ..models.scan import InventoryResponse, InventoryItem
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/inventory/{device_id}", response_model=InventoryResponse)
async def get_inventory_router(device_id: str, db: AsyncSession = Depends(get_db)):
    quantities = await get_inventory(db, device_id)

    items = []
    for barcode, quantity in quantities.items():
        product = await get_product(db, barcode)
        product_name = product.product_name if product else None

        items.append(InventoryItem(
            barcode=barcode,
            product_name=product_name,
            quantity=quantity
        ))
    
    return InventoryResponse(device_id=device_id, items=items)