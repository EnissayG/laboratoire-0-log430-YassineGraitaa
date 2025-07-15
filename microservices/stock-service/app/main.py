from fastapi import FastAPI
from app.routers import stock

# 👇 Ajout pour créer automatiquement les tables
from app.db.database import Base, engine
from app.models import produit, magasin  # 🔁 importer les modèles

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Stock Service", version="1.0")
app.include_router(stock.router)
