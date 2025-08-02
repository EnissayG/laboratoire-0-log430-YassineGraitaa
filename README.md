# LOG430 – Laboratoire 1 à 6 : Système de caisse distribué observé 🧾🔁📊

## 🧩 Description du projet

Ce projet suit l'évolution progressive d'un système de caisse initialement local vers une architecture distribuée et observable, en passant par une API REST, une scalabilité complète et une orchestration de processus critiques via une saga. Il est réalisé dans le cadre du cours **LOG430 – Architecture Logicielle (Été 2025)** à l’ÉTS.

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
- 🧭 Load Balancer (NGINX) avec 3 stratégies :
  - Round Robin
  - Least Connections
  - IP Hash
- 📈 Monitoring complet :
  - Prometheus
  - Grafana (latence, trafic, erreurs, CPU, connexions)
- 🧪 Test de charge avec **K6**
- ⚠️ Test de tolérance aux pannes (instances down)
- ⚡ Impact du cache observé via métriques live

### Lab 5 – Microservices, Gateway et Résilience
- 🚀 Microservices découpés par domaine (produits, ventes, stock, panier, clients...)
- 🌐 API Gateway KrakenD : centralisation et routage
- 🔐 CORS, throttling global (max_rate)
- 🧪 Tests de charge avec K6 (jusqu’à 100 VUs)
- ✅ Réplication `stock-service`
- ⚠️ Simulation de pannes / tolérance validée

### Lab 6 – Saga orchestrée et machine d’état
- 🤖 Implémentation d'une **saga orchestrée synchrone**
- 🧠 Gestion explicite de l'état (`EtatCommande`)
- 💾 Persistance des transitions (`EtatSaga`)
- ♻️ Rollback automatiques (stock, paiement, vente)
- 📊 Métriques Prometheus : états de commande
- 🧪 Tests Postman avec scénarios d’échec simulés

---

## 🗂️ Structure du projet

```
/
├── microservices/
│   ├── produits-service/
│   ├── ventes-service/
│   ├── stock-service/
│   ├── client-service/
│   ├── panier-service/
│   ├── checkout-service/
│   ├── orchestrateur-service/
│   └── krakend/
├── frontend/dashboard/
├── nginx/
├── prometheus/
├── test.js
├── docker-compose.yml
├── docker-compose.observ.yml
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
- Résultats visibles sur Grafana

### Tests Postman pour la saga orchestrée (Lab 6)

1. Importer `saga_checkout_tests.postman_collection.json` dans Postman
2. Lancer les cas suivants :
   - ✅ client_id: 4 → succès complet
   - ❌ client_id: 1 → échec stock
   - ❌ client_id: 2 → échec paiement
   - ❌ client_id: 3 → échec enregistrement vente

Chaque test déclenche un scénario complet avec journalisation et rollback.

---

## 🧠 Recommandations finales

| Aspect       | Amélioration                                   |
|--------------|------------------------------------------------|
| SQL          | Indexation + analyse EXPLAIN                   |
| Cache        | fastapi-cache2 pour les agrégats               |
| Résilience   | Automatiser les rollbacks                      |
| Observabilité| Plus de métriques métier                       |
| Sécurité     | Gestion de rôles + authentification centralisée|
| CI/CD        | GitHub Actions (tests, lint, build, push)      |

---

## 📄 Licence

Projet académique – ÉTS 2025  
Développé par **Yassine Graitaa** – LOG430  
📅 Dernière mise à jour : **2025-08-01**