# 🧾 LOG430 – Laboratoire 7 : Architecture Événementielle (Pub/Sub, Event Sourcing, CQRS, Saga Chorégraphiée)

## 🧩 Contexte

Ce laboratoire met en œuvre une architecture événementielle complète, évoluant depuis une saga orchestrée (Lab 6) vers un système distribué résilient reposant sur :
- Redis Streams (Pub/Sub)
- Event Sourcing avec Event Store dédié
- CQRS
- Saga chorégraphiée avec compensation
- Observabilité Prometheus + Grafana

---

## ⚙️ Microservices

| Service            | Rôle                                                 |
|--------------------|------------------------------------------------------|
| `panier-service`   | Génère `CommandeCreee`                               |
| `stock-service`    | Réserve ou libère le stock (`StockReserve`, `StockIndisponible`) |
| `client-service`   | Tente le paiement (`PaiementAccepte`, `PaiementRefuse`) |
| `ventes-service`   | Enregistre la vente si paiement OK                   |
| `event-store`      | Stocke tous les événements + API `/events/` & `/projections/` |

---

## 🚀 Déploiement

```bash
docker-compose build
docker-compose up -d
```

Services exposés :
- KrakenD : http://localhost:8090
- Grafana : http://localhost:3000 (admin/admin)
- Prometheus : http://localhost:9090
- Event Store : http://localhost:8028/docs

---

## 📬 Simulation d’un scénario

1. ✅ `POST /api/commande/depuis-panier/{id}` (panier-service)
2. 🔁 Redis Streams : chaque service réagit (stock → client → ventes)
3. 📥 Event Store reçoit tous les événements (`POST /events`)
4. 🔎 Projection accessible : `/events/projections/{aggregate_id}`

---

## 📊 Observabilité

- `/metrics` exposé par `event-store`
- Métrique : `event_store_events_total{event_type, source}`
- Dashboard Grafana : activité, répartition, latence, etc.

---

## 🧪 Tests & Échecs simulés

- Échecs de stock (`quantité insuffisante`) déclenchent `StockIndisponible`
- Paiements aléatoires → `PaiementRefuse` ou `PaiementAccepte`
- Compensation automatique via rollback stock

---

## 📄 Pour aller plus loin

- Lire projection : `/events/projections/{id}`
- Générer un rapport PDF/Markdown : scénario, diagramme saga, ADRs, etc.
