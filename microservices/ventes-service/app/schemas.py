from pydantic import BaseModel
from typing import List
from datetime import datetime


# 🔹 DTO pour une ligne de vente
class LigneVenteOut(BaseModel):
    produit_id: int
    quantite: int
    sous_total: float

    class Config:
        from_attributes = True


# 🔹 DTO pour une vente
class VenteOut(BaseModel):
    id: int
    date: datetime
    magasin_id: int
    total: float
    lignes: List[LigneVenteOut]

    class Config:
        from_attributes = True


# 🔹 Réponse simple (message + données optionnelles)
class MessageResponse(BaseModel):
    message: str
    vente_id: int | None = None
    total: float | None = None


# 🔹 Pour le rapport de performance globale
class ProduitVendableDTO(BaseModel):
    nom: str
    categorie: str
    quantite: int


class ProduitSimpleDTO(BaseModel):
    nom: str
    categorie: str
    stock: int


class VentesParMagasinDTO(BaseModel):
    magasin: str
    total: float


class TendanceJourDTO(BaseModel):
    jour: str  # format "YYYY-MM-DD"
    total: float


class PerformanceGlobaleDTO(BaseModel):
    total_ventes: float
    produits: List[ProduitVendableDTO]
    ruptures: List[ProduitSimpleDTO]
    surstocks: List[ProduitSimpleDTO]
    ventes_par_magasin: List[VentesParMagasinDTO]
    tendance_journaliere: List[TendanceJourDTO]


class ProduitQuantite(BaseModel):
    produit_id: int
    quantite: int
    prix: float


class VenteInput(BaseModel):
    client_id: int
    magasin_id: int
    produits: list[ProduitQuantite]
