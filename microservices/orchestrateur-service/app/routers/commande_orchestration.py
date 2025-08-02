from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from app.db.database import get_session
from app.models.commande import Commande
from app.models.etat_saga import EtatSaga
from app.schemas import CommandeInput
from app.services.saga_checkout import executer_saga

router = APIRouter(prefix="/api/commande")


@router.post("/checkout", summary="Effectuer une commande complète via saga orchestrée")
async def checkout(commande: CommandeInput):
    return await executer_saga(commande)


@router.get(
    "/{id}",
    summary="Consulter une commande",
    description="Retourne l’état actuel d’une commande.",
)
def get_commande(id: UUID, db: Session = Depends(get_session)):
    commande = db.query(Commande).filter_by(id=id).first()
    if not commande:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    return {
        "id": str(commande.id),
        "client_id": commande.client_id,
        "magasin_id": commande.magasin_id,
        "etat_actuel": commande.etat_actuel,
    }


@router.get(
    "/{id}/historique",
    summary="Consulter l’historique d’une commande",
    description="Liste les transitions d’état de la commande.",
)
def historique_commande(id: UUID, db: Session = Depends(get_session)):
    lignes = db.query(EtatSaga).filter_by(saga_id=id).order_by(EtatSaga.timestamp).all()
    if not lignes:
        raise HTTPException(
            status_code=404, detail="Historique non trouvé pour cette commande"
        )
    return [
        {"etat": ligne.etat, "timestamp": ligne.timestamp.isoformat()}
        for ligne in lignes
    ]
