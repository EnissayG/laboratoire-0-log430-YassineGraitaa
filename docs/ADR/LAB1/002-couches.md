# ADR 002 – Séparation des responsabilités : présentation, logique métier, persistance

## Contexte

Afin d'assurer la maintenabilité, testabilité et évolutivité du projet, il est essentiel de structurer le code en modules bien séparés selon leur rôle.

## Décision

Nous avons séparé l’application en trois couches principales :
1. **Présentation** (`main.py`) : gestion de l’interface console
2. **Logique métier** (`services.py`) : contient les règles fonctionnelles
3. **Persistance** (`models/`, `db.py`) : gestion de la base de données via SQLAlchemy

## Justification

- **Modularité** : chaque couche peut évoluer indépendamment
- **Testabilité** : la logique métier peut être testée sans dépendre de l’IHM ou de la BDD
- **Bonne pratique logicielle** : favorise la lisibilité, la maintenance et la scalabilité

## Conséquences

- Le projet est structuré clairement
- L’équipe peut travailler de manière plus parallèle et organisée
