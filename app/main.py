from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from app.db import init_db
from app.routers.produits import router as produits_router
from app.routers.ventes import router as ventes_router
from app.routers.demandes import router as demandes_router
from app.routers.magasins import router as magasins_router
from app.routers.stock import router as stock_router
from app.routers.performance import router as performance_router
from app.routers.rapports import router as rapports_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi import HTTPException
from datetime import datetime

app = FastAPI()
from app.logger import logger


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Système de caisse",
        version="1.0.0",
        description="API LOG430 avec token statique de sécurité",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "APIKeyHeader": {"type": "apiKey", "in": "header", "name": "x-token"}
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"APIKeyHeader": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    log_entry = f"{request.method} {request.url} -> {exc.status_code} {exc.detail}"
    logger.warning(log_entry)

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "timestamp": datetime.utcnow().isoformat(),
            "status": exc.status_code,
            "error": exc.detail,
            "path": request.url.path,
        },
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


Instrumentator().instrument(app).expose(app)
