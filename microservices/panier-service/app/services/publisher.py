import redis.asyncio as redis
import json
import uuid
from datetime import datetime
import httpx

redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)

EVENT_STORE_URL = "http://event-store:8000/events"  # URL interne Docker


async def publier_commande_creee(commande: dict):
    aggregate_id = f"cmd-{commande['client_id']}-{uuid.uuid4().hex[:6]}"
    event_type = "CommandeCreee"

    event_payload = {
        "event_type": event_type,
        "data": commande,
        "timestamp": datetime.utcnow().isoformat(),
        "event_id": str(uuid.uuid4()),
    }

    # 👉 Redis Streams
    await redis_client.xadd("checkout.commandes", event_payload)

    # 👉 Event Store (POST)
    try:
        async with httpx.AsyncClient() as client:
            await client.post(
                EVENT_STORE_URL,
                json={
                    "event_type": event_type,
                    "aggregate_id": aggregate_id,
                    "data": commande,
                    "source": "panier-service",
                },
            )
    except Exception as e:
        print(f"⚠️ Erreur envoi Event Store: {e}")
