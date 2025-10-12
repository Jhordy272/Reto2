from pydantic import BaseModel, Field
from typing import Optional, Any, Dict

class LogCreate(BaseModel):
    service: str = Field(..., examples=["invoice-controller"])
    level: str = Field(..., examples=["INFO", "WARN", "ERROR"])
    message: str = Field(..., examples=["Started processing request"])
    context: Optional[Dict[str, Any]] = Field(default=None, examples=[{"request_id": "abc-123"}])

class LogOut(LogCreate):
    id: int
