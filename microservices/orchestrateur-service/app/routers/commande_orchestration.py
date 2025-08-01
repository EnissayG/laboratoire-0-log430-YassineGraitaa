from fastapi import APIRouter
from app.models.commande_saga import CommandeInput
from app.services.saga_checkout import executer_saga

router = APIRouter(prefix="/orchestration", tags=["Commande"])


@router.post("/commande")
async def orchestrer_commande(commande: CommandeInput):
    etat_final = await executer_saga(commande)
    return {"etat_final": etat_final}
