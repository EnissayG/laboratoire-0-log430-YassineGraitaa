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
    magasin_id: int


class DemandeApprovisionnementOut(BaseModel):
    id: int
    produit_id: int
    quantite: int
    magasin_id: int
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
    magasin_id: int  # mis à jour
    total: float
    lignes: List[LigneVenteOut]

    class Config:
        from_attributes = True


# ========================
class RapportVenteDTO(BaseModel):
    magasin: str
    nombre_ventes: int
    total_ventes: float


class RapportVenteResponse(BaseModel):
    rapport: List[RapportVenteDTO]


class ProduitStockDTO(BaseModel):
    id: int
    nom: str
    categorie: str
    quantite_stock: int
    prix: float

    class Config:
        from_attributes = True  # ✅ pour Pydantic v2 (au lieu de orm_mode)


class ProduitVendableDTO(BaseModel):
    nom: str
    categorie: str
    quantite: int


class ProduitSimpleDTO(BaseModel):
    nom: str
    categorie: str
    stock: int

    class Config:
        from_attributes = True


class VentesParMagasinDTO(BaseModel):
    magasin: str
    total: float


class TendanceJourDTO(BaseModel):
    jour: str  # ISO date string
    total: float


class PerformanceGlobaleDTO(BaseModel):
    total_ventes: float
    produits: List[ProduitVendableDTO]
    ruptures: List[ProduitSimpleDTO]
    surstocks: List[ProduitSimpleDTO]
    ventes_par_magasin: List[VentesParMagasinDTO]
    tendance_journaliere: List[TendanceJourDTO]


# ========================


class MagasinCreate(BaseModel):
    nom: str
    adresse: str | None = None
    ville: str | None = None


class MagasinDTO(MagasinCreate):
    id: int

    class Config:
        from_attributes = True  # anciennement orm_mode


class ProduitStockDTO(BaseModel):
    id: int
    nom: str
    categorie: str
    quantite_stock: int
    prix: float

    class Config:
        from_attributes = True


class VenteOut(BaseModel):
    id: int
    date: datetime  # ✅ Ceci accepte un datetime et le convertit automatiquement en string ISO
    magasin_id: int
    total: float

    class Config:
        from_attributes = True


class VenteRapportDTO(BaseModel):
    produit: str
    magasin: str
    quantite: int
    total: float


class MessageResponse(BaseModel):
    message: str
