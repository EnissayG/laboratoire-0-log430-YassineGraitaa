from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_session
from app.models.evenement import Evenement
from app.schemas import EvenementIn
from datetime import datetime
from app.services.projection import reconstruire_etat
from fastapi.encoders import jsonable_encoder
from prometheus_client import Counter
import json
from app.schemas import EvenementOut
from typing import List


router = APIRouter(prefix="/events", tags=["Event Store"])

# ✅ Déclaration du compteur Prometheus
event_store_events_total = Counter(
    "event_store_events_total",  # Nom du compteur (visible dans /metrics)
    "Nombre total d’événements enregistrés",  # Description
    ["event_type", "source"],  # Labels pour filtrer/compter
)


@router.get("/", response_model=List[EvenementOut])
def lister_evenements(db: Session = Depends(get_session)):
    evenements = db.query(Evenement).order_by(Evenement.timestamp.desc()).all()

    # 🔁 On convertit chaque `data` (str) en dict JSON
    result = []
    for e in evenements:
        item = e.__dict__.copy()
        item["data"] = json.loads(e.data)
        result.append(item)

    return result


@router.post("/")
def enregistrer_evenement(event: EvenementIn, db: Session = Depends(get_session)):
    e = Evenement(
        event_type=event.event_type,
        aggregate_id=event.aggregate_id,
        data=json.dumps(jsonable_encoder(event.data)),
        timestamp=event.timestamp or datetime.utcnow(),
        source=event.source,
    )
    db.add(e)
    db.commit()

    # ✅ Incrément Prometheus avec labels
    event_store_events_total.labels(
        event_type=event.event_type, source=event.source or "inconnu"
    ).inc()

    return {"message": "Événement stocké"}


@router.get("/projections/{aggregate_id}")
def projection(aggregate_id: str, db: Session = Depends(get_session)):
    return reconstruire_etat(aggregate_id, db)
