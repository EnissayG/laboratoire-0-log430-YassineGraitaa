from sqlalchemy.orm import Session
from app.models.commande import Commande


def valider_commande(data: dict, db: Session):
    commande = Commande(**data)
    db.add(commande)
    db.commit()
    db.refresh(commande)
    return commande


def lister_commandes(db: Session):
    return db.query(Commande).all()
