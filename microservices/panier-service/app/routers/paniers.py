from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import PanierCreate, PanierDTO
from app.services.panier_service import (
    ajouter_au_panier,
    get_panier_client,
    supprimer_article,
    vider_panier,
    creer_commande_depuis_panier,
)
from app.db.database import get_session
from typing import List

router = APIRouter(prefix="/api/panier", tags=["Panier"])


@router.post("/", response_model=PanierDTO)
def ajouter(data: PanierCreate, db: Session = Depends(get_session)):
    return ajouter_au_panier(data.dict(), db)


@router.get("/{client_id}", response_model=List[PanierDTO])
def consulter(client_id: int, db: Session = Depends(get_session)):
    return get_panier_client(client_id, db)


@router.delete("/{panier_id}", status_code=204)
def supprimer(panier_id: int, db: Session = Depends(get_session)):
    if not supprimer_article(panier_id, db):
        raise HTTPException(status_code=404, detail="Article non trouvé")


@router.delete("/client/{client_id}", status_code=204)
def vider(client_id: int, db: Session = Depends(get_session)):
    vider_panier(client_id, db)


@router.post("/commande/depuis-panier/{panier_id}")
async def checkout_depuis_panier(panier_id: int, db: Session = Depends(get_session)):
    await creer_commande_depuis_panier(panier_id, db)
    return {"message": "Événement CommandeCreee publié avec succès"}
