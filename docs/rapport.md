
# 📦 Rapport - Laboratoire 2 (LOG430 - Été 2025)

## 1. 🎯 Objectif du projet

Ce projet consiste à faire évoluer un système de caisse local (Lab 1) vers une architecture distribuée en 3 tiers. Le système permet la gestion de produits, la vente, la consultation de stock, et le réapprovisionnement via un centre logistique.

---

## 2. ⚙️ Choix technologiques

- **Langage** : Python 3.11
- **Framework API** : FastAPI ✅ [ADR-001: Choix de FastAPI](ADR/ADR-001.md)
- **Architecture** : 3-tier avec découplage clair Client/API/BD ✅ [ADR-002: Choix 3-tier](ADR/ADR-002.md)
- **Base de données** : PostgreSQL (conteneurisée)
- **ORM** : SQLAlchemy
- **Conteneurisation** : Docker + Docker Compose
- **CI/CD** : GitHub Actions

---

## 3. 📚 Cas d'utilisation
| UC  | Description                                                     | Statut         | Endpoints principaux                 |
| --- | --------------------------------------------------------------- | -------------- | ------------------------------------ |
| UC1 | Générer un rapport consolidé des ventes                         | ✅ Terminé      | `GET /ventes/rapport`                |
| UC2 | Consulter le stock central et déclencher un réapprovisionnement | ✅ Terminé      | `GET /produits`, `POST /demandes`    |
| UC3 | Visualiser les performances des magasins                        | ⚠️ À améliorer | `GET /ventes`, `GET /ventes/rapport` |
| UC4 | Mettre à jour les produits depuis la maison mère                | ✅ Terminé      | `PUT /produits/{id}`                 |
| UC6 | Approvisionner un magasin depuis le centre logistique           | ✅ Terminé      | `POST /approvisionner/{demande_id}`  |
| UC7 | Alerte automatique en cas de rupture critique                   | ❌ Bonus        | –                                    |
| UC8 | Interface web légère pour les gestionnaires                     | ❌ Bonus        | –                                    |

---

### 📄 UC2 – Consulter le stock central et déclencher un réapprovisionnement

#### 🎯 Objectif
Permettre à un employé :
- De consulter la liste des produits et leur stock (`GET /produits`)
- De créer une demande de réapprovisionnement (`POST /demandes`)
- De consulter les demandes existantes (`GET /demandes`)

#### 🔧 Implémentation technique

- **Modèle SQLAlchemy** :

```python
class DemandeApprovisionnement(Base):
    __tablename__ = "demandes_approvisionnement"
    id = Column(Integer, primary_key=True)
    produit_id = Column(Integer, ForeignKey("produits.id"))
    quantite = Column(Integer)
    magasin = Column(String)
    statut = Column(String, default="en_attente")
    produit = relationship("Produit")
```

- **Schemas Pydantic** :

```python
class DemandeApprovisionnementIn(BaseModel):
    produit_id: int
    quantite: int
    magasin: str

class DemandeApprovisionnementOut(BaseModel):
    id: int
    produit_id: int
    quantite: int
    magasin: str
    statut: str
    class Config:
        from_attributes = True
```

- **Services** :

```python
def creer_demande_approvisionnement(demande_data: dict, session: Session):
    demande = DemandeApprovisionnement(**demande_data, statut="en_attente")
    session.add(demande)
    session.commit()
    return demande

def lister_demandes_approvisionnement(session: Session):
    return session.query(DemandeApprovisionnement).all()
```

- **Routes** :

```python
@router.post("/", response_model=DemandeApprovisionnementOut)
def creer_demande(...)

@router.get("/", response_model=List[DemandeApprovisionnementOut])
def get_demandes(...)
```

✅ Testé avec Swagger UI, stocké en base PostgreSQL.

---

## 4. 🧱 Architecture et structure du code

- `models/` : modèles ORM (Produit, Vente, DemandeApprovisionnement…)
- `services/` : logique métier indépendante du framework
- `routers/` : routes FastAPI (produits, ventes, demandes)
- `schemas.py` : schémas Pydantic (entrée/sortie)
- `main.py` : point d’entrée API + menu console
- `db.py` : configuration PostgreSQL + SQLAlchemy
- `docker-compose.yml` : 2 conteneurs (app + postgres)
- `.github/workflows/ci.yml` : tests, lint, build automatique

---

## 5. 📊 Diagrammes UML à inclure

📁 `docs/UML/` :

- `cas_utilisation.drawio` ✅ UC1 à UC6
- `classes.drawio` ✅ Produit, Vente, LigneVente, DemandeApprovisionnement
- `deploiement.drawio` ✅ 3-tier + Docker
- `sequence_uc2.drawio` ✅ depuis menu ou Swagger

---

## 6. 🧪 Tests & CI

- Pytest (unitaires) dans `tests/test_app.py`
- GitHub Actions : `.github/workflows/ci.yml`
- Testé via Swagger UI : `http://localhost:8000/docs`

---

## 7. 📌 Difficultés rencontrées

- Compréhension du découpage entre services et routers
- Erreurs de build Docker (chemins, imports)
- Problèmes initiaux avec la base de données SQLite (résolu en passant à PostgreSQL)
- Découverte de FastAPI, Pydantic v2, Uvicorn, Swagger

---

## 8. ✅ État final

- UC1 à faire
- UC2, UC4 terminés
- UC3 partiellement fait
- UC6 : en cours d'implémentation (prochaine étape)
- Bonus UC7/UC8 non faits

---

