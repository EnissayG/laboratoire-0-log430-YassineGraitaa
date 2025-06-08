# ADR 004 – Choix de la base de données : SQL vs NoSQL, local vs serveur

## Contexte

L'application nécessite une base fiable pour stocker des objets fortement structurés et liés (produits, ventes, utilisateurs), dans un contexte mono-magasin avec possibilité d’évolution future.

## Décision

- Type : **SQL**
- Système : **PostgreSQL**
- Hébergement : **Conteneur séparé (serveur local)**

## Justification

- **SQL** : modèle relationnel mieux adapté aux opérations transactionnelles
- **PostgreSQL** : robuste, mature, bien supporté avec Docker
- **Local (dans VM)** : performant et autonome sans dépendre d’un service externe
- **Séparation logique** : base et application tournent dans des processus distincts (2-tier)

## Conséquences

- Configuration Docker plus complète
- Possibilité d'évolution vers une BDD distante dans les Lab 2/3
