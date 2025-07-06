from fastapi.testclient import TestClient
from app.main import app
from app.db import Base, engine, get_session
from sqlalchemy.orm import sessionmaker
import uuid
# Créer une session de test
TestSession = sessionmaker(bind=engine)
client = TestClient(app)

# Utilitaires de test


import uuid

def creer_magasin_et_produit():
    session = TestSession()

    from app.models.magasin import Magasin
    from app.models.produit import Produit

    nom_unique = f"TestMag_{uuid.uuid4().hex[:8]}"

    magasin = Magasin(nom=nom_unique, adresse="123", ville="MTL")
    session.add(magasin)
    session.commit()
    session.refresh(magasin)
    magasin_id = magasin.id  # ✅ on récupère l’ID AVANT de fermer la session

    produit = Produit(
        nom="TestProduit",
        categorie="TestCat",
        prix=10.0,
        quantite_stock=5,
        magasin_id=magasin_id
    )
    session.add(produit)
    session.commit()
    session.refresh(produit)
    produit_id = produit.id  # ✅ pareil ici

    session.close()
    return magasin_id, produit_id


# =============================
# 🔹 UC4 – Créer une demande
# =============================
def test_creer_demande():
    magasin_id, produit_id = creer_magasin_et_produit()

    payload = {
        "produit_id": produit_id,
        "quantite": 10,
        "magasin_id": magasin_id
    }

    response = client.post("/api/demandes/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["produit_id"] == produit_id
    assert data["quantite"] == 10
    assert data["magasin_id"] == magasin_id
    assert data["statut"] == "en_attente"

# =============================
# 🔹 UC5 – Traiter une demande
# =============================
def test_traiter_demande():
    magasin_id, produit_id = creer_magasin_et_produit()

    # Créer une demande d’approvisionnement
    payload = {
        "produit_id": produit_id,
        "quantite": 5,
        "magasin_id": magasin_id
    }

    resp = client.post("/api/demandes/", json=payload)
    assert resp.status_code == 200
    demande_id = resp.json()["id"]

    # Traiter la demande
    traiter = client.post(f"/api/demandes/traiter/{demande_id}")
    assert traiter.status_code == 200
    assert traiter.json()["message"] == "Demande traitée avec succès"

    # Vérifier que la quantité du produit a été augmentée
    produits = client.get("/api/produits/").json()
    produit = next((p for p in produits if p["id"] == produit_id), None)
    assert produit["quantite_stock"] == 10  # 5 initiaux + 5 demandés
