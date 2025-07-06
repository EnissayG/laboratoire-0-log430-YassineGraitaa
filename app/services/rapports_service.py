# app/services/rapports_service.py

from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.vente import Vente
from app.models.magasin import Magasin


def generer_rapport_ventes(db: Session, date_debut, date_fin):
    """
    Retourne un rapport de ventes groupé par magasin entre deux dates.
    """
    resultats = (
        db.query(
            Magasin.nom,
            func.count(Vente.id).label("nombre_ventes"),
            func.sum(Vente.total).label("total_ventes"),
        )
        .join(Vente, Vente.magasin_id == Magasin.id)
        .filter(Vente.date >= date_debut, Vente.date <= date_fin)
        .group_by(Magasin.nom)
        .all()
    )

    return [
        {"magasin": nom, "nombre_ventes": int(nb), "total_ventes": float(total)}
        for nom, nb, total in resultats
    ]
