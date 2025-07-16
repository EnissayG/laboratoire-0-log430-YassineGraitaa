from fastapi import FastAPI
from app.db.database import Base, engine
from app.routers import paniers

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Panier Service")

app.include_router(paniers.router)
