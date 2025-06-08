from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_session
from app.schemas import ProduitUpdate
from app.services.produit_service import (
    afficher_tout_le_stock,
    rechercher_produit,
    ajouter_produit,
    modifier_produit,
)

router = APIRouter(prefix="/produits", tags=["Produits"])


@router.get("/")
def get_all(session: Session = Depends(get_session)):
    return afficher_tout_le_stock(session)


@router.get("/recherche")
def rechercher(critere: str, session: Session = Depends(get_session)):
    return rechercher_produit(critere, session)


@router.post("/")
def ajouter(
    nom: str,
    categorie: str,
    prix: float,
    quantite_stock: int,
    session: Session = Depends(get_session),
):
    return ajouter_produit(nom, categorie, prix, quantite_stock, session)


@router.put("/{produit_id}")
def update_produit(
    produit_id: int, update_data: ProduitUpdate, session: Session = Depends(get_session)
):
    updated = modifier_produit(
        produit_id, update_data.dict(exclude_unset=True), session
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    return updated
