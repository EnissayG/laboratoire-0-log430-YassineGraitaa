from fastapi import FastAPI
from app.routers import magasins
from app.db.database import Base, engine
from app.models import magasin, produit
from prometheus_fastapi_instrumentator import Instrumentator

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Magasin Service", version="1.0")
app.include_router(magasins.router)
Instrumentator().instrument(app).expose(app)
