from fastapi import FastAPI
from app.db import init_db
from app.routers.produits import router as produits_router
from app.routers.ventes import router as ventes_router
from app.routers.demandes import router as demandes_router
from app.routers.magasins import router as magasins_router
from app.routers.stock import router as stock_router
from app.routers.performance import router as performance_router
from app.routers.rapports import router as rapports_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialisation de la base de données
@app.on_event("startup")
def startup_event():
    init_db()


# Inclusion des routes
app.include_router(produits_router)
app.include_router(ventes_router)
app.include_router(demandes_router)
app.include_router(magasins_router)
app.include_router(stock_router)
app.include_router(performance_router)
app.include_router(rapports_router)


# Endpoint de test
@app.get("/")
def ping():
    return {"message": "Backend caisse opérationnel"}
