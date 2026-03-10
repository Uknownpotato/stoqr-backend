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
    device_id: str
    barcode: str
    action: ActionType
    timestamp: str
    source: SourceType

class ScanResponse(BaseModel):
    product_name: Optional[str] = None
    status: ActionResponse
    message: Optional[str] = None
