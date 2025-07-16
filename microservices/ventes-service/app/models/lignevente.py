from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class LigneVente(Base):
    __tablename__ = "lignes_vente"

    id = Column(Integer, primary_key=True)
    vente_id = Column(Integer, ForeignKey("ventes.id"))
    produit_id = Column(
        Integer
    )  # ici aussi, pas besoin de ForeignKey si le produit vient d'un autre microservice
    quantite = Column(Integer)
    sous_total = Column(Float)

    vente = relationship("Vente", back_populates="lignes")
