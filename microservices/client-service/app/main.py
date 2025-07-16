from fastapi import FastAPI
from app.routers.clients import router
from app.db.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Client Service")
app.include_router(router)
