from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.models.produit import Produit


def afficher_tout_le_stock(session):
    return session.query(Produit).all()


def ajouter_produit(nom, categorie, prix, quantite_stock, magasin_id, db: Session):
    produit = Produit(
        nom=nom,
        categorie=categorie,
        prix=prix,
        quantite_stock=quantite_stock,
        magasin_id=magasin_id,
    )
    db.add(produit)
    db.commit()
    db.refresh(produit)
    return produit


def rechercher_produit(critere: str, session) -> list[Produit]:
    try:
        if critere.isdigit():
            produit = session.get(Produit, int(critere))
            return [produit] if produit else []

        return (
            session.query(Produit)
            .filter(
                or_(
                    Produit.nom.ilike(f"%{critere}%"),
                    Produit.categorie.ilike(f"%{critere}%"),
                )
            )
            .all()
        )
    except Exception as e:
        print(f"❌ Erreur : {e}")
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


def rechercher_produits_avances(page, size, sort, categorie, session):
    query = session.query(Produit)
    if categorie:
        query = query.filter(Produit.categorie.ilike(f"%{categorie}%"))

    try:
        sort_field, sort_order = sort.split(",")
    except ValueError:
        sort_field, sort_order = "nom", "asc"

    sort_col = getattr(Produit, sort_field, Produit.nom)
    query = query.order_by(sort_col.desc() if sort_order == "desc" else sort_col.asc())

    total = query.count()
    produits = query.offset((page - 1) * size).limit(size).all()

    return {
        "total": total,
        "page": page,
        "size": size,
        "produits": produits,
    }
