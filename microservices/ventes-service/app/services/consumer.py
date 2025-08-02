import redis.asyncio as redis
import json
import asyncio
from app.services.vente_service import enregistrer_vente

redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)


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
                        await enregistrer_vente(commande)
                    await redis_client.xack(stream_name, group_name, message_id)
                except Exception as e:
                    print(f"[ventes-service] Erreur : {e}")
