import redis.asyncio as redis
import json
import uuid
from datetime import datetime

redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)


async def publier_commande_creee(commande: dict):
    event = {
        "event_type": "CommandeCreee",
        "data": json.dumps(commande),
        "timestamp": datetime.utcnow().isoformat(),
        "event_id": str(uuid.uuid4()),
    }
    await redis_client.xadd("checkout.commandes", event)
