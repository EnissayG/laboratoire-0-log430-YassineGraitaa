from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.magasin import Magasin
from app.db import Base


class DemandeApprovisionnement(Base):
    __tablename__ = "demandes_approvisionnement"

    id = Column(Integer, primary_key=True, index=True)
    produit_id = Column(Integer, ForeignKey("produits.id"))
    magasin_id = Column(Integer, ForeignKey("magasins.id"))
    quantite = Column(Integer)
    statut = Column(String, default="en_attente")

    produit = relationship("Produit")
    magasin = relationship("Magasin")
