# app/services/stock_service.py

from sqlalchemy.orm import Session
from app.models.produit import Produit


def lister_stock(db: Session):
    return db.query(Produit).all()
