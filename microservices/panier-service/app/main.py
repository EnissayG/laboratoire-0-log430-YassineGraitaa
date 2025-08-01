from fastapi import FastAPI
from app.db.database import Base, engine
from app.routers import paniers
from prometheus_fastapi_instrumentator import Instrumentator

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Panier Service")

app.include_router(paniers.router)
Instrumentator().instrument(app).expose(app)
