from pydantic import BaseModel
from enum import Enum
from typing import Optional

class ActionResponse(str, Enum):
    OK = "ok"
    FAIL = "fail"
    TIMEOUT = "timeout"

class ActionType(str, Enum):
    ADD = "add"
    REMOVE = "remove"

class SourceType(str, Enum):
    DEVICE = "device"
    PHONE = "phone"
    MANUAL = "manual"

class ScanEvent(BaseModel):
    barcode: str
    action: ActionType
    timestamp: str
    source: SourceType

class ScanResponse(BaseModel):
    product_name: Optional[str] = None
    status: ActionResponse
    message: Optional[str] = None

class InventoryItem(BaseModel):
    barcode: str
    product_name: str | None
    quantity: int

class InventoryResponse(BaseModel):
    device_id: str
    items: list[InventoryItem]

class RegisterRequest(BaseModel):
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class DeviceRegisterRequest(BaseModel):
    name: str

class DeviceRegisterResponse(BaseModel):
    device_id: int
    name: str
    api_key: str