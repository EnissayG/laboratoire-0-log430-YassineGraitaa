# models/commande.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from app.db.database import Base


class Commande(Base):
    __tablename__ = "commandes"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    client_id = Column(Integer, nullable=False)
    magasin_id = Column(Integer, nullable=False)
    etat_actuel = Column(String, nullable=False)
