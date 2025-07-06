from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db import get_session
from app.schemas import DemandeApprovisionnementIn, DemandeApprovisionnementOut
from app.services.produit_service import (
    creer_demande_approvisionnement,
    lister_demandes_approvisionnement,
    traiter_demande_approvisionnement,
)
from app.models import Produit

router = APIRouter(prefix="/api/demandes", tags=["Demandes d’approvisionnement"])


@router.post(
    "/",
    response_model=DemandeApprovisionnementOut,
    status_code=201,
    summary="Créer une demande d’approvisionnement",
    description="Crée une nouvelle demande d’approvisionnement pour un produit donné dans un magasin.",
)
def creer_demande(
    donnees: DemandeApprovisionnementIn, session: Session = Depends(get_session)
):
    produit = session.get(Produit, donnees.produit_id)
    if not produit:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    return creer_demande_approvisionnement(donnees.dict(), session)


@router.get(
    "/",
    response_model=List[DemandeApprovisionnementOut],
    summary="Lister toutes les demandes",
    description="Retourne toutes les demandes d’approvisionnement enregistrées dans le système.",
)
def get_demandes(session: Session = Depends(get_session)):
    return lister_demandes_approvisionnement(session)


@router.post(
    "/traiter/{demande_id}",
    status_code=200,
    summary="Traiter une demande",
    description="Valide une demande d’approvisionnement : met son statut à 'traitée' et met à jour le stock.",
)
def traiter_demande(demande_id: int, session: Session = Depends(get_session)):
    resultat = traiter_demande_approvisionnement(demande_id, session)
    if not resultat:
        raise HTTPException(
            status_code=404, detail="Demande non trouvée ou déjà traitée"
        )
    return {"message": "Demande traitée avec succès"}
