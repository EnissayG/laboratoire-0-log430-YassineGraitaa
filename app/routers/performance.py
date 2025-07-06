from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_session
from app.services.performance_service import calculer_performance_globale
from app.schemas import PerformanceGlobaleDTO

router = APIRouter(prefix="/api/performance", tags=["Performance"])


@router.get(
    "/global",
    response_model=PerformanceGlobaleDTO,
    summary="Afficher les performances agrégées du système",
    description="Retourne les performances globales du système de vente.",
)
def get_performance_globale(db: Session = Depends(get_session)):
    return calculer_performance_globale(db)
