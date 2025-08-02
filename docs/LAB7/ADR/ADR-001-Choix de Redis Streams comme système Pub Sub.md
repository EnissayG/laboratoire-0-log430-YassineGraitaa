# ADR 1 – Choix de Redis Streams comme système Pub/Sub

## Statut
Accepté

## Contexte
Dans le cadre de la migration vers une architecture événementielle distribuée, il était nécessaire d’introduire un mécanisme de communication asynchrone entre les microservices. Plusieurs solutions étaient envisageables : Kafka, RabbitMQ, Redis Streams, etc. Le système choisi devait être simple à intégrer, compatible avec les conteneurs Docker existants, supportant les groupes de consommateurs, et offrir une persistance minimale des messages.

## Décision
Nous avons retenu Redis Streams comme système de messagerie Pub/Sub pour coordonner les microservices dans le cadre du laboratoire.

## Justification
- Redis Streams est directement supporté par l'image Docker officielle de Redis, déjà présente dans le projet.
- Il permet la création de **groupes de consommateurs** (`XGROUP`) avec lecture parallèle (`XREADGROUP`), convenant à une architecture scalable.
- L’API de Redis est simple et bien supportée en Python (`redis-py`).
- Redis ne nécessite pas de configuration complexe ni d’installation supplémentaire contrairement à Kafka.
- Les performances sont suffisantes pour un usage académique et démonstratif.

## Conséquences
- La solution n’est pas aussi robuste ni scalable que Kafka en production.
- Le stockage des événements dans Redis est temporaire. Une solution complémentaire a été mise en place via un Event Store pour la persistance longue durée.
- Le choix de Redis permet une montée en charge raisonnable, mais un changement vers Kafka pourrait être envisagé dans un contexte professionnel.

## Alternatives envisagées
- Kafka : trop lourd à configurer et monitorer dans un environnement de laboratoire.
- RabbitMQ : nécessitait un autre type d’interface et de configuration (notamment AMQP), sans avantage décisif par rapport à Redis pour ce projet.
