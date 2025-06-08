# app/main.py
from fastapi import FastAPI
from app.db import init_db
from app.routers import produits, ventes, demandes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # autorise React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    init_db()


# Inclusion des routes
app.include_router(produits.router)
app.include_router(ventes.router)
app.include_router(demandes.router)


@app.get("/")
def ping():
    return {"message": "Backend caisse opérationnel"}
