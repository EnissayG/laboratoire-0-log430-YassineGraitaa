from fastapi import FastAPI
from app.routers.clients import router
from app.db.database import Base, engine
from prometheus_fastapi_instrumentator import Instrumentator
import asyncio
from app.services.consumer import consommer_stock_reserve


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Client Service")
app.include_router(router)
Instrumentator().instrument(app).expose(app)


@app.on_event("startup")
async def demarrer_consumer():
    asyncio.create_task(consommer_stock_reserve())
