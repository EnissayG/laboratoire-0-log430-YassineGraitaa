from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# ========================
# 🔹 PRODUIT
# ========================


from pydantic import BaseModel


class ProduitOut(BaseModel):
    id: int
    nom: str
    prix: float

    class Config:
        orm_mode = True  # Très important pour que FastAPI comprenne l’objet SQLAlchemy


class ProduitUpdate(BaseModel):
    nom: Optional[str]
    categorie: Optional[str]
    prix: Optional[float]
    quantite_stock: Optional[int]


# ========================
# 🔹 APPROVISIONNEMENT
# ========================


class DemandeApprovisionnementIn(BaseModel):
    produit_id: int
    quantite: int
    magasin: str


class DemandeApprovisionnementOut(BaseModel):
    id: int
    produit_id: int
    quantite: int
    magasin: str
    statut: str

    class Config:
        from_attributes = True


# ========================
# 🔹 VENTES
# ========================


class LigneVenteOut(BaseModel):
    produit_id: int
    quantite: int
    sous_total: float

    class Config:
        from_attributes = True


class VenteOut(BaseModel):
    id: int
    date: datetime
    magasin: str
    total: float
    lignes: List[LigneVenteOut]

    class Config:
        from_attributes = True
