from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CommandeCreate(BaseModel):
    client_id: int
    total: float


class CommandeOut(BaseModel):
    id: int
    client_id: int
    total: float
    statut: str
    date: datetime

    class Config:
        orm_mode = True


class CommandeInput(BaseModel):
    client_id: int
    magasin_id: int
