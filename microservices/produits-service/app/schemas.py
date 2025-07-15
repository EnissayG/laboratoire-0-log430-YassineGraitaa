from pydantic import BaseModel
from typing import Optional


class ProduitOut(BaseModel):
    id: int
    nom: str
    prix: float
    categorie: str
    quantite_stock: int

    class Config:
        from_attributes = True


class ProduitUpdate(BaseModel):
    nom: Optional[str]
    categorie: Optional[str]
    prix: Optional[float]
    quantite_stock: Optional[int]
