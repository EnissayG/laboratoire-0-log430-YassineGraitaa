from sqlalchemy.orm import Session
from app.models.produit import Produit
from app.db.database import get_session
from sqlalchemy.orm import Session
from .publisher import publier_evenement_stock
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


async def reserver_produits(commande: dict, db: Session):
    produits_commande = commande["produits"]
    client_id = commande["client_id"]

    for produit in produits_commande:
        produit_id = produit["produit_id"]
        quantite_demandee = produit["quantite"]

        produit_stock = db.query(Produit).filter(Produit.id == produit_id).first()

        if not produit_stock:
            await publier_evenement_stock(
                "StockIndisponible",
                {
                    "produit_id": produit_id,
                    "raison": "Produit introuvable",
                    "commande": commande,
                },
            )
            raise Exception(f"Produit ID {produit_id} introuvable.")

        if produit_stock.quantite_stock < quantite_demandee:
            await publier_evenement_stock(
                "StockIndisponible",
                {
                    "produit_id": produit_id,
                    "stock_disponible": produit_stock.quantite_stock,
                    "quantite_demandee": quantite_demandee,
                    "commande": commande,
                },
            )
            raise Exception(f"Stock insuffisant pour {produit_stock.nom}")

        produit_stock.quantite_stock -= quantite_demandee

    db.commit()

    await publier_evenement_stock(
        "StockReserve",
        {
            "client_id": client_id,
            "produits": produits_commande,
            "total": commande["total"],
        },
    )

    print(f"[stock-service] Stock réservé et événement publié.")
    return True


async def liberer_produits(commande: dict, db: Session = None):
    if db is None:
        db = next(get_session())
    produits_commande = commande["commande"]["produits"]

    for produit in produits_commande:
        produit_id = produit["produit_id"]
        quantite = produit["quantite"]

        produit_stock = db.query(Produit).filter(Produit.id == produit_id).first()

        if produit_stock:
            produit_stock.quantite_stock += quantite  # remettre la quantité
        else:
            print(
                f"[stock-service] Produit {produit_id} introuvable, impossible de libérer"
            )

    db.commit()
    print(f"[stock-service] Stock libéré pour commande refusée")
