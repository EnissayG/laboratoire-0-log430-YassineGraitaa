from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base


class LigneVente(Base):
    __tablename__ = "lignes_vente"

    id = Column(Integer, primary_key=True, index=True)
    vente_id = Column(Integer, ForeignKey("ventes.id"))
    produit_id = Column(Integer, ForeignKey("produits.id"))
    quantite = Column(Integer, nullable=False)
    sous_total = Column(Float, nullable=False)

    vente = relationship("Vente", back_populates="lignes")
    produit = relationship("Produit")

    def __repr__(self):
        return f"<LigneVente(vente_id={self.vente_id}, produit_id={self.produit_id}, quantite={self.quantite})>"
