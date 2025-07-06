# tests/test_magasin.py

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_creer_magasin():
    response = client.post(
        "/api/magasins/",
        json={"nom": "TestMagasin", "adresse": "123 rue Test", "ville": "Testville"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["nom"] == "TestMagasin"
    assert data["ville"] == "Testville"
    global MAGASIN_ID
    MAGASIN_ID = data["id"]  # garde pour les autres tests


def test_lister_magasins():
    response = client.get("/api/magasins/")
    assert response.status_code == 200
    magasins = response.json()
    assert any(m["nom"] == "TestMagasin" for m in magasins)


def test_modifier_magasin():
    response = client.put(
        f"/api/magasins/{MAGASIN_ID}",
        json={"nom": "MagasinModifie", "ville": "VilleModifiee"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["nom"] == "MagasinModifie"
    assert data["ville"] == "VilleModifiee"


def test_supprimer_magasin():
    response = client.delete(f"/api/magasins/{MAGASIN_ID}")
    assert response.status_code == 200
    # Vérifie que le magasin a bien été supprimé
    response = client.get("/api/magasins/")
    magasins = response.json()
    assert all(m["id"] != MAGASIN_ID for m in magasins)
