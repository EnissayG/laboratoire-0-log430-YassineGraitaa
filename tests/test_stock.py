# tests/test_stock.py

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_stock_endpoint():
    response = client.get("/api/stock/")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)

    if data:  # on vérifie un exemple seulement s'il y a au moins un produit
        produit = data[0]
        assert "id" in produit
        assert "nom" in produit
        assert "categorie" in produit
        assert "quantite_stock" in produit
        assert "prix" in produit
