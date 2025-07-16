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
