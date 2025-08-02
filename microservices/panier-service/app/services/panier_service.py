from sqlalchemy.orm import Session
from app.models.panier import Panier
from .publisher import publier_commande_creee


def ajouter_au_panier(data: dict, db: Session) -> Panier:
    panier = Panier(**data)
    db.add(panier)
    db.commit()
    db.refresh(panier)
    return panier


def get_panier_client(client_id: int, db: Session):
    return db.query(Panier).filter(Panier.client_id == client_id).all()


def supprimer_article(panier_id: int, db: Session) -> bool:
    panier = db.get(Panier, panier_id)
    if not panier:
        return False
    db.delete(panier)
    db.commit()
    return True


def vider_panier(client_id: int, db: Session):
    db.query(Panier).filter(Panier.client_id == client_id).delete()
    db.commit()


async def creer_commande_depuis_panier(panier_id: int, db: Session):
    # Récupérer l'entrée panier par ID
    ligne_panier = db.query(Panier).filter(Panier.id == panier_id).first()
    if not ligne_panier:
        raise Exception(f"Panier avec ID {panier_id} introuvable.")

    client_id = ligne_panier.client_id

    # Récupérer tous les produits du client
    panier_client = db.query(Panier).filter(Panier.client_id == client_id).all()

    if not panier_client:
        raise Exception(f"Aucun panier trouvé pour le client ID {client_id}.")

    # Construire les produits
    produits = [
        {
            "produit_id": ligne.produit_id,
            "nom": ligne.nom_produit,
            "quantite": ligne.quantite,
            "prix_unitaire": ligne.prix_unitaire,
            "sous_total": ligne.quantite * ligne.prix_unitaire,
        }
        for ligne in panier_client
    ]

    total = sum(p["sous_total"] for p in produits)

    commande = {"client_id": client_id, "produits": produits, "total": total}

    # Publier l’événement dans Redis Stream
    await publier_commande_creee(commande)

    return commande  # Optionnel, utile pour debug/test
