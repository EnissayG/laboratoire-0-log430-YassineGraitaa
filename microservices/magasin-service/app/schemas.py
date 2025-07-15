from pydantic import BaseModel
from typing import Optional, List


class MagasinCreate(BaseModel):
    nom: str
    adresse: Optional[str]
    ville: Optional[str]


class MagasinDTO(MagasinCreate):
    id: int

    class Config:
        from_attributes = True


class ProduitStockDTO(BaseModel):
    id: int
    nom: str
    categorie: str
    quantite_stock: int
    prix: float

    class Config:
        from_attributes = True
