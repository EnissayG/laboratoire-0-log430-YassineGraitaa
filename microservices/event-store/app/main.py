from fastapi import FastAPI
from app.db.database import create_tables
from app.routers import events
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="Event Store")
Instrumentator().instrument(app).expose(app)
app.include_router(events.router)


@app.on_event("startup")
def startup():
    create_tables()
