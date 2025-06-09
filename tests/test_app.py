from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_produits():
    response = client.get("/produits/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_recherche_produit():
    response = client.get("/produits/recherche", params={"critere": "Test"})
    assert response.status_code == 200


def test_ajout_produit():
    response = client.post(
        "/produits/",
        params={
            "nom": "TestProduit",
            "categorie": "TestCat",
            "prix": 9.99,
            "quantite_stock": 20,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["nom"] == "TestProduit"


def test_vente_invalide():
    # Vente sans panier ni magasin → erreur 422
    response = client.post("/ventes/", json={})
    assert response.status_code == 422


def test_rapport_global():
    response = client.get("/ventes/rapport")
    assert response.status_code == 200
    data = response.json()
    assert "total_ventes" in data
    assert "ruptures" in data
    assert "surstocks" in data


def test_creer_demande_approvisionnement():
    # 🔸 À ajuster selon un produit réel
    response = client.post(
        "/demandes/", json={"produit_id": 1, "quantite": 5, "magasin": "TestMagasin"}
    )
    # Soit il passe (produit existe), soit 404
    assert response.status_code in (200, 404)
