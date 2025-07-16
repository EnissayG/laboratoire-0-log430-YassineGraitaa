from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy import func, cast, Date
import httpx
import os
from app.models.produit import Produit
from app.models.vente import Vente
from app.models.lignevente import LigneVente
from app.models.magasin import Magasin

# Cache local (valide tant que l'app tourne)
_cached_rapport = None

MAGASIN_SERVICE_URL = os.getenv("MAGASIN_SERVICE_URL", "http://magasin-service:8000")
PRODUIT_SERVICE_URL = os.getenv("PRODUIT_SERVICE_URL", "http://produits-service:8000")


def verifier_magasin_existe(magasin_id: int) -> bool:
    try:
        r = httpx.get(f"{MAGASIN_SERVICE_URL}/api/magasins/{magasin_id}", timeout=5)
        return r.status_code == 200
    except httpx.RequestError as e:
        print(f"❌ Erreur réseau avec magasin-service : {e}")
        return False


def obtenir_produit(produit_id: int):
    try:
        r = httpx.get(
            f"{PRODUIT_SERVICE_URL}/api/produits/recherche?critere={produit_id}",
            timeout=5,
        )
        if r.status_code == 200:
            data = r.json()
            return data[0] if data else None
        return None
    except httpx.RequestError as e:
        print(f"❌ Erreur réseau avec produit-service : {e}")
        return None


def reset_cache_rapport():
    global _cached_rapport
    _cached_rapport = None


def enregistrer_vente(
    produits_selectionnes: list[dict],
    magasin_id: int,
    session: Session,
    date_vente=None,
) -> Vente | None:
    try:
        total = 0
        lignes = []

        magasin = session.get(Magasin, magasin_id)
        if not verifier_magasin_existe(magasin_id):
            raise ValueError(f"Magasin ID {magasin_id} introuvable.")

        for item in produits_selectionnes:
            produit_data = obtenir_produit(item["produit_id"])
            if not produit_data:
                raise ValueError(f"Produit ID {item['produit_id']} introuvable.")

            quantite = item["quantite"]
            if produit_data["quantite_stock"] < quantite:
                raise ValueError(f"Stock insuffisant pour {produit_data['nom']}.")

            sous_total = quantite * produit_data["prix"]
            total += sous_total

            ligne = LigneVente(
                produit_id=produit_data["id"],
                quantite=quantite,
                sous_total=sous_total,
            )
            lignes.append(ligne)
            try:
                r = httpx.put(
                    f"{PRODUIT_SERVICE_URL}/api/produits/{produit_data['id']}/decrementer_stock",
                    params={"quantite": quantite},
                    timeout=5,
                )
                if r.status_code != 200:
                    raise ValueError(
                        f"Erreur lors de la décrémentation du stock : {r.text}"
                    )
            except httpx.RequestError as e:
                print(f"❌ Erreur HTTP pour décrémenter stock : {e}")
                raise ValueError("Erreur réseau lors de la mise à jour du stock")

        vente = Vente(
            date=(
                datetime.fromisoformat(date_vente) if date_vente else datetime.utcnow()
            ),
            total=total,
            lignes=lignes,
            magasin_id=magasin_id,
        )
        session.add(vente)
        session.commit()

        reset_cache_rapport()  # Invalide le cache si vente ajoutée

        return vente

    except (SQLAlchemyError, ValueError) as e:
        session.rollback()
        print(f"❌ Erreur : {e}")
        return None


def lister_ventes(session: Session):
    return session.query(Vente).all()


def generer_rapport(session: Session):
    global _cached_rapport
    if _cached_rapport is not None:
        return _cached_rapport

    rapport = {}

    total_ventes = session.query(func.sum(Vente.total)).scalar() or 0
    rapport["total_ventes"] = float(total_ventes)

    produits = (
        session.query(
            Produit.nom,
            Produit.categorie,
            func.sum(LigneVente.quantite).label("quantite_totale"),
            func.sum(LigneVente.sous_total).label("revenu_total"),
        )
        .join(LigneVente, LigneVente.produit_id == Produit.id)
        .group_by(Produit.nom, Produit.categorie)
        .order_by(func.sum(LigneVente.quantite).desc())
        .all()
    )
    rapport["produits"] = [
        {"nom": nom, "categorie": cat, "quantite": int(q), "revenu": float(r)}
        for nom, cat, q, r in produits
    ]

    ruptures = session.query(Produit).filter(Produit.quantite_stock == 0).all()
    rapport["ruptures"] = [
        {"nom": p.nom, "categorie": p.categorie, "stock": p.quantite_stock}
        for p in ruptures
    ]

    surstocks = session.query(Produit).filter(Produit.quantite_stock > 50).all()
    rapport["surstocks"] = [
        {"nom": p.nom, "categorie": p.categorie, "stock": p.quantite_stock}
        for p in surstocks
    ]

    ventes_par_magasin = (
        session.query(Magasin.nom, func.sum(Vente.total).label("total"))
        .join(Vente)
        .group_by(Magasin.nom)
        .all()
    )
    rapport["ventes_par_magasin"] = [
        {"magasin": m, "total": float(t)} for m, t in ventes_par_magasin
    ]

    tendance = (
        session.query(
            cast(Vente.date, Date).label("jour"), func.sum(Vente.total).label("total")
        )
        .group_by(cast(Vente.date, Date))
        .order_by(cast(Vente.date, Date))
        .all()
    )
    rapport["tendance_journaliere"] = [
        {"jour": str(jour), "total": float(total)} for jour, total in tendance
    ]

    _cached_rapport = rapport
    return rapport


def annuler_vente(vente_id: int, session: Session) -> bool:
    try:
        vente = session.get(Vente, vente_id)
        if not vente:
            return False

        for ligne in vente.lignes:
            produit = session.get(Produit, ligne.produit_id)
            if produit:
                produit.quantite_stock += ligne.quantite

        session.delete(vente)
        session.commit()

        reset_cache_rapport()  # Invalide le cache si vente supprimée

        return True

    except Exception as e:
        session.rollback()
        print("❌ Erreur lors de l’annulation :", e)
        return False
