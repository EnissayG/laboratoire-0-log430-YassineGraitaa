from pydantic import BaseModel


class ProduitStockDTO(BaseModel):
    id: int
    nom: str
    categorie: str
    prix: float
    quantite_stock: int
    magasin_id: int

    class Config:
        orm_mode = True


class ProduitQuantite(BaseModel):
    produit_id: int
    quantite: int
    prix: float


class ReservationProduits(BaseModel):
    produits: list[ProduitQuantite]
