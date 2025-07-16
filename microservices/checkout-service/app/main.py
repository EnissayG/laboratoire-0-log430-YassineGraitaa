from fastapi import FastAPI
from app.db.database import Base, engine
from app.routers import checkout

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Service de Check-out")
app.include_router(checkout.router)
