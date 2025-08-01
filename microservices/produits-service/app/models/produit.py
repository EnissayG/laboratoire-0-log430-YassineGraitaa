# Fichier : produits-service/app/models/produit.py

from sqlalchemy import Column, Integer, String, Float
from app.db.database import Base


class Produit(Base):
    __tablename__ = "produits"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False)
    categorie = Column(String, nullable=False)
    prix = Column(Float, nullable=False)
    quantite_stock = Column(Integer, nullable=False)
    magasin_id = Column(Integer, nullable=False)  # 💡 Juste un champ entier
