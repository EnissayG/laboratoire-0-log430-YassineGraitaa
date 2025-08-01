import httpx
from app.models.commande_saga import CommandeInput, EtatCommande


async def executer_saga(commande: CommandeInput) -> EtatCommande:
    etat = EtatCommande.INITIEE
    try:
        async with httpx.AsyncClient() as client:

            # 1️⃣ Récupérer le panier du client
            panier_resp = await client.get(
                f"http://panier-service:8000/api/paniers/client/{commande.client_id}"
            )
            if panier_resp.status_code != 200:
                return EtatCommande.ECHEC_STOCK
            produits = panier_resp.json()
            if not produits:
                return EtatCommande.ECHEC_STOCK

            # 2️⃣ Réserver les produits
            res = await client.post(
                "http://stock-service:8000/api/stock/reserver",
                json={"produits": produits},
            )
            if res.status_code != 200:
                return EtatCommande.ECHEC_STOCK
            etat = EtatCommande.STOCK_RESERVE

            # 3️⃣ Débiter le client
            total = sum(p["quantite"] * p["prix"] for p in produits)
            paiement = await client.post(
                f"http://client-service:8000/api/clients/{commande.client_id}/payer",
                json={"montant": total},
            )
            if paiement.status_code != 200:
                # rollback stock
                await client.post(
                    "http://stock-service:8000/api/stock/liberer",
                    json={"produits": produits},
                )
                return EtatCommande.ECHEC_PAIEMENT
            etat = EtatCommande.PAIEMENT_EFFECTUE

            # 4️⃣ Enregistrer la commande (vente)
            vente = await client.post(
                "http://ventes-service:8000/api/ventes",
                json={
                    "produits": produits,
                    "client_id": commande.client_id,
                    "magasin_id": commande.magasin_id,
                },
            )
            if vente.status_code != 201:
                # rollback paiement + stock
                await client.post(
                    f"http://client-service:8000/api/clients/{commande.client_id}/rembourser",
                    json={"montant": total},
                )
                await client.post(
                    "http://stock-service:8000/api/stock/liberer",
                    json={"produits": produits},
                )
                return EtatCommande.ECHEC_ENREGISTREMENT

            etat = EtatCommande.CONFIRMEE
            return etat

    except Exception as e:
        print(f"❌ Erreur critique orchestrateur : {e}")
        return EtatCommande.ANNULEE
