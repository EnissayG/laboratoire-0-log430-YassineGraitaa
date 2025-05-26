from app.db import session
from app.models import Produit
from sqlalchemy import or_


def afficher_tout_le_stock():
    return session.query(Produit).all()


def rechercher_produit(critere: str) -> list[Produit]:
    """
    Recherche un produit par nom, catégorie ou identifiant.

    critere: peut être un mot (ex: "banane") ou un chiffre (ex: "1")

    Retourne une liste de Produits correspondants.
    """
    try:
        if critere.isdigit():
            produit = session.query(Produit).get(int(critere))
            return [produit] if produit else []

        results = (
            session.query(Produit)
            .filter(
                or_(
                    Produit.nom.ilike(f"%{critere}%"),
                    Produit.categorie.ilike(f"%{critere}%"),
                )
            )
            .all()
        )

        return results

    except Exception as e:
        print(f"❌ Erreur lors de la recherche : {e}")
        return []
