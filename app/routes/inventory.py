from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..database.deps import get_db, get_current_user
from ..database.crud import get_inventory, get_product, get_user_by_email, get_device_by_id
from ..models.scan import InventoryResponse, InventoryItem
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/inventory/{device_id}", response_model=InventoryResponse)
async def get_inventory_router(device_id: int, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    email = current_user["sub"]
    user = await get_user_by_email(db, email)

    device = await get_device_by_id(db, device_id)
    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    
    if device.user_id != user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    

    
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
    
    return InventoryResponse(device_id=str(device_id), items=items)