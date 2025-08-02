from fastapi import FastAPI
from app.db.database import create_tables
from app.routers import events

app = FastAPI(title="Event Store")

app.include_router(events.router)


@app.on_event("startup")
def startup():
    create_tables()
