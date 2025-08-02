from sqlalchemy.orm import Session
from app.models.evenement import Evenement
import json


def reconstruire_etat(aggregate_id: str, db: Session):
    events = (
        db.query(Evenement)
        .filter(Evenement.aggregate_id == aggregate_id)
        .order_by(Evenement.timestamp)
        .all()
    )

    etat = {}
    for e in events:
        data = json.loads(e.data)
        if e.event_type == "CommandeCreee":
            etat = data
        elif e.event_type == "StockReserve":
            etat["stock_ok"] = True
        elif e.event_type == "PaiementAccepte":
            etat["paiement_ok"] = True
        elif e.event_type == "VenteConfirmee":
            etat["terminee"] = True
        elif e.event_type in ["PaiementRefuse", "StockIndisponible"]:
            etat["annulee"] = True
    return etat
