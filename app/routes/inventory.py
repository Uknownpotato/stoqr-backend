from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..database.deps import get_db, get_current_user
from ..database.crud import get_inventory, get_product, get_user_by_email, get_device_by_id, get_inventory_by_user
from ..models.scan import InventoryResponse, InventoryItem
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/inventory", response_model=InventoryResponse)
async def get_inventory_router(db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    email = current_user["sub"]
    user = await get_user_by_email(db, email)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    quantities = await get_inventory_by_user(db, user.id)

    items = []
    for barcode, quantity in quantities.items():
        product = await get_product(db, barcode)
        product_name = product.product_name if product else None
        items.append(InventoryItem(
            barcode=barcode,
            product_name=product_name,
            quantity=quantity
        ))

    return InventoryResponse(device_id=str(user.id), items=items)