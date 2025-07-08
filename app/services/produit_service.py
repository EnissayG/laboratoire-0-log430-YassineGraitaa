from __future__ import annotations  # Ajout essentiel
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.models import Produit, DemandeApprovisionnement


def afficher_tout_le_stock(session):
    return session.query(Produit).all()


def ajouter_produit(nom, categorie, prix, quantite_stock, magasin_id, db: Session):
    from app.models.produit import Produit

    produit = Produit(
        nom=nom,
        categorie=categorie,
        prix=prix,
        quantite_stock=quantite_stock,
        magasin_id=magasin_id,  # 🔥 ASSOCIER LE MAGASIN
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


def rechercher_produits_avances(page, size, sort, categorie, session):
    query = session.query(Produit)

    # 🔍 Filtrage
    if categorie:
        query = query.filter(Produit.categorie.ilike(f"%{categorie}%"))

    # 🔀 Tri robuste
    try:
        sort_field, sort_order = sort.split(",")
    except ValueError:
        sort_field, sort_order = "nom", "asc"

    sort_col = getattr(Produit, sort_field, Produit.nom)
    if sort_order == "desc":
        sort_col = sort_col.desc()
    else:
        sort_col = sort_col.asc()
    query = query.order_by(sort_col)

    total = query.count()
    produits = query.offset((page - 1) * size).limit(size).all()

    return {
        "total": total,
        "page": page,
        "size": size,
        "produits": produits,
    }


def creer_demande_approvisionnement(
    demande_data: dict, session: Session
) -> DemandeApprovisionnement:
    demande = DemandeApprovisionnement(
        produit_id=demande_data["produit_id"],
        quantite=demande_data["quantite"],
        magasin_id=demande_data["magasin_id"],
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
