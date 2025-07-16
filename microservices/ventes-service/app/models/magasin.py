from sqlalchemy import Column, Integer, String
from app.db.database import Base


class Magasin(Base):
    __tablename__ = "magasins"

    id = Column(Integer, primary_key=True)
    nom = Column(String)
    adresse = Column(String)
    ville = Column(String)
