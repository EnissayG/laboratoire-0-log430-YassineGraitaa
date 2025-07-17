# ADR-005 : Mise en cache des endpoints critiques

## Statut
Accepté – 2025-07-16

## Contexte
Certains endpoints du système sont fortement sollicités ou coûteux à exécuter car ils effectuent des agrégations complexes ou parcourent beaucoup de données. Une latence excessive a été observée lors des tests de charge.

## Décision
Nous avons décidé d’ajouter un **cache mémoire local** sur les endpoints suivants :
- `/api/performance/global`
- `/api/rapports/ventes`
- `/api/stock`

Les fonctions Python correspondantes ont été décorées avec `@lru_cache()` (ou `functools.cache()`).

## Conséquences
- Réduction significative du nombre d’appels SQL en base.
- Amélioration de la latence des réponses.
- Risque de données obsolètes atténué par la faible fréquence de mise à jour de ces endpoints.
- La stratégie reste simple, mais pourrait évoluer vers un cache Redis à l’avenir.
