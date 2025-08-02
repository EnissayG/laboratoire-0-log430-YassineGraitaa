from fastapi import FastAPI
from app.routers import ventes
from app.db.database import Base, engine
from app.models import vente, lignevente, produit, magasin
from prometheus_fastapi_instrumentator import Instrumentator
import asyncio
from app.services.consumer import consommer_paiements

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Ventes Service", version="1.0")
app.include_router(ventes.router)

Instrumentator().instrument(app).expose(app)


@app.on_event("startup")
async def demarrer_consumer():
    asyncio.create_task(consommer_paiements())
