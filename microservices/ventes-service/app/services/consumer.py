import redis.asyncio as redis
import json
import asyncio
import uuid
from datetime import datetime
import httpx

from app.services.vente_service import enregistrer_vente

redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)

EVENT_STORE_URL = "http://event-store:8000/events"


async def consommer_paiements():
    stream_name = "paiement.evenements"
    group_name = "ventes-group"
    consumer_name = "ventes-service-1"

    try:
        await redis_client.xgroup_create(stream_name, group_name, id="0", mkstream=True)
    except redis.ResponseError as e:
        if "BUSYGROUP" not in str(e):
            raise e

    print(f"[ventes-service] En écoute sur {stream_name}...")

    while True:
        events = await redis_client.xreadgroup(
            group_name, consumer_name, streams={stream_name: ">"}, count=10, block=5000
        )
        for stream, messages in events:
            for message_id, data in messages:
                try:
                    if data["event_type"] == "PaiementAccepte":
                        commande = json.loads(data["data"])

                        # 1. Enregistrer la vente
                        await enregistrer_vente(commande)

                        # 2. Publier dans event-store
                        event_type = "VenteConfirmee"
                        aggregate_id = str(commande.get("client_id", "inconnu"))
                        async with httpx.AsyncClient() as client:
                            await client.post(
                                EVENT_STORE_URL,
                                json={
                                    "event_type": event_type,
                                    "aggregate_id": aggregate_id,
                                    "data": commande,
                                    "source": "ventes-service",
                                },
                            )

                    await redis_client.xack(stream_name, group_name, message_id)
                except Exception as e:
                    print(f"[ventes-service] Erreur : {e}")
