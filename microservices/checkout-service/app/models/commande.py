from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base


class Commande(Base):
    __tablename__ = "commandes"

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer)
    total = Column(Float)
    statut = Column(String, default="en_attente")
    date = Column(DateTime, default=datetime.utcnow)
