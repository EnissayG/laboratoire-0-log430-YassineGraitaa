from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_session
from app.models.evenement import Evenement
from app.schemas import EvenementIn
from datetime import datetime
from app.services.projection import reconstruire_etat
import json
from fastapi.encoders import jsonable_encoder

router = APIRouter(prefix="/events", tags=["Event Store"])


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
    return {"message": "Événement stocké"}


@router.get("/projections/{aggregate_id}")
def projection(aggregate_id: str, db: Session = Depends(get_session)):
    return reconstruire_etat(aggregate_id, db)
