# ADR-002 : Passage d’une architecture 2-tier à une architecture 3-tier distribuée

## Statut
Accepté

## Contexte
Le projet initial (Lab 1) utilisait une architecture 2-tier :
- Un client console (UI + logique métier)
- Une base de données PostgreSQL (accédée directement via SQLAlchemy)

Cette structure est simple mais pose des limites claires :
- ❌ Impossible d’accéder au système à distance (client et base dans le même processus)
- ❌ Difficulté à gérer plusieurs magasins simultanément
- ❌ Interface non réutilisable (ex. pour web ou mobile)
- ❌ Couplage fort entre UI, logique et persistance

## Décision
Nous avons choisi de faire évoluer le système vers une **architecture 3-tier distribuée**, avec les trois couches suivantes :
1. **Client** : application console (et plus tard interface web)
2. **Serveur API** : backend REST développé avec FastAPI
3. **Base de données** : PostgreSQL dans un conteneur Docker

## Raisons
- ✅ Permet d’avoir **plusieurs clients** connectés en même temps (magasins, maison mère)
- ✅ Rend le backend accessible **depuis n’importe quel réseau**
- ✅ Sépare clairement les responsabilités : UI ↔ logique métier ↔ persistance
- ✅ Prépare l’architecture pour une **interface web ou mobile future**
- ✅ Favorise les bonnes pratiques : tests API, CI/CD, déploiement conteneurisé

## Alternatives considérées
- ❌ Rester en 2-tier : impossible de faire évoluer vers multi-client ou consultation distante
- ❌ Monolithique tout-en-un (console + serveur) : non évolutif à long terme
- ❌ Architecture microservices : trop complexe pour l’échelle actuelle

## Conséquences
- La console ne parle plus directement à la base : elle passe par des requêtes HTTP
- Toute nouvelle interface (ex. web) pourra se brancher sur la même API
- Il faut documenter et sécuriser les endpoints de l’API REST
- La gestion des erreurs et des statuts HTTP devient importante (FastAPI facilite ça)

## Auteurs
Yassine Graitaa – Étudiant LOG430
