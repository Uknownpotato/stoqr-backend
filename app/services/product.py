import httpx
import logging

logger = logging.getLogger(__name__)

BASE_URL = "https://world.openfoodfacts.org/api/v0/product"

async def get_product_name(barcode: str) -> str | None:
    url = f"{BASE_URL}/{barcode}.json"

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(url)
        data = response.json()
    
    except Exception as e:
        logger.error(f"Product lookup failed: {type(e).__name__}: {e}")
        return None

    if data.get("status") == 1:
        product = data.get("product", {})
        return product.get("product_name")
    return None