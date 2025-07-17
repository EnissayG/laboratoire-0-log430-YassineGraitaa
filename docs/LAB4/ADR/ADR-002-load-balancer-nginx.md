# ADR-004 : Choix de NGINX comme Load Balancer

## Statut
Accepté – 2025-07-15

## Contexte
Dans le cadre du Laboratoire 4, nous devions déployer plusieurs instances de notre service FastAPI et équilibrer la charge entre elles. Il fallait un outil simple, léger et compatible avec Docker pour assurer ce routage.

## Décision
Nous avons choisi **NGINX** comme Load Balancer HTTP pour les raisons suivantes :
- Faible empreinte mémoire.
- Configuration simple (fichier `nginx.conf`).
- Support du round-robin, least connections, IP hash, weighted.
- Intégration facile avec Prometheus via `nginx-prometheus-exporter`.

## Conséquences
- NGINX a été placé devant les services `fastapi1`, `fastapi2`, `fastapi3`.
- Le trafic passe par `http://localhost:8081`, redirigé dynamiquement vers une instance disponible.
- La stratégie de load balancing est interchangeable via `nginx.conf`.
- Exposition d’un endpoint `/nginx_status` pour les métriques.
