from fastapi import FastAPI
from app.routers import ventes
from app.db.database import Base, engine
from app.models import vente, lignevente, produit, magasin

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Ventes Service", version="1.0")
app.include_router(ventes.router)
