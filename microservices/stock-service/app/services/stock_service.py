from sqlalchemy.orm import Session
from app.models.produit import Produit
import httpx
import os

MAGASIN_SERVICE_URL = os.getenv("MAGASIN_SERVICE_URL", "http://magasin-service:8000")


def lister_stock(db: Session):
    return db.query(Produit).all()


def magasin_existe(magasin_id: int) -> bool:
    try:
        r = httpx.get(f"{MAGASIN_SERVICE_URL}/api/magasins/{magasin_id}", timeout=5)
        return r.status_code == 200
    except Exception as e:
        print(f"❌ Erreur réseau ou magasin indisponible : {e}")
        return False


def lister_stock_du_magasin(magasin_id: int, db: Session):
    if not magasin_existe(magasin_id):
        return None
    return db.query(Produit).filter(Produit.magasin_id == magasin_id).all()


def reserver_produits(produits: list[dict], db: Session) -> bool:
    for item in produits:
        produit = db.get(Produit, item["produit_id"])
        if not produit or produit.quantite_stock < item["quantite"]:
            return False
    for item in produits:
        produit = db.get(Produit, item["produit_id"])
        produit.quantite_stock -= item["quantite"]
    db.commit()
    return True


def liberer_produits(produits: list[dict], db: Session):
    for item in produits:
        produit = db.get(Produit, item["produit_id"])
        if produit:
            produit.quantite_stock += item["quantite"]
    db.commit()
