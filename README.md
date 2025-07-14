# LOG430 – Laboratoire 1, 2, 3 & 4 : Système de caisse distribué observé 🧾🔁📊

## 🧩 Description du projet

Ce projet évolue d’une application **console (Lab 1)** vers une **architecture 3-tier distribuée (Lab 2)**, une **API RESTful avancée (Lab 3)**, puis une **infrastructure scalable avec monitoring et tolérance aux pannes (Lab 4)**.

Développé dans le cadre du cours **LOG430 – Architecture Logicielle (Été 2025)** à l’ÉTS.

---

## ⚙️ Fonctionnalités de l'application

### Lab 1 – Console (2-tier)
- 🔍 Rechercher un produit
- 🛒 Enregistrer une vente
- ➕ Ajouter un produit
- ❌ Annuler une vente
- 📦 Consulter le stock

### Lab 2 – Architecture 3-tier (FastAPI + React + PostgreSQL)
- 🧠 Séparation claire des responsabilités (services)
- 🌐 API REST : ventes, produits, magasins, réapprovisionnement
- 📊 Dashboard React (UC3)
- 🧾 Rapport de ventes et stock (UC1 & UC2)

### Lab 3 – API REST avancée
- ✅ Authentification (`x-token`)
- 🔐 Sécurisation des routes critiques
- 📜 Swagger personnalisé (`custom_openapi`)
- 🧪 Tests `.http` + Pytest
- 📦 Gestion d’erreurs formatée
- 🔍 Filtrage / tri / pagination (bonus)
- ⚡ Cache LRU sur `/performance/global`

### Lab 4 – Observabilité & Scalabilité
- 🧭 Load Balancer (NGINX) avec 3 stratégies comparées :
  - Round Robin
  - Least Connections
  - IP Hash
- 📈 Monitoring complet :
  - Prometheus
  - Grafana (latence, trafic, erreurs, CPU, connexions)
- 🧪 Test de charge avec **K6**
- ⚠️ Test de tolérance aux pannes (instances down)
- ⚡ Impact du cache observé en live via métriques

---

## 🗂️ Structure du projet

```
/
├── app/                      # Backend FastAPI
│   ├── routers/              # Points d’entrée REST (magasins, produits, etc.)
│   ├── services/             # Logique métier (vente_service, etc.)
│   ├── models.py / db.py / schemas.py / securite.py
├── tests/                    # Fichiers .http + tests unitaires
├── frontend/dashboard/       # React dashboard (perf UC3)
├── nginx/                    # Fichiers nginx.conf
├── prometheus/               # Fichier prometheus.yml
├── docker-compose.yml        # Compose main (FastAPI + DB + NGINX + Exporter)
├── docker-compose.observ.yml # Compose Prometheus + Grafana
└── README.md
```

---

## 🚀 Lancement local

```bash
# Cloner le dépôt
git clone https://github.com/EnissayG/laboratoire-0-log430-YassineGraitaa.git
cd laboratoire-0-log430-YassineGraitaa/
```

### Lancer l'application principale

```bash
docker-compose up --build
```

- API Swagger : http://localhost:8000/docs
- Frontend React : http://localhost:3000
- Load Balancer : http://localhost:8081

### Lancer les outils d’observabilité

```bash
docker-compose -f docker-compose.observ.yml up --build
```

- Prometheus : http://localhost:9090
- Grafana : http://localhost:3009 (admin/admin)

💡 Ajoutez un header `x-token: mon-token-secret` sur les routes protégées.

---

## 🧪 Tests et Monitoring

### Test de charge (`K6`)

```bash
k6 run test.js
```

Effectué avec 3, 2 puis 1 instance active pour valider la résilience du système.

### Test de tolérance aux pannes

```bash
docker stop fastapi2
docker stop fastapi3
```

➡️ Vérification dans Grafana des courbes de latence, erreurs et trafic.

---

## 📊 Dashboards Grafana

Suivi en temps réel :
- ⏱ Latence moyenne par handler
- 🔁 Nombre de connexions (NGINX)
- ⚠️ Erreurs 4xx / 5xx
- 📦 Charge CPU
- 🎯 Impact du cache activé

---

## 📚 Swagger API (customisé)

- Summary / description
- `response_model` cohérent
- Champs `example=`
- Sécurité `x-token` visible

---

## ✅ CI/CD – GitHub Actions

- ✅ Formatage (`black`)
- ✅ Tests (`pytest`)
- ✅ Build docker
- 🔁 Déclenché à chaque `push`

---

## 🧠 Recommandations finales

- 🧠 Le cache améliore nettement la latence et la charge.
- 🔁 Round Robin est équilibré, IP Hash garantit l’affinité client.
- 🔥 Le système reste fonctionnel avec seulement 1 instance active.
- 📦 Architecture modulaire, scalable et observable.

---

## 📄 Licence

Projet académique – ÉTS 2025  
Développé par **Yassine Graitaa** – LOG430  
📅 Dernière mise à jour : **2025-07-14**