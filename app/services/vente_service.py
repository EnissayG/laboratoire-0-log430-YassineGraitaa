from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy import func, cast, Date

from app.models import Produit, Vente, LigneVente, Magasin  # ✅ Magasin importé


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
        if not magasin:
            raise ValueError(f"Magasin ID {magasin_id} introuvable.")

        for item in produits_selectionnes:
            produit = session.get(Produit, item["produit_id"])
            quantite = item["quantite"]

            if not produit:
                raise ValueError(f"Produit ID {item['produit_id']} introuvable.")
            if produit.quantite_stock < quantite:
                raise ValueError(f"Stock insuffisant pour {produit.nom}.")

            sous_total = quantite * produit.prix
            total += sous_total

            ligne = LigneVente(
                produit_id=produit.id, quantite=quantite, sous_total=sous_total
            )
            lignes.append(ligne)
            produit.quantite_stock -= quantite

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

        return vente

    except (SQLAlchemyError, ValueError) as e:
        session.rollback()
        print(f"❌ Erreur : {e}")
        return None


def lister_ventes(session: Session):
    return session.query(Vente).all()


def generer_rapport(session: Session):
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
    rapport["ruptures"] = [{"nom": p.nom, "categorie": p.categorie} for p in ruptures]

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
        return True

    except Exception as e:
        session.rollback()
        print("❌ Erreur lors de l’annulation :", e)
        return False
