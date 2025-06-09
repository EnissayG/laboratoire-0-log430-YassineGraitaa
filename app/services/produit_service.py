from __future__ import annotations  # Ajout essentiel
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.models import Produit, DemandeApprovisionnement


def afficher_tout_le_stock(session):
    return session.query(Produit).all()


def ajouter_produit(nom, categorie, prix, quantite_stock, session):
    produit = Produit(
        nom=nom, categorie=categorie, prix=prix, quantite_stock=quantite_stock
    )
    session.add(produit)
    session.commit()
    session.refresh(produit)  # <== pour recharger les données (ex: id généré)
    return produit


def rechercher_produit(critere: str, session) -> list[Produit]:
    try:
        if critere.isdigit():
            produit = session.get(Produit, int(critere))
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


def modifier_produit(produit_id: int, nouvelles_donnees: dict, session: Session):
    produit = session.get(Produit, produit_id)
    if not produit:
        return None

    for champ, valeur in nouvelles_donnees.items():
        if hasattr(produit, champ):
            setattr(produit, champ, valeur)

    session.commit()
    return produit


def creer_demande_approvisionnement(
    demande_data: dict, session: Session
) -> DemandeApprovisionnement:
    demande = DemandeApprovisionnement(
        produit_id=demande_data["produit_id"],
        quantite=demande_data["quantite"],
        magasin=demande_data["magasin"],
        statut="en_attente",
    )
    session.add(demande)
    session.commit()
    return demande


def lister_demandes_approvisionnement(session: Session):
    return session.query(DemandeApprovisionnement).all()


def traiter_demande_approvisionnement(demande_id: int, session: Session) -> bool:
    demande = session.get(DemandeApprovisionnement, demande_id)
    if not demande or demande.statut != "en_attente":
        return False

    produit = session.get(Produit, demande.produit_id)
    if not produit:
        return False

    produit.quantite_stock += demande.quantite
    demande.statut = "traitee"

    session.commit()
    return True
