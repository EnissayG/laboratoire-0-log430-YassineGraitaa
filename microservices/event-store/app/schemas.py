from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class EvenementIn(BaseModel):
    event_type: str
    aggregate_id: str
    data: dict
    timestamp: Optional[datetime] = None
    source: Optional[str] = None
