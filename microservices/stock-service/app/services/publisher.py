import redis.asyncio as redis
import json
import uuid
from datetime import datetime

redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)


async def publier_evenement_stock(event_type: str, data: dict):
    aggregate_id = data.get("commande", {}).get("client_id", "unknown")

    event = {
        "event_type": event_type,
        "data": json.dumps(data),
        "timestamp": datetime.utcnow().isoformat(),
        "event_id": str(uuid.uuid4()),
    }
    await redis_client.xadd("stock.evenements", event)

    # Event Store
    try:
        async with httpx.AsyncClient() as client:
            await client.post(
                EVENT_STORE_URL,
                json={
                    "event_type": event_type,
                    "aggregate_id": str(aggregate_id),
                    "data": data,
                    "source": "stock-service",
                },
            )
    except Exception as e:
        print(f"⚠️ Erreur Event Store: {e}")
