import pytest
from app.db import init_db, session
from app.models import Produit, Vente, LigneVente
from app.services.produit_service import rechercher_produit, afficher_tout_le_stock
from app.services.vente_service import enregistrer_vente, annuler_vente

produit_test_id = None

@pytest.fixture(scope="module", autouse=True)
def setup():
    global produit_test_id
    init_db()

    session.query(LigneVente).delete()
    session.query(Vente).delete()
    session.query(Produit).delete()

    produit = Produit(nom="Banane", categorie="Fruit", prix=1.5, quantite_stock=10)
    session.add(produit)
    session.commit()
    produit_test_id = produit.id
    print(f"✅ Produit inséré avec ID : {produit_test_id}")

    yield

    session.query(LigneVente).delete()
    session.query(Vente).delete()
    session.query(Produit).delete()
    session.commit()

def test_recherche_produit():
    result = rechercher_produit("banane")
    assert len(result) == 1
    assert result[0].nom.lower() == "banane"

def test_enregistrer_vente():
    global produit_test_id
    vente = enregistrer_vente([{"produit_id": produit_test_id, "quantite": 2}])
    assert vente is not None
    assert vente.total == 3.0
    assert vente.id is not None
    session.expire_all()  # pour recharger le stock
    produit = session.get(Produit, produit_test_id)
    assert produit.quantite_stock == 8  # 10 - 2

def test_afficher_tout_le_stock():
    stock = afficher_tout_le_stock()
    assert any(p.nom.lower() == "banane" for p in stock)

def test_annuler_vente():
    global produit_test_id

    # S'assurer d’un stock propre
    session.query(LigneVente).delete()
    session.query(Vente).delete()
    session.commit()

    produit = session.get(Produit, produit_test_id)
    produit.quantite_stock = 10
    session.commit()

    # Test réel
    vente = enregistrer_vente([{"produit_id": produit_test_id, "quantite": 2}])
    assert vente is not None
    vente_id = vente.id
    success = annuler_vente(vente_id)
    assert success is True

    session.expire_all()
    produit = session.get(Produit, produit_test_id)
    assert produit.quantite_stock == 10  # Maintenant oui ✅

