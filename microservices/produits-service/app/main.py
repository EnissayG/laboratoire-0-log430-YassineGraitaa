from fastapi import FastAPI
from app.routers import produits
from prometheus_fastapi_instrumentator import Instrumentator

# 💥 Ceci va créer les tables automatiquement au démarrage
from app.db.database import Base, engine
from app.models import produit  # assure-toi que ce fichier existe

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Produits Service", version="1.0")
app.include_router(produits.router)
Instrumentator().instrument(app).expose(app)
