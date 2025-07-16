from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_session
from app.services.stock_service import lister_stock, lister_stock_du_magasin
from app.schemas import ProduitStockDTO
from typing import List
import time

router = APIRouter(prefix="/api/stock", tags=["Stock"])

_stock_cache = {"data": None, "timestamp": 0}
CACHE_DURATION_SECONDS = 60


@router.get(
    "/",
    response_model=List[ProduitStockDTO],
    summary="Lister le stock global",
    description="Retourne tous les produits avec leurs quantités en stock dans chaque magasin.",
)
def get_stock(db: Session = Depends(get_session)):
    now = time.time()
    if now - _stock_cache["timestamp"] < CACHE_DURATION_SECONDS:
        return _stock_cache["data"]

    result = lister_stock(db)
    _stock_cache["data"] = result
    _stock_cache["timestamp"] = now
    return result


@router.get(
    "/magasin/{magasin_id}",
    response_model=List[ProduitStockDTO],
    summary="Stock par magasin",
    description="Retourne les produits et quantités pour un magasin donné.",
)
def get_stock_magasin(magasin_id: int, db: Session = Depends(get_session)):
    result = lister_stock_du_magasin(magasin_id, db)
    if result is None:
        raise HTTPException(status_code=404, detail="Magasin introuvable")
    return result
