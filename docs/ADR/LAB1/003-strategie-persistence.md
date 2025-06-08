# ADR 003 – Stratégie de persistance

## Contexte

L'application doit stocker durablement les informations liées aux produits, ventes, retours, etc., avec fiabilité et support des transactions.

## Décision

Nous avons choisi :
- D’utiliser une base de données relationnelle PostgreSQL
- De passer par un ORM (SQLAlchemy) pour gérer l’accès à la base

## Justification

- **Transactions complexes** : PostgreSQL gère bien les opérations multi-tables
- **Requêtes structurées** : relations entre ventes, produits, lignes
- **ORM** : simplifie le code, évite les requêtes SQL manuelles, rend la logique portable

## Conséquences

- Nécessite une configuration PostgreSQL dans Docker Compose
- Le code SQL est géré par SQLAlchemy de manière abstraite
