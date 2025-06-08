# LOG430 – Laboratoire 1 & 2 : Système de caisse (3-tier + dashboard)

## 🧩 Description du projet

Ce projet évolue d’une application **console conteneurisée (Lab 1)** vers une **application distribuée (Lab 2)** avec API REST (FastAPI) et dashboard web (React).

Il est développé dans le cadre des laboratoires du cours **LOG430 – Architecture Logicielle (Été 2025)**.

---

## ⚙️ Fonctionnalités de l'application

### Lab 1 (2-tier, console)
- 🔍 Rechercher un produit (ID, nom ou catégorie)
- 🛒 Enregistrer une vente (multi-produits)
- ➕ Ajouter un produit
- 🔁 Annuler une vente
- 📦 Consulter l’état du stock

### Lab 2 (3-tier, web API + React)
- 🌐 API REST avec FastAPI (produits, ventes, réapprovisionnement)
- 🗂️ Gestion des demandes de stock
- 📊 Dashboard visuel avec React : ventes, ruptures, surstock
- 🧾 Génération de rapport de ventes (UC1)
- ✅ Couverture UC1 à UC6, UC8 (option B)

---

## 🗂️ Structure du projet

```
/
├── app/                          # Backend Python (FastAPI)
│   ├── models/                   # Modèles ORM
│   ├── routers/                  # Routes API REST
│   ├── services/                 # Logique métier
│   ├── db.py / main.py / schemas.py
├── tests/                        # Tests Pytest
├── frontend/dashboard/          # Interface React (UC3/UC8)
├── docker-compose.yml / Dockerfile
├── requirements.txt             # Dépendances backend
├── .github/workflows/ci.yml     # Pipeline CI/CD
└── README.md
```

---

## 🚀 Instructions d’exécution

### 1. Cloner le dépôt

```bash
git clone https://github.com/EnissayG/laboratoire-0-log430-YassineGraitaa.git
cd laboratoire-0-log430-YassineGraitaa/
```

---

### 2. Lancer toute l’architecture (FastAPI + PostgreSQL + dashboard React)

```bash
docker-compose up --build
```

- 🔹 Accès API : http://localhost:8000/docs
- 🔹 Accès dashboard : http://localhost:3000

---

### 3. Exécuter les tests

```bash
# En local
python -m pytest

# Ou via Docker Compose
docker-compose run --rm app pytest
```

---

### 4. Formater le code Python avec Black

```bash
python -m black .
```

> Le style est automatiquement vérifié dans la CI avec `black --check .`

---

## 🔁 CI/CD (GitHub Actions)

Déclenchée à chaque `push` sur `main`.

Étapes automatisées :
1. ✅ **Lint** avec `black`
2. ✅ **Tests** via `pytest`
3. ✅ **Build Docker** image backend
4. ✅ **Push Docker Hub** : `docker.io/<votre_nom>/log430-app`

---

## 🧼 Bonnes pratiques appliquées

- Architecture 3-tier : base de données, API, frontend React
- Découplage total (routes, services, modèles)
- ORM SQLAlchemy + Pydantic (v2)
- Dashboard React avec Recharts pour UC3 + UC8
- Tests unitaires + CI avec GitHub Actions
- Lint automatique avec `black`
- Déploiement conteneurisé (Docker Compose)

---

## 📄 Licence

Projet académique – cours LOG430 (Architecture Logicielle) à l’ÉTS – Été 2025.  
Développé par **Yassine Graitaa**.
