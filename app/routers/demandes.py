from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db import get_session
from app.schemas import DemandeApprovisionnementIn, DemandeApprovisionnementOut
from app.services.produit_service import (
    creer_demande_approvisionnement,
    lister_demandes_approvisionnement,
)

router = APIRouter(prefix="/demandes", tags=["Demandes"])


@router.post("/", response_model=DemandeApprovisionnementOut)
def creer_demande(
    donnees: DemandeApprovisionnementIn, session: Session = Depends(get_session)
):
    from app.models import Produit

    produit = session.get(Produit, donnees.produit_id)
    if not produit:
        raise HTTPException(status_code=404, detail="Produit non trouvé")

    demande = creer_demande_approvisionnement(donnees.dict(), session)
    return demande


@router.get("/", response_model=List[DemandeApprovisionnementOut])
def get_demandes(session: Session = Depends(get_session)):
    return lister_demandes_approvisionnement(session)


@router.post("/traiter/{demande_id}")
def traiter_demande(demande_id: int, session: Session = Depends(get_session)):
    from app.services.produit_service import traiter_demande_approvisionnement

    resultat = traiter_demande_approvisionnement(demande_id, session)
    if not resultat:
        raise HTTPException(
            status_code=404, detail="Demande non trouvée ou déjà traitée"
        )

    return {"message": "Demande traitée avec succès"}
