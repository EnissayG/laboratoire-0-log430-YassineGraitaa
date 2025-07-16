from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import CommandeCreate, CommandeOut
from app.services.checkout_service import valider_commande, lister_commandes
from app.db.database import get_session
from typing import List

router = APIRouter(prefix="/api/checkout", tags=["Check-out"])


@router.post("/", response_model=CommandeOut)
def create_commande(data: CommandeCreate, db: Session = Depends(get_session)):
    return valider_commande(data.dict(), db)


@router.get("/", response_model=List[CommandeOut])
def get_commandes(db: Session = Depends(get_session)):
    return lister_commandes(db)
