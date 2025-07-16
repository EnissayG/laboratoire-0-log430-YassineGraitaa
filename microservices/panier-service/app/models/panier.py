from sqlalchemy import Column, Integer, String, Float
from app.db.database import Base


class Panier(Base):
    __tablename__ = "paniers"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, index=True)
    produit_id = Column(Integer, nullable=False)
    nom_produit = Column(String, nullable=False)
    quantite = Column(Integer, nullable=False)
    prix_unitaire = Column(Float, nullable=False)

    def __repr__(self):
        return f"<Panier {self.nom_produit} x{self.quantite}>"
