from pydantic import BaseModel


class ProduitStockDTO(BaseModel):
    id: int
    nom: str
    categorie: str
    quantite_stock: int
    prix: float

    class Config:
        from_attributes = True
