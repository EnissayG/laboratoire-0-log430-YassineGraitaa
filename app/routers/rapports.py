from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from app.db import get_session
from app.services.rapports_service import generer_rapport_ventes
from app.schemas import RapportVenteDTO, RapportVenteResponse
import time

router = APIRouter(prefix="/api/rapports", tags=["Rapports"])

# 🧠 Cache mémoire avec clés dynamiques (par dates)
_rapport_cache = {}  # clé = (date_debut, date_fin), valeur = (timestamp, data)
CACHE_DURATION = 60  # 60 secondes


@router.get(
    "/ventes",
    response_model=RapportVenteResponse,
    summary="Rapport consolidé des ventes",
    description="Génère un rapport consolidé des ventes entre deux dates spécifiques.",
)
def rapport_ventes(
    date_debut: date = Query(..., description="Date de début (YYYY-MM-DD)"),
    date_fin: date = Query(..., description="Date de fin (YYYY-MM-DD)"),
    db: Session = Depends(get_session),
):
    import time

    if date_debut > date_fin:
        raise HTTPException(
            status_code=400, detail="La date de début doit précéder la date de fin."
        )

    key = (str(date_debut), str(date_fin))
    now = time.time()

    if key in _rapport_cache:
        ts, data = _rapport_cache[key]
        if now - ts < CACHE_DURATION:
            return data

    donnees = generer_rapport_ventes(db, date_debut, date_fin)

    rapport = [
        RapportVenteDTO(
            magasin=r.magasin,
            nombre_ventes=r.nombre_ventes,
            total_ventes=r.total_ventes,
        )
        for r in donnees
    ]

    _rapport_cache[key] = (now, {"rapport": rapport})
    return {"rapport": rapport}
