from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_session
from app.services.client_service import creer_client, get_client, lister_clients
from app.schemas import ClientDTO, ClientCreate

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
