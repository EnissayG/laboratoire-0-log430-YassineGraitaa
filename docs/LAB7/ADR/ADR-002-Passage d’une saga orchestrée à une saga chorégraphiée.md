# ADR 2 – Passage d’une saga orchestrée à une saga chorégraphiée

## Statut
Accepté

## Contexte
Lors du Laboratoire 6, la coordination entre les microservices était assurée par un service orchestrateur central. Celui-ci déclenchait les appels de manière séquentielle et contrôlait l’avancement de la commande à travers une machine d’état. Cette approche bien qu’efficace présente une dépendance forte à l’orchestrateur. Le Laboratoire 7 propose d’explorer un modèle alternatif : la saga chorégraphiée.

## Décision
Nous avons remplacé la coordination centralisée par une saga chorégraphiée où chaque microservice écoute les événements métier, agit en fonction de ceux-ci, et publie de nouveaux événements.

## Justification
- Réduction du **couplage** : chaque microservice est autonome et responsable de son comportement.
- Amélioration de la **tolérance aux pannes** : la perte d’un service n’affecte pas la coordination globale.
- Meilleure **scalabilité** : chaque service peut être répliqué sans coordination centrale.
- Simplicité du flux événementiel : les événements publiés deviennent l’interface unique entre les services.
- Le modèle est plus représentatif d’un système distribué moderne orienté événements.

## Conséquences
- La coordination devient plus difficile à tracer sans observabilité renforcée (logs, métriques).
- Il faut une gestion explicite des événements compensatoires (rollback) dans chaque service.
- La documentation et les projections deviennent essentielles pour reconstituer les états métier (solution : Event Store + `/projections/{id}`).

## Alternatives envisagées
- Conserver l’orchestrateur (Laboratoire 6) avec un enrichissement pour la persistance et la résilience. Cette approche aurait été plus centralisée mais moins distribuée.
- Utiliser un broker plus riche (Kafka) avec des outils de traceability intégrés (non retenu ici).
