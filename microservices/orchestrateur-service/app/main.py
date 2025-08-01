from fastapi import FastAPI
from app.routers.commande_orchestration import router
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="Orchestrateur de commande", version="1.0")
app.include_router(router)

Instrumentator().instrument(app).expose(app)


@app.get("/")
def ping():
    return {"message": "Orchestrateur opérationnel"}
