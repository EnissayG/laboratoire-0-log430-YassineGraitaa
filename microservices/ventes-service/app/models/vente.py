from sqlalchemy import Column, Integer, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base


class Vente(Base):
    __tablename__ = "ventes"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.utcnow)
    total = Column(Float)
    magasin_id = Column(Integer)  # ✅ plus de ForeignKey ici

    lignes = relationship(
        "LigneVente", back_populates="vente", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return (
            f"<Vente(id={self.id}, total={self.total}, magasin_id={self.magasin_id})>"
        )
