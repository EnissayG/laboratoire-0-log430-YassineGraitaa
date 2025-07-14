from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_session
from app.services.stock_service import lister_stock
from app.schemas import ProduitStockDTO
from typing import List
import time

router = APIRouter(prefix="/api/stock", tags=["Stock"])

# 🧠 Cache mémoire local simple
_stock_cache = {"data": None, "timestamp": 0}
CACHE_DURATION_SECONDS = 60  # durée de vie du cache (1 min)


@router.get(
    "/",
    response_model=List[ProduitStockDTO],
    summary="Lister le stock global",
    description="Retourne tous les produits avec leurs quantités en stock dans chaque magasin.",
)
def get_stock(db: Session = Depends(get_session)):
    now = time.time()

    # ⚡ Retourne les données du cache si elles sont encore valides
    if now - _stock_cache["timestamp"] < CACHE_DURATION_SECONDS:
        return _stock_cache["data"]

    # 🛠️ Sinon, génère et met en cache
    result = lister_stock(db)
    _stock_cache["data"] = result
    _stock_cache["timestamp"] = now
    return result
