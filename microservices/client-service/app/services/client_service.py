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
