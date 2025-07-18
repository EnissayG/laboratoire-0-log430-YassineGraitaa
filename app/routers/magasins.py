from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_session
import time
from app.schemas import MagasinDTO, MagasinCreate, ProduitStockDTO
from app.services.magasin_service import (
    creer_magasin,
    lister_magasins,
    maj_magasin,
    supprimer_magasin,
    get_stock_du_magasin,
)
from typing import List

router = APIRouter(prefix="/api/magasins", tags=["Magasins"])

# Cache
_magasins_cache = {"data": None, "timestamp": 0}
_stock_par_magasin_cache = {}
CACHE_DURATION = 60


@router.post(
    "/",
    response_model=MagasinDTO,
    summary="Créer un magasin",
    description="Ajoute un nouveau magasin dans la base de données.",
)
def post_magasin(data: MagasinCreate, db: Session = Depends(get_session)):
    return creer_magasin(data.dict(), db)


@router.get(
    "/",
    response_model=List[MagasinDTO],
    summary="Lister tous les magasins",
    description="Retourne la liste de tous les magasins enregistrés.",
)
def get_magasins(db: Session = Depends(get_session)):
    now = time.time()
    if now - _magasins_cache["timestamp"] < CACHE_DURATION:
        return _magasins_cache["data"]

    data = lister_magasins(db)
    _magasins_cache["data"] = data
    _magasins_cache["timestamp"] = now
    return data


@router.get(
    "/{id}/stock",
    response_model=List[ProduitStockDTO],
    summary="Afficher le stock d’un magasin",
    description="Retourne les produits en stock pour un magasin spécifique (via son ID).",
)
def get_stock_magasin(id: int, db: Session = Depends(get_session)):
    now = time.time()
    cache = _stock_par_magasin_cache.get(id)

    if cache and now - cache["timestamp"] < CACHE_DURATION:
        return cache["data"]

    produits = get_stock_du_magasin(id, db)
    if produits is None:
        raise HTTPException(status_code=404, detail="Magasin introuvable")

    _stock_par_magasin_cache[id] = {"data": produits, "timestamp": now}
    return produits


@router.put(
    "/{id}",
    response_model=MagasinDTO,
    summary="Modifier un magasin",
    description="Met à jour les informations d’un magasin existant (nom, adresse, etc.).",
)
def update_magasin(id: int, data: MagasinCreate, db: Session = Depends(get_session)):
    magasin = maj_magasin(id, data.dict(), db)
    if not magasin:
        raise HTTPException(status_code=404, detail="Magasin introuvable")
    return magasin


@router.delete(
    "/{id}",
    status_code=200,
    summary="Supprimer un magasin",
    description="Supprime un magasin s’il existe dans la base de données.",
)
def delete_magasin(id: int, db: Session = Depends(get_session)):
    if not supprimer_magasin(id, db):
        raise HTTPException(status_code=404, detail="Magasin introuvable")
    return {"message": "Magasin supprimé"}
