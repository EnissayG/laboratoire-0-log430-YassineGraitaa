from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session  # ✅ Ajout nécessaire
from datetime import datetime
from sqlalchemy import func

from app.models import Produit, Vente, LigneVente


def enregistrer_vente(
    produits_selectionnes: list[dict], magasin: str, session: Session
) -> Vente | None:
    """
    Enregistre une vente complète avec lignes de vente et mise à jour de stock.

    produits_selectionnes: list of {"produit_id": int, "quantite": int}
    Exemple :
        [
            {"produit_id": 1, "quantite": 2},
            {"produit_id": 3, "quantite": 1}
        ]
    """
    try:
        total = 0
        lignes = []

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
            date=datetime.utcnow(), total=total, lignes=lignes, magasin=magasin
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

    # Total des ventes
    total_ventes = session.query(func.sum(Vente.total)).scalar() or 0
    rapport["total_ventes"] = float(total_ventes)

    # Produits les plus vendus
    produits = (
        session.query(
            Produit.nom,
            func.sum(LigneVente.quantite).label("quantite_totale"),
            func.sum(LigneVente.sous_total).label("revenu_total"),
        )
        .join(LigneVente, LigneVente.produit_id == Produit.id)
        .group_by(Produit.nom)
        .order_by(func.sum(LigneVente.quantite).desc())
        .all()
    )
    rapport["produits"] = [
        {"nom": nom, "quantite": int(q), "revenu": float(r)} for nom, q, r in produits
    ]

    # Produits en rupture
    ruptures = session.query(Produit).filter(Produit.quantite_stock == 0).all()
    rapport["ruptures"] = [{"nom": p.nom, "categorie": p.categorie} for p in ruptures]

    # Produits en surstock (seuil arbitraire : > 50 unités)
    surstocks = session.query(Produit).filter(Produit.quantite_stock > 50).all()
    rapport["surstocks"] = [
        {"nom": p.nom, "stock": p.quantite_stock} for p in surstocks
    ]

    # Chiffre d'affaires par magasin
    ventes_par_magasin = (
        session.query(Vente.magasin, func.sum(Vente.total).label("total"))
        .group_by(Vente.magasin)
        .all()
    )
    rapport["ventes_par_magasin"] = [
        {"magasin": m, "total": float(t)} for m, t in ventes_par_magasin
    ]

    return rapport


def annuler_vente(vente_id: int, session: Session) -> bool:
    """
    Annule une vente : supprime la vente et remet les quantités dans le stock.

    Retourne True si succès, False sinon.
    """
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
