from fastapi import FastAPI
from app.routers.commande_orchestration import router
from prometheus_fastapi_instrumentator import Instrumentator
from app.db.database import Base, engine
from app.models import etat_saga  # Assure-toi d’importer le modèle

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Orchestrateur de commande", version="1.0")
app.include_router(router)

Instrumentator().instrument(app).expose(app)


@app.get("/")
def ping():
    return {"message": "Orchestrateur opérationnel"}


# app/main.py
from fastapi import FastAPI
from app.routers.commande_orchestration import router
from prometheus_client import make_asgi_app

app = FastAPI(title="Orchestrateur Saga")

app.include_router(router)

# Expose /metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)
