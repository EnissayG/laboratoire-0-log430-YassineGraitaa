# ADR-001: Choix de l’architecture microservices

## Statut
Acceptée – 2025-07-16

## Contexte
Le système initial, construit dans les laboratoires précédents, suivait une architecture 3-tiers avec un backend FastAPI monolithique. Cependant, la complexité du domaine e-commerce (produits, stock, ventes, clients, panier, validation) justifie une séparation claire des responsabilités. Le besoin de scalabilité, de répartition de charge, et de déploiement indépendant renforce cette nécessité.

## Décision
Nous avons choisi de migrer vers une **architecture microservices**, en découpant l’application en services indépendants :

- `produits-service`
- `stock-service` (x2, derrière un NGINX load balancer)
- `ventes-service`
- `magasin-service`
- `client-service`
- `panier-service`
- `checkout-service`
- Chaque service possède sa propre base de données PostgreSQL.

Une **API Gateway** (KrakenD) centralise les appels et applique du throttling, des logs et des règles de routage.

## Conséquences

### ✅ Positives
- Meilleure séparation des responsabilités métier
- Déploiement indépendant de chaque service
- Scalabilité horizontale facilitée
- Facilité d’intégration avec des observateurs (Prometheus/Grafana)

### ❌ Négatives
- Complexité accrue : orchestration Docker, configurations, surveillance
- Montée en charge de la CI/CD
- Cohésion entre services à maintenir manuellement (pas de service discovery automatisé)

## Alternatives envisagées
- Garder un monolithe FastAPI mais avec modularisation stricte
- Utiliser une architecture hexagonale au lieu de microservices
