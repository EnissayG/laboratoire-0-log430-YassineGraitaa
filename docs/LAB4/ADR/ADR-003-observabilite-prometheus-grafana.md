# ADR-006 : Choix de Prometheus et Grafana pour l'observabilité

## Statut
Accepté – 2025-07-16

## Contexte
Dans le Laboratoire 4, l’un des objectifs était d’intégrer des outils de supervision afin de mesurer et visualiser les performances du système distribué (latence, trafic, erreurs, saturation…). Il fallait des outils compatibles avec Docker, faciles à configurer et largement adoptés.

## Décision
Nous avons retenu le couple **Prometheus** (pour la collecte des métriques) et **Grafana** (pour la visualisation).

### Raisons du choix :
- Écosystème mature et bien documenté.
- Intégration native avec FastAPI via `prometheus_fastapi_instrumentator`.
- Exporter officiel disponible pour NGINX (`nginx-prometheus-exporter`).
- Dashboard personnalisable en quelques clics.
- Compatible avec Docker et Kubernetes (standard de facto en entreprise).

## Conséquences
- Prometheus scrute deux cibles :
  - `/metrics` exposé par FastAPI.
  - `/nginx_status` exposé via un container `nginx-exporter`.
- Grafana affiche :
  - 📈 Latence moyenne.
  - 🔥 Saturation CPU.
  - 🚦 Nombre de connexions.
  - ❌ Erreurs 4xx/5xx.
- Cela nous a permis :
  - D’observer l’impact de la mise en cache.
  - D’analyser le comportement sous charge.
  - De valider la résilience lors de la défaillance d’une instance.
- Ces outils seront également réutilisés au **Laboratoire 5**.

## Alternatives envisagées
- **ELK Stack** (Elasticsearch, Logstash, Kibana) : trop complexe pour le contexte du labo.
- **Datadog, NewRelic** : solutions cloud, mais non open-source.
