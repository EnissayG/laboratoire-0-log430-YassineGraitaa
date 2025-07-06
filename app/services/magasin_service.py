from sqlalchemy.orm import Session
from app.models.magasin import Magasin
from app.models.produit import Produit


def creer_magasin(data: dict, db: Session) -> Magasin:
    try:
        magasin = Magasin(**data)
        if db.query(Magasin).filter_by(nom=data["nom"]).first():
            raise ValueError("Un magasin avec ce nom existe déjà.")
        db.add(magasin)
        db.commit()
        db.refresh(magasin)
        return magasin
    except Exception as e:
        print("🚨 ERREUR lors de la création du magasin :", e)
        raise


def get_stock_du_magasin(magasin_id: int, db: Session):
    magasin = db.get(Magasin, magasin_id)
    if not magasin:
        return None
    return db.query(Produit).filter(Produit.magasin_id == magasin_id).all()


def lister_magasins(db: Session):
    return db.query(Magasin).all()


def maj_magasin(id: int, data: dict, db: Session) -> Magasin | None:
    magasin = db.get(Magasin, id)
    if not magasin:
        return None
    for key, value in data.items():
        setattr(magasin, key, value)
    db.commit()
    db.refresh(magasin)
    return magasin


def supprimer_magasin(id: int, db: Session) -> bool:
    magasin = db.get(Magasin, id)
    if not magasin:
        return False
    db.delete(magasin)
    db.commit()
    return True
