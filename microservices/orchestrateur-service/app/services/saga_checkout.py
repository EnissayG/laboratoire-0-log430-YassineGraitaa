import uuid
import httpx
from sqlalchemy.orm import Session
from app.db.database import get_session
from app.schemas import CommandeInput
from app.models.etat_commande_enum import EtatCommande
from app.services.etat_commande import changer_etat_commande


async def executer_saga(commande: CommandeInput) -> dict:
    saga_id = uuid.uuid4()

    with next(get_session()) as db:
        changer_etat_commande(
            db, saga_id, EtatCommande.INITIEE, commande.client_id, commande.magasin_id
        )

    try:
        async with httpx.AsyncClient() as client:
            panier = await client.get(
                f"http://panier-service:8000/api/paniers/client/{commande.client_id}"
            )
            if panier.status_code != 200:
                with next(get_session()) as db:
                    changer_etat_commande(db, saga_id, EtatCommande.ECHEC_STOCK)
                return {
                    "saga_id": str(saga_id),
                    "etat_final": EtatCommande.ECHEC_STOCK.value,
                }

            produits = panier.json()

            # Réservation
            res = await client.post(
                "http://stock-service:8000/api/stock/reserver",
                json={"produits": produits},
            )
            if res.status_code != 200:
                with next(get_session()) as db:
                    changer_etat_commande(db, saga_id, EtatCommande.ECHEC_STOCK)
                return {
                    "saga_id": str(saga_id),
                    "etat_final": EtatCommande.ECHEC_STOCK.value,
                }

            with next(get_session()) as db:
                changer_etat_commande(db, saga_id, EtatCommande.STOCK_RESERVE)

            # Paiement
            total = sum(p["quantite"] * p["prix"] for p in produits)
            pay = await client.post(
                f"http://client-service:8000/api/clients/{commande.client_id}/payer",
                json={"montant": total},
            )
            if pay.status_code != 200:
                await client.post(
                    "http://stock-service:8000/api/stock/liberer",
                    json={"produits": produits},
                )
                with next(get_session()) as db:
                    changer_etat_commande(db, saga_id, EtatCommande.ECHEC_PAIEMENT)
                return {
                    "saga_id": str(saga_id),
                    "etat_final": EtatCommande.ECHEC_PAIEMENT.value,
                }

            with next(get_session()) as db:
                changer_etat_commande(db, saga_id, EtatCommande.PAIEMENT_EFFECTUE)

            # Vente
            vente = await client.post(
                "http://ventes-service:8000/api/ventes",
                json={
                    "produits": produits,
                    "client_id": commande.client_id,
                    "magasin_id": commande.magasin_id,
                },
            )
            if vente.status_code != 201:
                await client.post(
                    f"http://client-service:8000/api/clients/{commande.client_id}/rembourser",
                    json={"montant": total},
                )
                await client.post(
                    "http://stock-service:8000/api/stock/liberer",
                    json={"produits": produits},
                )
                with next(get_session()) as db:
                    changer_etat_commande(
                        db, saga_id, EtatCommande.ECHEC_ENREGISTREMENT
                    )
                return {
                    "saga_id": str(saga_id),
                    "etat_final": EtatCommande.ECHEC_ENREGISTREMENT.value,
                }

            with next(get_session()) as db:
                changer_etat_commande(db, saga_id, EtatCommande.CONFIRMEE)

            return {"saga_id": str(saga_id), "etat_final": EtatCommande.CONFIRMEE.value}

    except Exception as e:
        with next(get_session()) as db:
            changer_etat_commande(db, saga_id, EtatCommande.ANNULEE)
        return {
            "saga_id": str(saga_id),
            "etat_final": EtatCommande.ANNULEE.value,
            "erreur": str(e),
        }
