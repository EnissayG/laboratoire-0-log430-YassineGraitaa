from sqlalchemy import Column, Integer, Float, DateTime, String
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base


class Vente(Base):
    __tablename__ = "ventes"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.utcnow)
    total = Column(Float, nullable=False)
    magasin = Column(String, nullable=False)  # ✅ Ajout corrigé

    lignes = relationship(
        "LigneVente", back_populates="vente", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Vente(id={self.id}, magasin={self.magasin}, total={self.total})>"
