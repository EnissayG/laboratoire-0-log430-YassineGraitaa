from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_session
from app.services.client_service import (
    creer_client,
    get_client,
    lister_clients,
    payer_client,
    rembourser_client,
)
from app.schemas import ClientDTO, ClientCreate, Paiement

router = APIRouter(prefix="/api/clients", tags=["Clients"])


@router.post("/", response_model=ClientDTO)
def creer(data: ClientCreate, db: Session = Depends(get_session)):
    return creer_client(data.dict(), db)


@router.get("/{id}", response_model=ClientDTO)
def lire(id: int, db: Session = Depends(get_session)):
    client = get_client(id, db)
    if not client:
        raise HTTPException(status_code=404, detail="Client introuvable")
    return client


@router.get("/", response_model=List[ClientDTO])
def liste(db: Session = Depends(get_session)):
    return lister_clients(db)


@router.post("/{client_id}/payer")
def debiter(client_id: int, paiement: Paiement, db: Session = Depends(get_session)):
    success = payer_client(client_id, paiement.montant, db)
    if not success:
        raise HTTPException(status_code=400, detail="Solde insuffisant")
    return {"message": "Paiement effectué"}


@router.post("/{client_id}/rembourser")
def rembourser(client_id: int, paiement: Paiement, db: Session = Depends(get_session)):
    rembourser_client(client_id, paiement.montant, db)
    return {"message": "Remboursement effectué"}
