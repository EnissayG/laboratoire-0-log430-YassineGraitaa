from fastapi import FastAPI
from app.routers import stock
from prometheus_fastapi_instrumentator import Instrumentator
import asyncio
from app.services.consumer import consommer_commandes, consommer_paiement_refuse

# 👇 Ajout pour créer automatiquement les tables
from app.db.database import Base, engine
from app.models import produit, magasin  # 🔁 importer les modèles

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Stock Service", version="1.0")
app.include_router(stock.router)
Instrumentator().instrument(app).expose(app)


@app.on_event("startup")
async def demarrer_consumers():
    asyncio.create_task(consommer_commandes())
    asyncio.create_task(consommer_paiement_refuse())
