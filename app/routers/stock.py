from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_session
from app.services.stock_service import lister_stock
from app.schemas import ProduitStockDTO
from typing import List

router = APIRouter(prefix="/api/stock", tags=["Stock"])


@router.get(
    "/",
    response_model=List[ProduitStockDTO],
    summary="Lister le stock global",
    description="Retourne tous les produits avec leurs quantités en stock dans chaque magasin.",
)
def get_stock(db: Session = Depends(get_session)):
    return lister_stock(db)
