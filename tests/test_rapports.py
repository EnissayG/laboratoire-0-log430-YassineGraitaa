# tests/test_rapports.py

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_rapport_ventes_endpoint():
    response = client.get(
        "/api/rapports/ventes",
        params={"date_debut": "2024-01-01", "date_fin": "2025-12-31"},
    )

    assert response.status_code == 200

    data = response.json()
    assert "rapport" in data
    assert isinstance(data["rapport"], list)

    # Si tu veux tester un format d'élément
    if data["rapport"]:
        premier = data["rapport"][0]
        assert "magasin" in premier
        assert "nombre_ventes" in premier
        assert "total_ventes" in premier
