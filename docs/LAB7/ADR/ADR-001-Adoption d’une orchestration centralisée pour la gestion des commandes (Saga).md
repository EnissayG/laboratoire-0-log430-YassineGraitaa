# 🧠 ADR #1 – Adoption d’une orchestration centralisée pour la gestion des commandes (Saga)

## 🎯 Contexte

Dans le cadre du Laboratoire 6 du cours LOG430 (Été 2025), nous devions gérer une transaction répartie sur plusieurs microservices (panier, stock, client, ventes) de manière fiable, avec rollback en cas d’échec. Deux approches étaient envisageables : **orchestration centralisée** ou **chorégraphie distribuée**.

## ✅ Décision

Nous avons choisi de centraliser la coordination dans un microservice dédié, appelé `orchestrateur-service`, qui implémente une **saga orchestrée synchrone**.

## 📌 Conséquences

- Un seul point de décision contrôle l’ordre et les transitions de la saga.
- L’**état de la commande** est maintenu dans une machine d’état persistée (`etat_actuel` dans `Commande` + historique dans `EtatSaga`).
- Le service `orchestrateur-service` gère les appels HTTP interservices, les erreurs, et les actions compensatoires (rollback).
- Chaque état est instrumenté avec des métriques Prometheus (`commande_etat_total`), facilitant le suivi.

## 📉 Alternatives envisagées

- **Chorégraphie distribuée** : chaque service déclenche l’étape suivante via des événements asynchrones.
  - Avantage : découplage maximal
  - Inconvénient : complexité accrue, difficile à suivre et tester
  - Nécessite un bus de messages (RabbitMQ, Kafka)

## 🧩 Justification

- Nous voulions maximiser la clarté, la testabilité et la traçabilité des transitions.
- Le style synchrone et impératif de l’orchestration est mieux adapté pour un laboratoire avec contraintes de temps, sans infra Kafka.
- Permet d’ajouter facilement des métriques, des logs, et des tests de bout en bout.

## 🛠️ Implémentation

- `orchestrateur-service` implémente la logique complète de la saga.
- La progression est journalisée dans `EtatSaga`, et l’état courant dans `Commande`.
- Le tout est exposé via des endpoints REST (`/checkout`, `/commande/{id}`).

---

