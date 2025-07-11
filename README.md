# LOG430 – Laboratoire 1, 2 & 3 : Système de caisse (3-tier + API REST + dashboard)

## 🧩 Description du projet

Ce projet évolue d’une application **console conteneurisée (Lab 1)** vers une **application distribuée (Lab 2)**, puis une **API RESTful sécurisée (Lab 3)** avec dashboard web.

Développé dans le cadre des laboratoires du cours **LOG430 – Architecture Logicielle (Été 2025)**.

---

## ⚙️ Fonctionnalités de l'application

### Lab 1 (2-tier, console)
- 🔍 Rechercher un produit (ID, nom ou catégorie)
- 🛒 Enregistrer une vente (multi-produits)
- ➕ Ajouter un produit
- 🔁 Annuler une vente
- 📦 Consulter l’état du stock

### Lab 2 (3-tier, API + Frontend)
- 🌐 API REST (produits, ventes, réapprovisionnement)
- 🧾 Génération de rapport de ventes (UC1)
- 🧂 Visualiser le stock par magasin (UC2)
- 📊 Visualiser les performances globales (UC3)
- 🧼 Mise à jour d’un produit (UC4)
- 🧠 Logique métier bien séparée (services)

### Lab 3 (API avancée)
- ✅ Authentification minimale (token statique)
- 🔐 Endpoints sécurisés avec `x-token`
- 📜 Documentation Swagger personnalisée
- 🧪 Tests API avec fichier `.http` (ou Postman)
- 🧠 Mise en cache (`@lru_cache`) sur `/performance/global`
- 📦 Format structuré des erreurs
- 🔍 Filtrage, pagination et tri des produits (bonus)

---

## 🗂️ Structure du projet

```
/
├── app/                          # Backend Python (FastAPI)
│   ├── models/                   # Modèles ORM
│   ├── routers/                  # Routes API REST
│   ├── services/                 # Logique métier
│   ├── db.py / main.py / schemas.py / securite.py
├── tests/                        # Tests Pytest + lab3.http
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

### 2. Lancer l’architecture (FastAPI + PostgreSQL + React)

```bash
docker-compose up --build
```

- 🧠 API Swagger : http://localhost:8000/docs
- 💻 Frontend : http://localhost:3000

💡 Le token est requis pour les endpoints sensibles :  
Ajouter le header `x-token: mon-token-secret` dans Swagger ou Postman.

---

### 🔁 Développement avec hot reload

#### 🔹 Backend FastAPI
- Le service API est lancé avec `uvicorn --reload`
- Les modifications `.py` sont automatiquement détectées.

```bash
docker-compose up api
```

#### 🔹 Frontend React
- Le service frontend utilise `npm start`
- Hot reload activé avec `react-scripts`

```bash
docker-compose up frontend
```

---



### 3. Tester l’API

```bash
# En local
pytest

# Via Docker
docker-compose exec api pytest
```

Fichier `.http` dans `tests/lab3.http`

---

## ✅ CI/CD (GitHub Actions)

Déclenchée à chaque `push`.

- `black` (style Python)
- `pytest`
- Build & test Docker image

---

## 📚 Documentation API (Swagger)

- ✅ Toutes les routes ont un `summary` + `description`
- ✅ `response_model` défini
- ✅ Sécurité documentée (`x-token`)
- ✅ Champs `example=` dans les DTOs (certains)
- ✅ Swagger modifié via `custom_openapi()`

---

## ✨ Bonnes pratiques REST

- URI claires : `/api/produits`, `/api/ventes`
- Verb HTTP bien utilisés (GET, POST, PUT, DELETE)
- Codes HTTP standardisés
- Message d’erreur normalisé (format JSON)
- Séparation des couches (services / routes)
- Filtrage et pagination (bonus)
- Mise en cache (bonus)

---

## 📄 Licence

Projet académique LOG430 – Été 2025  
Développé par **Yassine Graitaa** – `Étudiant ÉTS`  
📅 Mis à jour le 2025-07-07
