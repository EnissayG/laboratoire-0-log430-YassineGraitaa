
# LOG430 – Laboratoire 1, 2, 3, 4 & 5 : Système de caisse distribué observé 🧾🔁📊

## 🧩 Description du projet

Ce projet évolue d’une application **console (Lab 1)** vers une **architecture 3-tier distribuée (Lab 2)**, une **API RESTful avancée (Lab 3)**, une **infrastructure scalable avec monitoring et tolérance aux pannes (Lab 4)**, et enfin une **architecture microservices avec API Gateway, Load Balancer et Observabilité (Lab 5)**.

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

### Lab 5 – Microservices, Gateway et Résilience
- 🚀 Microservices découpés par domaine (produits, ventes, stock, panier, clients...)
- 🌐 API Gateway KrakenD : centralisation et routage
- 🔐 CORS, throttling global (max_rate)
- 🧪 Tests de charge avec K6 (jusqu’à 100 VUs)
- 📊 Comparaison directe architecture monolithe vs microservices
- ✅ NGINX + plusieurs instances stock-service
- ⚠️ Simulation de pannes / tolérance validée

---

## 🗂️ Structure du projet

```
/
├── microservices/
│   ├── produits-service/
│   ├── ventes-service/
│   ├── stock-service/      # Répliqué en plusieurs instances
│   ├── client-service/
│   ├── panier-service/
│   ├── checkout-service/
│   └── krakend/            # Fichier krakend.json
├── frontend/dashboard/     # React dashboard
├── nginx/                  # nginx.conf + exporters
├── prometheus/             # prometheus.yml
├── test.js                 # Script de charge K6
├── docker-compose.yml      # Compose principal
├── docker-compose.observ.yml # Compose Prometheus + Grafana
└── README.md
```

---

## 🚀 Lancement local

```bash
git clone https://github.com/EnissayG/laboratoire-0-log430-YassineGraitaa.git
cd laboratoire-0-log430-YassineGraitaa/
docker-compose up --build
```

- API Gateway : http://localhost:8090
- NGINX Load Balancer : http://localhost:8081
- Frontend React : http://localhost:3000
- Swagger (produits-service) : http://localhost:8020/docs

### Outils d’observabilité

```bash
docker-compose -f docker-compose.observ.yml up --build
```

- Prometheus : http://localhost:9090
- Grafana : http://localhost:3009 (admin/admin)

---

## 🧪 Tests de charge & tolérance

- `k6 run test.js` → Simulation 100 VUs sur `/api/magasins/1/stock`
- `docker stop stock-service-2` → Test de résilience

Résultats observables dans Grafana : latence, erreurs, CPU, connexions.

---

## 🧠 Recommandations finales

| Aspect | Amélioration |
|--------|--------------|
| SQL    | Indexation, requêtes optimisées |
| Cache  | fastapi-cache2 sur endpoints agrégés |
| Scalabilité | Load balancing horizontal efficace |
| Observabilité | Grafana prêt à l’emploi avec panels |
| Sécurité | Authentification simple par token + throttling |
| CI/CD  | GitHub Actions (tests, build, format) |

---

## 📄 Licence

Projet académique – ÉTS 2025  
Développé par **Yassine Graitaa** – LOG430  
📅 Dernière mise à jour : **2025-07-16**
