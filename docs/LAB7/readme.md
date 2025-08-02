# 📦 orchestrateur-service – Saga orchestrée (Lab 6 - LOG430)

Ce microservice constitue le **cerveau de l’architecture microservices** du système de caisse e-commerce multi-magasins. Il implémente une **saga orchestrée synchrone**, permettant de coordonner de manière fiable les étapes critiques d’une commande réparties entre plusieurs services indépendants (`panier`, `stock`, `client`, `ventes`).

À chaque étape du processus, l’orchestrateur valide le succès ou l’échec des appels aux services externes, enregistre les transitions d’état dans une base PostgreSQL, déclenche des actions de **compensation (rollback)** si nécessaire, et met à jour une **machine d’état explicite**. De plus, les transitions sont exposées comme **métriques Prometheus** pour l’observabilité, et intégrées à un dashboard Grafana.

---

## 🧠 Fonctionnalités principales

Ce service gère l’orchestration complète d’une commande (checkout), incluant les étapes suivantes :
- 🔎 Lecture du panier via le `panier-service`
- 📦 Réservation du stock via le `stock-service`
- 💳 Paiement via le `client-service`
- 🧾 Création de la vente via le `ventes-service`

Il assure également :
- Le suivi de l’état courant de chaque commande via l’énumération `EtatCommande`
- La persistance complète des transitions (`Commande`, `EtatSaga`)
- L’exécution de **rollbacks automatiques** en cas d’échec d'une étape
- L’exportation de **métriques Prometheus** accessibles via `/metrics`

---

## 🚀 Endpoints exposés

| Méthode | URI                             | Description                                          |
|--------|----------------------------------|------------------------------------------------------|
| POST   | `/api/commande/checkout`         | Lance la saga pour une nouvelle commande             |
| GET    | `/api/commande/{id}`             | Récupère l’état courant de la commande               |
| GET    | `/metrics`                       | Métriques Prometheus (commande_etat_total, etc.)     |

---

## 📄 Modèles utilisés

### `Commande`
Représente une commande métier initiée. Elle est identifiée par un UUID et contient les informations suivantes :
- `id: UUID` – identifiant unique de la commande (également ID de la saga)
- `client_id: int`
- `magasin_id: int`
- `etat_actuel: str` – état courant de la commande (voir Enum ci-dessous)

### `EtatCommande` (Enum explicite)
Définit les différents états possibles d’une commande au cours de la saga :
- INITIEE
- STOCK_RESERVE
- PAIEMENT_EFFECTUE
- COMMANDE_ENREGISTREE
- CONFIRMEE
- ECHEC_STOCK / ECHEC_PAIEMENT / ECHEC_ENREGISTREMENT
- ANNULEE

### `EtatSaga`
Modèle permettant de conserver un **historique complet** des transitions d’états associées à chaque commande :
- `saga_id: UUID`
- `etat: str`
- `timestamp: datetime`

---

## 📊 Métriques Prometheus

Une métrique clé est exposée via le endpoint `/metrics` :
```python
commande_etat_total{etat="..."}  # compteur de commandes par état
```
Ces métriques sont utilisées dans Grafana pour visualiser la répartition des commandes par étape, la fréquence des erreurs, et les transitions dans le temps.

---

## 🧪 Tests Postman – Simulation de cas réels

Pour valider la robustesse du système, une **collection de tests Postman** est fournie (`saga_checkout_tests.postman_collection.json`). Elle couvre à la fois le **scénario nominal** et plusieurs **échecs simulés**.

### 📌 Instructions

1. Démarrez le système :
```bash
docker-compose up --build orchestrateur-service
```

2. Dans **Postman** :
   - Importez le fichier `.json` via `Import > File`
   - Ouvrez l'onglet **Saga Checkout Tests**
   - Exécutez chaque requête l’une après l’autre

### ✅ Scénarios testés

| Nom du test           | Payload envoyé (`client_id`) | Comportement attendu                                   |
|-----------------------|------------------------------|--------------------------------------------------------|
| ✅ Succès complet     | (client_id: 4+)              | Tous les services répondent, la commande est confirmée |
| ❌ ECHEC STOCK        | client_id: 1                 | Stock insuffisant → ECHEC_STOCK (rollback immédiat)   |
| ❌ ECHEC PAIEMENT     | client_id: 2                 | Paiement échoué → rollback du stock                    |
| ❌ ECHEC ENREGISTREMENT | client_id: 3               | Vente échoue → rollback paiement + stock               |

Chaque test simule un comportement métier réaliste afin de valider les transitions d’états, les compensations, et la robustesse de la machine d’état.

---

## 🧱 Dépendances techniques

- Python 3.11
- FastAPI
- SQLAlchemy
- httpx
- prometheus-fastapi-instrumentator
- PostgreSQL
- Docker / Docker Compose

---

## 🐳 Déploiement local

```bash
docker-compose up --build orchestrateur-service
```

- 📘 Swagger : http://localhost:8023/docs
- 📊 Prometheus : http://localhost:9090

---

## 👨‍💻 Auteur

Projet réalisé par **Yassine Graitaa**, dans le cadre du cours **LOG430 – Architecture logicielle**, session d’été 2025, ÉTS.