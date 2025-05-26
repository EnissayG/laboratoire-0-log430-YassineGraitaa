from sqlalchemy import Column, Integer, String, Float
from app.db import Base

class Produit(Base):
    __tablename__ = "produits"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False)
    categorie = Column(String, nullable=False)
    prix = Column(Float, nullable=False)
    quantite_stock = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Produit(id={self.id}, nom='{self.nom}', prix={self.prix}, stock={self.quantite_stock})>"
