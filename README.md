# LOG430 – Laboratoire 1 : Système de caisse console (2-tier)

## 🧩 Description du projet

Ce projet est une application **console Python conteneurisée**, développée dans le cadre du Laboratoire 1 du cours **LOG430 – Architecture Logicielle (Été 2025)**.  
Elle met en œuvre une architecture 2-tiers pour un système de caisse local, avec une base de données PostgreSQL et une application cliente en console.

---

## ⚙️ Fonctionnalités de l'application

- 🔍 Rechercher un produit (ID, nom ou catégorie)
- 🛒 Enregistrer une vente (multi-produits)
- ➕ Ajouter un produit
- 🔁 Annuler une vente
- 📦 Consulter l’état du stock
- 🧪 Tests automatisés avec `pytest`
- 🐳 Docker + `docker-compose`
- 🔁 Pipeline CI/CD (GitHub Actions + Docker Hub)

---

## 🗂️ Structure du projet

```
/
├── app/                          # Application principale
│   ├── models/                   # Modèles ORM (Produit, Vente, LigneVente)
│   ├── services/                 # Logique métier (vente, produit)
│   ├── db.py                     # Connexion PostgreSQL
│   └── main.py                   # Menu console
├── app.py                        # Point d’entrée global
├── tests/test_app.py             # Tests unitaires
├── Dockerfile                    # Image Docker
├── docker-compose.yml            # App + PostgreSQL
├── requirements.txt              # Dépendances
├── .github/workflows/ci.yml      # Pipeline GitHub Actions
├── .dockerignore / .gitignore    # Fichiers exclus
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

### 2. Lancer l'application (en mode interactif avec Docker Compose)

⚠️ Pour exécuter l’application console avec `input()`, il faut un terminal interactif :

```bash
docker-compose run --rm app
```

📌 Cela démarre :
- Le conteneur PostgreSQL
- Le conteneur de l'application console
- Et te permet d'interagir avec le menu

---

### 3. Ou lancer le tout (sans interaction)

```bash
docker-compose up --build
```

🔸 Utile pour vérifier que le conteneur démarre bien, mais `input()` plantera sans terminal interactif.

---

### 4. Utiliser Docker seul (si tu n’utilises pas Compose)

```bash
docker build -t log430-app .
docker run --rm -it log430-app
```

✅ N’oublie le flag `-it` pour rendre le terminal interactif

---

## ✅ Exécution des tests

### 1. Dans Docker (recommandé)

```bash
docker-compose run --rm app pytest
```

---

## 🔁 CI/CD

Une pipeline CI/CD est définie dans `.github/workflows/ci.yml`.  
Elle s’exécute automatiquement à chaque `push` ou `pull_request` sur `main`.

Étapes automatisées :
1. **Lint** avec `black --check .`
2. **Tests** unitaires avec `pytest`
3. **Build** de l’image Docker
4. **Push** sur Docker Hub :  
   `docker.io/<votre_nom_docker>/log430-app:latest`

---

## 🧼 Bonnes pratiques appliquées

- Architecture 2-tier avec couche ORM
- Conteneurisation Docker + orchestration PostgreSQL
- CI/CD complet avec GitHub Actions
- Code structuré et modulaire
- Tests unitaires automatisés
- Style de code unifié avec `black`

---

## 📄 Licence

Projet académique réalisé dans le cadre du cours LOG430 à l’ÉTS (Été 2025).  
Développé par Yassine Graitaa.
