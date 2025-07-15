from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class Produit(Base):
    __tablename__ = "produits"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False)
    categorie = Column(String, nullable=False)
    prix = Column(Float, nullable=False)
    quantite_stock = Column(Integer, nullable=False)

    magasin_id = Column(Integer, ForeignKey("magasins.id"))

    # ✅ Cette relation peut être conservée ici car Magasin est local
    magasin = relationship("Magasin", back_populates="produits")

    def __repr__(self):
        return f"<Produit(id={self.id}, nom='{self.nom}', prix={self.prix}, stock={self.quantite_stock})>"
