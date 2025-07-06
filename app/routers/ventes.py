from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_session
from app.services.vente_service import (
    enregistrer_vente,
    annuler_vente,
    lister_ventes,
    generer_rapport,
)
from app.schemas import VenteOut, VenteRapportDTO, MessageResponse
from app.schemas import PerformanceGlobaleDTO

from typing import List

router = APIRouter(prefix="/api/ventes", tags=["Ventes"])


@router.get(
    "/",
    response_model=List[VenteOut],
    summary="Lister toutes les ventes",
    description="Retourne la liste complète des ventes enregistrées dans tous les magasins.",
)
def get_ventes(session: Session = Depends(get_session)):
    return lister_ventes(session)


@router.get(
    "/rapport",
    response_model=PerformanceGlobaleDTO,  # ✅ correct ici
    summary="Générer un rapport global des ventes",
    description="Retourne un rapport contenant le chiffre d’affaires global par produit et par magasin.",
)
def rapport_global(session: Session = Depends(get_session)):
    return generer_rapport(session)


@router.post(
    "/",
    status_code=201,
    response_model=MessageResponse,
    summary="Enregistrer une nouvelle vente",
    description="""
Crée une vente dans un magasin donné.

Body attendu :
```json
{
  "magasin_id": 1,
  "date": "2025-07-02",  // optionnel
  "panier": [
    { "produit_id": 1, "quantite": 2 },
    { "produit_id": 3, "quantite": 1 }
  ]
}
""",
)
def creer_vente(data: dict, session: Session = Depends(get_session)):
    try:
        panier = data["panier"]
        magasin_id = data["magasin_id"]
        date_vente = data.get("date")
    except KeyError:
        raise HTTPException(
            status_code=422, detail="Le body doit contenir 'magasin_id' et 'panier'."
        )

    vente = enregistrer_vente(panier, magasin_id, session, date_vente)
    if not vente:
        raise HTTPException(
            status_code=400, detail="Erreur lors de l'enregistrement de la vente."
        )
    return {"message": "Vente enregistrée", "vente_id": vente.id, "total": vente.total}


@router.delete(
    "/{vente_id}",
    status_code=200,
    response_model=MessageResponse,
    summary="Annuler une vente",
    description="Annule une vente en la supprimant du système si elle n’a pas déjà été annulée.",
)
def supprimer_vente(vente_id: int, session: Session = Depends(get_session)):
    success = annuler_vente(vente_id, session)
    if not success:
        raise HTTPException(
            status_code=404, detail="Vente introuvable ou déjà annulée."
        )
    return {"message": "Vente annulée"}
