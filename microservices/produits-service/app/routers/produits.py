from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
import time

from app.db.database import get_session
from app.schemas import ProduitUpdate
from app.services.produit_service import (
    rechercher_produits_avances,
    afficher_tout_le_stock,
    rechercher_produit,
    ajouter_produit,
    modifier_produit,
)

router = APIRouter(prefix="/api/produits", tags=["Produits"])
# Caches
_produits_all_cache = {"data": None, "timestamp": 0}
_produits_filtre_cache = {}
_recherche_cache = {}
CACHE_DURATION = 60


@router.get(
    "/filtrer",
    summary="Filtrer, trier et paginer les produits",
    description="Permet de filtrer les produits par catégorie, trier et paginer les résultats.",
)
def filtrer_produits(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    sort: str = Query("nom,asc"),
    categorie: Optional[str] = None,
    session: Session = Depends(get_session),
):
    now = time.time()
    key = f"{page}-{size}-{sort}-{categorie}"
    cache = _produits_filtre_cache.get(key)

    if cache and now - cache["timestamp"] < CACHE_DURATION:
        return cache["data"]

    data = rechercher_produits_avances(page, size, sort, categorie, session)
    _produits_filtre_cache[key] = {"data": data, "timestamp": now}
    return data


@router.get(
    "/",
    summary="Lister tous les produits",
    description="Retourne tous les produits enregistrés dans tous les magasins.",
)
def get_all(session: Session = Depends(get_session)):
    now = time.time()
    if now - _produits_all_cache["timestamp"] < CACHE_DURATION:
        return _produits_all_cache["data"]

    data = afficher_tout_le_stock(session)
    _produits_all_cache["data"] = data
    _produits_all_cache["timestamp"] = now
    return data


@router.get(
    "/recherche",
    summary="Rechercher un produit",
    description="Recherche un produit par nom, catégorie ou ID numérique.",
)
def rechercher(critere: str, session: Session = Depends(get_session)):
    now = time.time()
    cache = _recherche_cache.get(critere)

    if cache and now - cache["timestamp"] < CACHE_DURATION:
        return cache["data"]

    data = rechercher_produit(critere, session)
    _recherche_cache[critere] = {"data": data, "timestamp": now}
    return data


@router.post(
    "/",
    summary="Ajouter un nouveau produit",
    description="Ajoute un nouveau produit dans un magasin donné. Le magasin est identifié par `magasin_id`.",
)
def ajouter(
    nom: str,
    categorie: str,
    prix: float,
    quantite_stock: int,
    magasin_id: int,
    session: Session = Depends(get_session),
):
    return ajouter_produit(nom, categorie, prix, quantite_stock, magasin_id, session)


@router.put(
    "/{produit_id}",
    summary="Mettre à jour un produit",
    description="Modifie un ou plusieurs champs (nom, prix, quantité...) d’un produit existant.",
)
def update_produit(
    produit_id: int, update_data: ProduitUpdate, session: Session = Depends(get_session)
):
    updated = modifier_produit(
        produit_id, update_data.dict(exclude_unset=True), session
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    return updated
