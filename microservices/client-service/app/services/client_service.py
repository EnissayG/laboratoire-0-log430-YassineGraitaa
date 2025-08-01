from sqlalchemy.orm import Session
from app.models.client import Client


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
