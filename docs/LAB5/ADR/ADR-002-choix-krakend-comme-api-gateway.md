# ADR-002: Choix de KrakenD comme API Gateway

## Statut
Acceptée – 2025-07-16

## Contexte
Une fois le système découpé en microservices, un besoin de centraliser les appels frontaux est apparu : pour uniformiser les URL, gérer le CORS, appliquer des quotas, et simplifier le point d’entrée du client.

## Décision
Nous avons choisi **KrakenD** comme API Gateway pour son approche déclarative, sa légèreté, et sa capacité à gérer :

- les règles de routage vers les services
- le CORS, les quotas, et le throttling
- des logs structurés
- une configuration JSON simple à intégrer dans notre `docker-compose`

## Conséquences

### ✅ Positives
- Déploiement rapide et sans code (config JSON uniquement)
- Intégration naturelle avec Docker
- Compatible avec Prometheus et Grafana
- Bon support du load balancing (directement ou via NGINX intermédiaire)

### ❌ Négatives
- Moins dynamique qu’une gateway comme Kong ou Traefik (pas de service discovery)
- Gestion manuelle des chemins JSON pour chaque endpoint
- Pas de support avancé OAuth/JWT sans plugins additionnels

## Alternatives envisagées
- Utiliser Traefik (plus flexible mais plus complexe à configurer)
- Développer une API gateway maison avec FastAPI (trop long pour le contexte du labo)
