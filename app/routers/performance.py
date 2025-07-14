from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_session
from app.services.performance_service import calculer_performance_globale
from app.schemas import PerformanceGlobaleDTO
import time

router = APIRouter(prefix="/api/performance", tags=["Performance"])

# 🧠 Simple cache
_perf_cache = {"data": None, "timestamp": 0}
CACHE_DURATION = 60  # 1 minute


@router.get(
    "/global",
    response_model=PerformanceGlobaleDTO,
    summary="Afficher les performances agrégées du système",
    description="Retourne les performances globales du système de vente.",
)
def get_performance_globale(db: Session = Depends(get_session)):
    now = time.time()
    if now - _perf_cache["timestamp"] < CACHE_DURATION:
        return _perf_cache["data"]

    result = calculer_performance_globale(db)
    _perf_cache["data"] = result
    _perf_cache["timestamp"] = now
    return result
