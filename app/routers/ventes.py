from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_session
from app.services.vente_service import (
    enregistrer_vente,
    annuler_vente,
    lister_ventes,
    generer_rapport,
)

router = APIRouter(prefix="/ventes", tags=["Ventes"])


@router.get("/")
def get_ventes(session: Session = Depends(get_session)):
    return lister_ventes(session)


@router.get("/rapport")
def rapport_global(session: Session = Depends(get_session)):
    return generer_rapport(session)


@router.post("/")
def creer_vente(data: dict, session: Session = Depends(get_session)):
    """
    Body attendu :
    {
      "magasin": "Montréal",
      "panier": [
          {"produit_id": 1, "quantite": 2},
          {"produit_id": 3, "quantite": 1}
      ]
    }
    """
    try:
        panier = data["panier"]
        magasin = data["magasin"]
    except KeyError:
        raise HTTPException(
            status_code=422, detail="Le body doit contenir 'magasin' et 'panier'."
        )

    vente = enregistrer_vente(panier, magasin, session)
    if not vente:
        raise HTTPException(
            status_code=400, detail="Erreur lors de l'enregistrement de la vente."
        )
    return {"message": "Vente enregistrée", "vente_id": vente.id, "total": vente.total}


@router.delete("/{vente_id}")
def supprimer_vente(vente_id: int, session: Session = Depends(get_session)):
    success = annuler_vente(vente_id, session)
    if not success:
        raise HTTPException(
            status_code=404, detail="Vente introuvable ou déjà annulée."
        )
    return {"message": "Vente annulée"}
