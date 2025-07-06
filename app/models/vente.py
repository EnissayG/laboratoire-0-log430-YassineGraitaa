from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base


class Vente(Base):
    __tablename__ = "ventes"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.utcnow)
    total = Column(Float, nullable=False)

    # ✅ Utilisation d'une relation réelle vers Magasin
    magasin_id = Column(Integer, ForeignKey("magasins.id"))
    magasin_ref = relationship("Magasin", back_populates="ventes")

    lignes = relationship(
        "LigneVente", back_populates="vente", cascade="all, delete-orphan"
    )
