import redis.asyncio as redis
import json
import asyncio
from app.services.stock_service import (
    reserver_produits,
)  # fonction à implémenter ou stub

redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)


async def consommer_commandes():
    stream_name = "checkout.commandes"
    group_name = "stock-group"
    consumer_name = "stock-service-1"

    try:
        await redis_client.xgroup_create(stream_name, group_name, id="0", mkstream=True)
    except redis.ResponseError as e:
        if "BUSYGROUP" not in str(e):
            raise e

    print(f"[stock-service] En écoute sur {stream_name}...")

    while True:
        events = await redis_client.xreadgroup(
            group_name, consumer_name, streams={stream_name: ">"}, count=10, block=5000
        )
        for stream, messages in events:
            for message_id, data in messages:
                try:
                    event_data = json.loads(data["data"])
                    await reserver_produits(event_data)
                    await redis_client.xack(stream_name, group_name, message_id)
                except Exception as e:
                    print(f"[Erreur traitement] {e}")
