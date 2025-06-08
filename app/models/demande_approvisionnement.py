from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base


class DemandeApprovisionnement(Base):
    __tablename__ = "demandes_approvisionnement"

    id = Column(Integer, primary_key=True, index=True)
    produit_id = Column(Integer, ForeignKey("produits.id"))
    quantite = Column(Integer)
    magasin = Column(String)
    statut = Column(String, default="en_attente")

    produit = relationship("Produit")
