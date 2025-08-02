from sqlalchemy.orm import Session
from app.models.client import Client
import random
from .publisher import publier_evenement_paiement


def creer_client(data: dict, db: Session) -> Client:
    client = Client(**data)
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


def get_client(id: int, db: Session) -> Client | None:
    return db.get(Client, id)


def lister_clients(db: Session):
    return db.query(Client).all()


def payer_client(client_id: int, montant: float, db: Session) -> bool:
    client = db.get(Client, client_id)
    if not client or client.solde < montant:
        return False
    client.solde -= montant
    db.commit()
    return True


def rembourser_client(client_id: int, montant: float, db: Session):
    client = db.get(Client, client_id)
    if client:
        client.solde += montant
        db.commit()


async def debiter_client(commande: dict):
    client_id = commande["client_id"]
    montant = commande["total"]

    # Simulation naïve (ex: refus si montant impair)
    paiement_accepte = random.choice([True, False])

    if paiement_accepte:
        await publier_evenement_paiement(
            "PaiementAccepte",
            {"client_id": client_id, "montant": montant, "commande": commande},
        )
        print(f"[client-service] Paiement accepté client {client_id}")
    else:
        await publier_evenement_paiement(
            "PaiementRefuse",
            {"client_id": client_id, "motif": "Simulation refus", "commande": commande},
        )
        print(f"[client-service] Paiement refusé client {client_id}")
