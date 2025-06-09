
# 📦 Rapport - Laboratoire 2 (LOG430 - Été 2025)

## 1. 🎯 Objectif du projet

Ce projet fait évoluer un système de caisse local (Lab 1) vers une architecture distribuée en 3 tiers. Le système permet de gérer les produits, ventes, réapprovisionnements et indicateurs de performance via une interface visuelle et une API REST.

---

## 2. ⚙️ Choix 

- **Langage** : Python 3.11
- **Backend** : FastAPI ✅ [ADR-001: Choix de FastAPI](docs\LAB2\ADR\ADR-001-fastapi.md)
- **Frontend** : React (dashboard interactif)
- **Architecture** : 3-tier (Client / API / BD) ✅ [ADR-002: Choix 3-tier](docs\LAB2\ADR\ADR-002-architecture-3-tier.md)
- **Base de données** : PostgreSQL (conteneurisée)
- **ORM** : SQLAlchemy
- **Conteneurisation** : Docker + Docker Compose
- **CI/CD** : GitHub Actions

---

## 3. 📚 Cas d'utilisation

| UC  | Description                                                     | Statut         | Endpoints principaux                 |
| --- | --------------------------------------------------------------- | -------------- | ------------------------------------ |
| UC1 | Générer un rapport consolidé des ventes                         | ✅ Terminé     | `GET /ventes/rapport`                |
| UC2 | Consulter le stock et réapprovisionner                          | ✅ Terminé     | `GET /produits`, `POST /demandes`    |
| UC3 | Visualiser les performances des magasins (dashboard)            | ✅ Terminé     | `GET /ventes/rapport` (frontend)     |
| UC4 | Mise à jour des produits depuis la maison mère                  | ✅ Terminé     | `PUT /produits/{id}`                 |
| UC6 | Approvisionnement depuis le centre logistique                   | ✅ Terminé     | `POST /approvisionner/{demande_id}`  |
| UC7 | Alerte automatique en cas de rupture critique                   | ❌ Bonus       | –                                    |
| UC8 | Interface web légère pour les gestionnaires                     | ✅ Partiel     | – (React)                            |

---

## 4. 🧱 Structure de l'architecture

- Architecture logique modulaire, basée sur les principes de séparation des responsabilités :
  - `models/` : entités SQLAlchemy (Produit, Vente, LigneVente, DemandeApprovisionnement)
  - `services/` : logique métier (stock, vente, rapports)
  - `routers/` : endpoints FastAPI
  - `schemas.py` : validation Pydantic
  - `main.py` : point d'entrée backend
  - `front/` : client React (dashboard)
  - `db.py` : configuration de la connexion à PostgreSQL

---

## 5. 🖼️ Diagrammes UML (modèle 4+1)

📁 `docs/UML/` contient les éléments suivants :
- ✅ `cas_utilisation.puml` : UC1 à UC6 (PlantUML)
- ✅ `diagramme_classes.puml` : modèle de domaine (Produit, Vente, etc.)
- ✅ `deploiement_tier3.puml` : Vue physique des conteneurs
- ✅ `developpement.puml` : Vue de développement (organisation technique)
- ✅ `sequence_rapport.puml`, `sequence_demande.puml` : Séquences API + BD

---

## 6. ⚙️ CI/CD (Automatisation)

- Pipeline CI dans `.github/workflows/ci.yml`
- Étapes :
  - ✅ Linting avec Black : `black --check .`
  - ✅ Exécution des tests unitaires : `pytest`
  - ✅ Build image Docker : `docker build .`
  - ✅ Push Docker Hub (si configuré)

---

## 7. 🧪 Tests unitaires

- Framework : `pytest`
- Exécution locale : `docker-compose run --rm api pytest`
- Cas testés :
  - ✅ Création, annulation de vente
  - ✅ Recherche de produits
  - ✅ Traitement de demande de réapprovisionnement
  - ✅ Vérification du stock après vente / annulation

---

## 8. 💻 Interface visuelle (UC3)

- Frontend React (`front/`)
- Affichage dynamique des données (via API FastAPI) :
  - Total des ventes
  - Produits les plus vendus (bar chart)
  - Produits en rupture de stock
  - Produits en surstock
  - Répartition des ventes par magasin (pie chart)

  ![alt text](image.png)

---

## 9. 📄 Décisions architecturales (ADR)

- [ADR-001](docs/ADR/ADR-001.md) : Choix de FastAPI pour sa rapidité, typage, Swagger intégré
- [ADR-002](docs/ADR/ADR-002.md) : Adoption d’une architecture 3-tier pour une séparation claire entre UI, logique métier et persistance

---

## 10. 🧭 Difficultés rencontrées

- Problèmes d'import à cause du rechargement Docker / Uvicorn
- Intégration React avec FastAPI (CORS, fetch)
- Résolution des dépendances entre modules FastAPI + SQLAlchemy
- Montée en complexité dans les tests avec `TestClient` et la BDD isolée

---

## 11. 🚀 Instructions d'exécution

### Lancer tous les services (API + BD + Frontend)
```bash
docker-compose up --build
```

### Tester l'API (via Swagger)
[http://localhost:8000/docs](http://localhost:8000/docs)

### Accéder au tableau de bord React
[http://localhost:3000](http://localhost:3000)

### Exécuter les tests
```bash
docker-compose run --rm api pytest
```

### Formatter le code
```bash
python -m black .
```

---

## 12. 📦 Livrables

- ✅ `lab0/`, `lab1/`, `lab2/` : Code source complet avec tags Git (`v0.1`, `v1.0`, `v2.0`)
- ✅ `rapport_final_log430_lab2.md` (ce fichier)
- ✅ 2 ADR (dans `docs/ADR/`)
- ✅ Diagrammes UML (dans `docs/UML/`)
- ✅ `.zip` contenant l’ensemble du dépôt pour remise finale
