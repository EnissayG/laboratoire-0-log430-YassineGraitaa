from sqlalchemy.orm import relationship
from app.db.database import Base
from sqlalchemy import Column, Integer, String


class Magasin(Base):
    __tablename__ = "magasins"

    id = Column(Integer, primary_key=True)
    nom = Column(String, unique=True, index=True)
    adresse = Column(String, nullable=True)
    ville = Column(String, nullable=True)

    produits = relationship("Produit", back_populates="magasin")
