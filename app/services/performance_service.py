from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Date
from app.models.vente import Vente
from app.models.magasin import Magasin
from app.models.lignevente import LigneVente
from app.models.produit import Produit


def calculer_performance_globale(db: Session):
    total_ventes = db.query(func.sum(Vente.total)).scalar() or 0.0

    produits_vendus = [
        {
            "nom": nom,
            "categorie": categorie,
            "quantite": int(quantite),
        }
        for nom, categorie, quantite in db.query(
            Produit.nom,
            Produit.categorie,
            func.sum(LigneVente.quantite).label("quantite"),
        )
        .join(LigneVente.produit)
        .group_by(Produit.nom, Produit.categorie)
        .order_by(func.sum(LigneVente.quantite).desc())
        .limit(5)
        .all()
    ]

    ruptures = [
        {
            "nom": produit.nom,
            "categorie": produit.categorie,
            "stock": produit.quantite_stock,
        }
        for produit in db.query(Produit).filter(Produit.quantite_stock == 0).all()
    ]

    surstocks = [
        {
            "nom": produit.nom,
            "categorie": produit.categorie,
            "stock": produit.quantite_stock,
        }
        for produit in db.query(Produit).filter(Produit.quantite_stock > 50).all()
    ]

    ventes_par_magasin = [
        {
            "magasin": magasin,
            "nombre_ventes": int(nb),
            "total": float(total),
        }
        for magasin, nb, total in db.query(
            Magasin.nom, func.count(Vente.id), func.sum(Vente.total)
        )
        .join(Vente, Vente.magasin_id == Magasin.id)
        .group_by(Magasin.nom)
        .all()
    ]

    tendance_journaliere = [
        {"jour": str(jour), "total": float(total)}
        for jour, total in db.query(cast(Vente.date, Date), func.sum(Vente.total))
        .group_by(cast(Vente.date, Date))
        .order_by(cast(Vente.date, Date))
        .limit(30)
        .all()
    ]

    return {
        "total_ventes": float(total_ventes),
        "produits": produits_vendus,
        "ruptures": ruptures,
        "surstocks": surstocks,
        "ventes_par_magasin": ventes_par_magasin,
        "tendance_journaliere": tendance_journaliere,
    }
