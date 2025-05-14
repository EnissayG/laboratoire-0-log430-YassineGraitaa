# LOG430 - Laboratoire 0 : Infrastructure

## 🧩 Description du projet

Ce dépôt contient une application Python minimaliste développée dans le cadre du Laboratoire 0 du cours **LOG430 – Architecture Logicielle (Été 2025)**.  
L’objectif est de mettre en place une infrastructure de développement moderne avec conteneurisation Docker, tests automatisés, linting, CI/CD et publication sur Docker Hub.

---

## ⚙️ Fonctionnalité de l'application

L’application consiste en une simple fonction `greet(name)` qui affiche ou retourne un message de salutation personnalisé.  
Elle est testée à l’aide de `pytest` et conforme au style `black`.

---

## 🗂️ Structure du projet

```
/
├── app.py                  # Code principal de l'application
├── test_app.py             # Tests unitaires avec pytest
├── Dockerfile              # Image Docker de l'application
├── docker-compose.yml      # Orchestration (à venir à l'étape 5)
├── .github/workflows/ci.yml  # Pipeline CI/CD GitHub Actions
├── .dockerignore           # Fichiers exclus de l'image Docker
├── .gitignore              # Fichiers exclus du repo Git
└── README.md
```

---

## 🚀 Instructions d’exécution

### 1. Cloner le dépôt

```bash
git clone https://github.com/votre-utilisateur/log430-lab0.git
cd log430-lab0
```

### 2. Lancer localement avec Docker

```bash
docker build -t log430-hello .
docker run --rm log430-hello
```

---

## ✅ Exécution des tests

### 1. En local

```bash
pytest
```

### 2. Dans un conteneur Docker

```bash
docker run --rm log430-hello pytest
```

---

## 🔁 CI/CD

Une pipeline CI/CD est définie dans `.github/workflows/ci.yml`.  
Elle s’exécute automatiquement à chaque `push` ou `pull request` sur la branche `main`.

Étapes automatisées :
1. **Lint** avec `black --check .`
2. **Tests** avec `pytest`
3. **Build** de l’image Docker
4. **Push** de l’image vers Docker Hub :  
   `docker.io/<votre_nom_docker>/log430-hello:latest`

---

## 📸 Capture d’écran de la CI/CD
Insez la capture d'ecrean 
---

## 🧼 Bonnes pratiques appliquées

- Environnement virtuel exclu via `.gitignore`
- Conteneur Docker léger basé sur `python:3.11-slim`
- Formatage du code avec `black`
- Tests unitaires automatisés
- CI/CD robuste sur GitHub avec publication vers Docker Hub

---

## 📄 Licence

Projet académique réalisé dans le cadre du cours LOG430 à l’ÉTS (Été 2025).
