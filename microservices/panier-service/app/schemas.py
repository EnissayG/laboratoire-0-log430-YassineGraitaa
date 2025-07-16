from pydantic import BaseModel
from typing import Optional


class PanierCreate(BaseModel):
    client_id: int
    produit_id: int
    nom_produit: str
    quantite: int
    prix_unitaire: float


class PanierDTO(PanierCreate):
    id: int

    class Config:
        orm_mode = True
