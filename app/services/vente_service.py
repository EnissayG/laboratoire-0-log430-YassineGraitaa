from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

from app.db import session
from app.models import Produit, Vente, LigneVente


def annuler_vente(vente_id: int) -> bool:
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


def enregistrer_vente(produits_selectionnes: list[dict]) -> Vente | None:
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
                produit_id=produit.id,
                quantite=quantite,
                sous_total=sous_total
            )
            lignes.append(ligne)
            produit.quantite_stock -= quantite

        vente = Vente(date=datetime.utcnow(), total=total, lignes=lignes)
        session.add(vente)
        session.commit()

        return vente

    except (SQLAlchemyError, ValueError) as e:
        session.rollback()
        print(f"❌ Erreur : {e}")
        return None
