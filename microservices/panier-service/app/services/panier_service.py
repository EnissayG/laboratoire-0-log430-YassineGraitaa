from sqlalchemy.orm import Session
from app.models.panier import Panier


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
