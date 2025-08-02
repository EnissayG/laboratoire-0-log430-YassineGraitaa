# 1. Introduction et motivation

Ce document présente l’architecture du **microservice `orchestrateur-service`**, développé dans le cadre du **Laboratoire 6** du cours **LOG430 – Architecture logicielle** (ÉTS, été 2025). Ce laboratoire s’inscrit dans la continuité des précédents (Labos 3, 4 et 5) où une application de gestion multi-magasins a évolué d’un monolithe vers une architecture distribuée à base de microservices, orchestrée par une API Gateway.

Le `orchestrateur-service` a pour rôle principal de **coordonner l’exécution de commandes complexes** impliquant plusieurs services (panier, stock, client, ventes). Il implémente une **saga orchestrée synchrone**, permettant de garantir la cohérence globale même en cas d’échec partiel. Il encapsule :

- La **gestion explicite de l’état d’une commande**, sous forme de machine d’état (Enum, persistance SQL).
- La **compensation automatique** en cas d’échec d’une étape (ex. libération du stock, remboursement).
- L’enregistrement **historique des transitions** pour la traçabilité (`EtatSaga`).
- L’**exposition de métriques Prometheus** pour l’observabilité (par état de commande).
- Une interface API REST simple (checkout, consultation).

L’introduction de cette orchestration est cruciale dans un système distribué, où chaque microservice est indépendant et peut échouer : elle permet de centraliser la logique de coordination tout en respectant le principe de découplage.

Ce rapport documente donc le design, les responsabilités, les décisions techniques et les interactions de ce microservice clé dans l’écosystème du système multi-magasins.

# 2. Contraintes

Le `orchestrateur-service` a été développé sous plusieurs contraintes fonctionnelles, techniques et d’infrastructure, définies par le contexte du projet LOG430 – Été 2025. Ces contraintes ont guidé la conception et l’implémentation du microservice.

## 2.1 Contraintes fonctionnelles

- **Saga orchestrée synchrone** : La coordination des étapes d’une commande doit être effectuée de façon synchrone, selon un enchaînement bien défini (panier → stock → paiement → vente).
- **Rollback partiel obligatoire** : En cas d’échec à une étape, le système doit déclencher des actions de compensation (ex. remboursement, libération du stock).
- **Persistance de l’état** : L’état courant d’une commande doit être sauvegardé dans une base de données, avec un historique des transitions.
- **Consultation de commande** : Il doit être possible de consulter l’état actuel d’une commande via un endpoint GET.

## 2.2 Contraintes techniques

- **Microservices** : Le service s’intègre dans une architecture distribuée avec des services indépendants (FastAPI) communiquant via HTTP.
- **Interservices asynchrones (httpx)** : Toutes les communications avec les services distants se font via `httpx.AsyncClient` pour éviter le blocage du serveur.
- **Base de données PostgreSQL** : Le service utilise PostgreSQL pour stocker les commandes (`Commande`) et leur historique (`EtatSaga`).
- **Prometheus pour observabilité** : Des métriques par état de commande doivent être exposées via `/metrics` (FastAPI Instrumentator).
- **Orchestration centralisée** : Le service agit comme le coordinateur unique des étapes, sans attendre d’événement externe (vs chorégraphie).

## 2.3 Contraintes d’infrastructure

- **Déploiement Dockerisé** : Le service doit être lancé via `docker-compose` dans un environnement multi-conteneurs.
- **Intégration à une API Gateway (Krakend)** : L’orchestrateur doit être accessible via la passerelle KrakenD, comme les autres services.
- **Port par défaut :8000**, réseau `backend` commun.
- **Monitoring commun avec Prometheus et Grafana**.

## 2.4 Contraintes pédagogiques

- Le laboratoire vise à simuler une **transaction répartie robuste** sur plusieurs services, avec journalisation d’état et mécanisme de reprise.
- L’implémentation de la machine d’état est évaluée, ainsi que sa clarté, sa traçabilité et sa capacité à refléter les erreurs du système.


# 3. Vue contextuelle

Le `orchestrateur-service` s’inscrit dans une architecture distribuée orientée microservices mise en place pour simuler un système de gestion de magasins en ligne. Chaque microservice est responsable d’un domaine métier (stock, client, ventes, panier, etc.) et expose ses fonctionnalités via des API REST. L’orchestrateur agit comme **point central de coordination** pour toutes les étapes critiques d’une commande.

Il ne possède pas de logique métier propre, mais orchestre celles des autres services selon une séquence rigide et résiliente. Il implémente une saga transactionnelle synchrone qui s’appuie sur des appels HTTP interservices, avec gestion d’erreurs et compensation.

## 3.1 Parties prenantes et environnement

Le système cible deux types d’utilisateurs :
- **Clients** : peuvent créer un compte, naviguer dans les produits, remplir leur panier et valider une commande.
- **Employés** : peuvent gérer le catalogue de produits, les magasins, les stocks, et consulter les rapports.

Les utilisateurs interagissent avec un **frontend React**, qui communique avec les microservices via une **API Gateway** (Krakend). Tous les services sont déployés dans un environnement Dockerisé et communiquent sur le réseau `backend`.

## 3.2 Rôle de l’orchestrateur

Le `orchestrateur-service` ne reçoit des requêtes que via un **endpoint unique** (`/checkout`) qui déclenche la saga. Il interagit ensuite avec les microservices suivants :

- **`panier-service`** : pour lire les produits à commander
- **`stock-service`** : pour réserver ou libérer le stock
- **`client-service`** : pour effectuer ou rembourser le paiement
- **`ventes-service`** : pour enregistrer la vente

Il maintient en base de données :
- l’état courant de la commande (`Commande`)
- l’historique des transitions d’état (`EtatSaga`)

L’API permet aussi de **consulter une commande** pour connaître son état actuel. L’orchestrateur expose également des **métriques Prometheus**, utilisées pour monitorer les transitions d’état à des fins d’observabilité.

## 3.3 Diagramme de contexte

![alt text](image.png)



# 4. Vue logique
![alt text](image-1.png)
Le `orchestrateur-service` est conçu selon une architecture **modulaire et claire**, inspirée des bonnes pratiques FastAPI. Chaque composant de la logique métier est isolé dans son propre dossier : `routers`, `services`, `models`, `schemas`, et `db`.

L’objectif est de séparer les responsabilités : chaque module a un rôle précis dans l’orchestration de la saga.

## 4.1 Découpage logique

- `routers/commande_orchestration.py` : point d’entrée HTTP, expose les endpoints `/checkout` et `/commande/{id}`.
- `services/saga_checkout.py` : logique principale d’orchestration, enchaîne les appels aux services distants via `httpx`.
- `services/etat_commande.py` : fonction `changer_etat_commande` centralisée pour gérer les transitions d’états, la persistance et les métriques Prometheus.
- `models/commande.py` : entité SQLAlchemy persistée, représente une commande avec son état courant.
- `models/etat_saga.py` : entité SQLAlchemy représentant une transition historique (pour audit).
- `models/etat_commande_enum.py` : énumération stricte de tous les états possibles d’une commande (de `INITIEE` à `CONFIRMEE` ou `ANNULEE`).
- `schemas.py` : modèles Pydantic d’entrée (par exemple `CommandeInput`), utilisés pour valider les requêtes.
- `metrics.py` : compteur Prometheus par état de commande (`commande_etat_total`).

## 4.2 Comportement de la saga

La saga suit les étapes suivantes :
1. **INITIEE** : la commande est créée, avec UUID.
2. **Récupération panier** (`panier-service`)
3. **Réservation stock** (`stock-service`)
4. **Paiement** (`client-service`)
5. **Enregistrement vente** (`ventes-service`)
6. **Succès** : `CONFIRMEE`
7. **En cas d’échec** : rollback stock/paiement + état `ANNULEE`

Chaque changement d’état est :
- Sauvegardé dans `EtatSaga`
- Répercuté dans `Commande.etat_actuel`
- Compteur Prometheus incrémenté

## 4.3 Avantages de cette structuration

- Modularité testable et remplaçable
- Possibilité d’ajouter d’autres étapes à la saga
- Facilité d’observabilité (Prometheus + historique)
- Adaptation à d'autres types d’orchestrations futures (ex : chorégraphiées)


# 5. Vue de développement

Le microservice `orchestrateur-service` est structuré selon les bonnes pratiques Python/FastAPI, avec une organisation claire des fichiers, facilitant la maintenabilité, les tests et l’extension.

## 5.1 Organisation des fichiers

```
orchestrateur-service/
├── app/
│   ├── main.py                      # Point d’entrée de l’application FastAPI
│   ├── db/
│   │   └── database.py              # Session DB, engine PostgreSQL
│   ├── routers/
│   │   └── commande_orchestration.py  # Endpoints: checkout, get commande
│   ├── services/
│   │   ├── saga_checkout.py         # Logique principale d’orchestration
│   │   └── etat_commande.py         # Fonction centrale pour gérer les transitions
│   ├── models/
│   │   ├── commande.py              # Modèle SQL de la commande
│   │   ├── etat_saga.py             # Historique des transitions
│   │   └── etat_commande_enum.py    # Enum des états possibles
│   ├── schemas.py                   # Modèles Pydantic (CommandeInput)
│   └── metrics.py                   # Exposition des métriques Prometheus
├── Dockerfile
├── requirements.txt
└── ...

```

## 5.2 Technologies utilisées

- **FastAPI** : framework web asynchrone
- **SQLAlchemy** : ORM relationnel pour PostgreSQL
- **httpx** : client HTTP asynchrone pour les appels interservices
- **Prometheus FastAPI Instrumentator** : exposition des métriques
- **Docker** : conteneurisation complète
- **PostgreSQL** : persistance locale pour les commandes et transitions

## 5.3 Diagrammes de composants et d’implémentation

![alt text](image-2.png)

# 6. Vue de déploiement

Le `orchestrateur-service` s’inscrit dans une infrastructure Docker multi-conteneurs, interconnectée à travers un réseau interne (`backend`) et exposée via une API Gateway (`krakend-gateway`). Chaque microservice est conteneurisé indépendamment, facilitant le scaling, le monitoring et la gestion des pannes.

## 6.1 Environnement d’exécution

- **Conteneur Docker** : Le service tourne dans un container FastAPI (Python 3.11), exposé sur le port `8000`.
- **Réseau Docker `backend`** : utilisé pour la communication avec les autres microservices.
- **PostgreSQL** : chaque microservice possède sa propre instance dédiée de PostgreSQL. Ici, la base contient les tables `commande` et `etat_saga`.
- **Prometheus** : la route `/metrics` permet d’exporter les métriques du service.
- **Grafana** : connecté à Prometheus pour visualiser l’état des commandes.

## 6.2 Intégration CI/CD (optionnelle)

- Le build se fait via `docker-compose up --build orchestrateur-service`.
- Des tests Postman manuels valident les cas de succès/échec via l’endpoint `/checkout`.

## 6.3 Dépendances réseau

Le service communique en HTTP asynchrone avec :

- `panier-service` → pour récupérer les produits à commander.
- `stock-service` → pour réserver ou libérer le stock.
- `client-service` → pour effectuer le paiement ou le remboursement.
- `ventes-service` → pour enregistrer la vente en base.

## 6.4 Diagramme de déploiement

![alt text](image-3.png)


## 6.5 Diagramme d'états de la saga
![alt text](image-8.png)

# 7. Vue logique

Cette vue décrit la structure interne du `orchestrateur-service` en termes de **composants logiciels**. Elle présente les modules principaux qui composent le service, leurs rôles et leurs interactions.

## 7.1 Composants principaux

Le microservice est structuré selon les conventions FastAPI et respecte une architecture **modulaire inspirée du 3-tier** :

### `main.py`
Point d’entrée de l’application. Il instancie l’application FastAPI, inclut les routes et configure les middlewares (dont Prometheus).

### `routers/commande_orchestration.py`
Expose les endpoints HTTP `/api/commande` :
- `POST /checkout` : lance la saga orchestrée
- `GET /{id}` : récupère l’état courant d’une commande
Il délègue la logique métier au module `services`.

### `services/saga_checkout.py`
Contient la logique de la saga orchestrée :
- Coordination séquentielle des appels (panier → stock → client → ventes)
- Gestion des erreurs et compensation
- Logging des transitions d’état (`log_etat`)
- Incrément des métriques Prometheus

### `services/etat_commande.py`
Contient la fonction `changer_etat_commande`, qui :
- Met à jour la commande (`etat_actuel`)
- Enregistre la transition dans `EtatSaga`
- Incrémente la métrique associée

### `models/commande.py`, `etat_saga.py`, `etat_commande_enum.py`
Définissent :
- Le modèle `Commande` (UUID, client_id, magasin_id, état)
- Le modèle `EtatSaga` (historique de transitions)
- L’énumération `EtatCommande`

### `schemas.py`
Contient le schéma `CommandeInput` utilisé pour recevoir les requêtes utilisateur.

### `metrics.py`
Expose `commande_etat_total` : compteur Prometheus par état de commande.

## 7.2 Bases de données

Le service utilise deux tables dans PostgreSQL :
- `commandes` : stocke l’état courant
- `etat_saga` : trace l’historique des transitions (avec timestamp)

## 7.3 Diagramme de composants

![alt text](image-4.png)
# 8. Vue comportementale

Cette section illustre le **comportement dynamique** du microservice `orchestrateur-service` à travers des diagrammes de séquence. Ces diagrammes modélisent l’enchaînement des appels lors du traitement d’une commande, ainsi que les alternatives en cas d’échec.

## 8.1 Scénario nominal – Traitement complet d’une commande

Ce scénario illustre le chemin heureux (happy path) dans lequel :
1. Le panier est récupéré,
2. Le stock est réservé,
3. Le client est débité,
4. La vente est enregistrée avec succès.

Chaque étape produit une transition de la machine d’état (`EtatCommande`) et est journalisée dans `EtatSaga`.



## 8.2 Scénario d’échec – Stock insuffisant

Si le `stock-service` échoue à réserver les produits (ex. stock insuffisant), alors :
- La saga est arrêtée,
- Aucun paiement n’est effectué,
- Le `EtatCommande` passe à `ECHEC_STOCK`,
- Une entrée est enregistrée dans `EtatSaga`.


## 8.3 Scénario d’échec – Paiement refusé

Si le paiement échoue :
- Le stock est libéré (rollback),
- Le client n’est pas facturé,
- L’état passe à `ECHEC_PAIEMENT`.



## 8.4 Scénario d’échec – Enregistrement de la vente échoué

En cas d’échec lors de l’appel au `ventes-service` :
- Le paiement est remboursé,
- Le stock est libéré,
- L’état final devient `ECHEC_ENREGISTREMENT`.



---

Chaque scénario valide le bon fonctionnement de la **compensation transactionnelle**, assurant la cohérence globale malgré les pannes partielles.


# 9. Vue de développement

Cette vue documente la **structure interne** du microservice `orchestrateur-service` en termes de fichiers, modules et dépendances logicielles. Elle reflète l’organisation des dossiers du code, l’architecture logique de FastAPI, et les responsabilités attribuées à chaque couche.

Le projet suit une architecture claire en plusieurs couches :
- `routers/` : Définition des routes exposées (ex: `/api/commande`)
- `services/` : Logique métier (orchestration, changement d’état)
- `models/` : Modèles SQLAlchemy liés à la base de données (`Commande`, `EtatSaga`)
- `schemas/` : Objets de validation Pydantic pour les entrées et sorties API
- `db/` : Configuration de la base de données (session, moteur)
- `metrics.py` : Instrumentation Prometheus
- `main.py` : Point d’entrée de l’application FastAPI

Cette séparation respecte les bonnes pratiques SOLID, facilite les tests unitaires, et rend les responsabilités explicites.
![alt text](image-5.png)


## 9.2 Décisions architecturales (ADR)

###  ADR #1 – Adoption d’une orchestration centralisée pour la gestion des commandes (Saga)

##  Contexte

Dans le cadre du Laboratoire 6 du cours LOG430 (Été 2025), nous devions gérer une transaction répartie sur plusieurs microservices (panier, stock, client, ventes) de manière fiable, avec rollback en cas d’échec. Deux approches étaient envisageables : **orchestration centralisée** ou **chorégraphie distribuée**.

## Décision

Nous avons choisi de centraliser la coordination dans un microservice dédié, appelé `orchestrateur-service`, qui implémente une **saga orchestrée synchrone**.

##  Conséquences

- Un seul point de décision contrôle l’ordre et les transitions de la saga.
- L’**état de la commande** est maintenu dans une machine d’état persistée (`etat_actuel` dans `Commande` + historique dans `EtatSaga`).
- Le service `orchestrateur-service` gère les appels HTTP interservices, les erreurs, et les actions compensatoires (rollback).
- Chaque état est instrumenté avec des métriques Prometheus (`commande_etat_total`), facilitant le suivi.

## Alternatives envisagées

- **Chorégraphie distribuée** : chaque service déclenche l’étape suivante via des événements asynchrones.
  - Avantage : découplage maximal
  - Inconvénient : complexité accrue, difficile à suivre et tester
  - Nécessite un bus de messages (RabbitMQ, Kafka)

##  Justification

- Nous voulions maximiser la clarté, la testabilité et la traçabilité des transitions.
- Le style synchrone et impératif de l’orchestration est mieux adapté pour un laboratoire avec contraintes de temps, sans infra Kafka.
- Permet d’ajouter facilement des métriques, des logs, et des tests de bout en bout.

## 🛠️ Implémentation

- `orchestrateur-service` implémente la logique complète de la saga.
- La progression est journalisée dans `EtatSaga`, et l’état courant dans `Commande`.
- Le tout est exposé via des endpoints REST (`/checkout`, `/commande/{id}`).

---

### ADR #2 – Gestion explicite des états de commande via machine d’état persistée

##  Contexte

Dans une saga orchestrée répartie sur plusieurs microservices, le suivi de l’évolution de l’état de la commande est **critique** pour la cohérence du système. Il est impératif de pouvoir savoir :

- où la commande se trouve dans le processus (stock, paiement, vente…),
- si un échec est survenu et à quelle étape,
- comment effectuer un rollback ou déclencher une action compensatoire.

##  Décision

Nous avons mis en place une **machine d’état explicite et persistée**, pilotée par l’orchestrateur. Deux structures sont utilisées pour assurer cette gestion :

1. Un **enum** `EtatCommande` définit tous les états possibles de la commande (initiation, validation, échecs, confirmation).
2. Une **table Commande** contient un champ `etat_actuel` mis à jour à chaque transition.
3. Une **table EtatSaga** conserve l’historique complet des transitions (`saga_id`, `état`, `timestamp`).

Chaque transition est aussi **instrumentée avec Prometheus** pour permettre le monitoring temps réel de la répartition des commandes par état.

##  Conséquences

-  **Clarté** : chaque état est nommé explicitement et visible via un endpoint `/api/commande/{id}`.
-  **Testabilité** : permet de valider des cas d’échec (stock/paiement) en suivant l’évolution des états.
-  **Observabilité** : les métriques permettent d’observer le taux d’échecs ou de confirmations dans Grafana.
-  **Persistance** : même après redémarrage, l’historique et l’état sont disponibles.

##  Implémentation

- La fonction `changer_etat_commande(...)` :
  - met à jour la table `Commande` avec l’état courant,
  - insère un enregistrement dans `EtatSaga`,
  - incrémente le compteur Prometheus `commande_etat_total{etat="..."}`
- Le service `saga_checkout.py` appelle cette fonction après chaque étape réussie ou échouée.

##  Alternatives considérées

-  **Gestion en mémoire** :
  - plus rapide, mais perdue au redémarrage,
  - difficile à tester en environnement distribué.
-  **État implicite dans les logs ou files d’attente** :
  - difficile à tracer,
  - nécessite un moteur externe de corrélation.

##  Justification

- Ce choix répond à des objectifs pédagogiques :
  - mettre en œuvre les **principes DDD (état explicite, persisté)**,
  - intégrer **l’observabilité** comme exigence non fonctionnelle (Prometheus, Grafana),
  - permettre une **analyse post-mortem** des commandes échouées.

---



# 10. Vue de déploiement

Le microservice `orchestrateur-service` est déployé dans un environnement **dockerisé**, au sein d’un système distribué basé sur Docker Compose. Chaque microservice est conteneurisé de manière isolée, et les communications interservices se font via HTTP sur un réseau Docker commun (`backend`).

L’architecture de déploiement est composée des éléments suivants :

- **Frontend React** : application web accessible via le navigateur, consommant les API exposées.
- **KrakenD** (API Gateway) : unique point d’entrée pour les appels API, répartissant les requêtes vers les services internes.
- **NGINX Load Balancer** : équilibre la charge entre plusieurs instances de `stock-service`.
- **Microservices FastAPI** :
  - `orchestrateur-service` (coordination de la saga)
  - `panier-service` (panier du client)
  - `stock-service-1` et `stock-service-2` (réservation/libération)
  - `client-service` (paiement/remboursement)
  - `ventes-service` (enregistrement)
  - `produits-service`, `magasin-service`, etc.
- **Bases de données PostgreSQL** : une base par microservice (sauf pour `stock-service` partagé entre instances).
- **Prometheus & Grafana** : outils d’observabilité, intégrés dans un réseau `observability`.

Chaque service expose son port interne (souvent `:8000`) dans son conteneur, mais seul le frontend, la gateway et les outils de monitoring sont exposés à l’extérieur.

Cette configuration favorise la résilience, la montée en charge et la surveillance précise du système.


### 10.3 Capture Grafana – Observabilité des états de commande

Le tableau de bord Grafana suivant illustre l’activité de l’orchestrateur dans le temps. Il permet de visualiser :

- Les **points d'entrée (`handler`) sollicités** dans le service (ex. `/api/panier`, `/api/stock/reserver`, `/api/clients`, etc.).
- Le nombre d’appels **par type de requête**, ce qui aide à surveiller la fréquence et la distribution des appels lors des tests ou de la production.
- La **courbe de l’état des commandes** (`commande_etat_total`) visible en bas, qui reflète :
  - le bon enchaînement des transitions vers des états comme `STOCK_RESERVE`, `PAIEMENT_EFFECTUE`, `CONFIRMEE`,
  - la détection des anomalies ou échecs (comme `ECHEC_STOCK`, `ECHEC_PAIEMENT`, etc.).

Cette vue est essentielle pour diagnostiquer les comportements inattendus, vérifier la robustesse de la saga, détecter des goulets d’étranglement, et confirmer que le système applique correctement les logiques de rollback ou de réussite.

![alt text](image-9.png)


# 11. Vue des cas d’utilisation

Le système distribué multi-magasins vise à couvrir les besoins des **clients** (parcours de commande) et des **employés** (gestion des produits, magasins, stocks, ventes). Cette section décrit les principales interactions utilisateur-système en termes de cas d'utilisation, indépendamment de l’implémentation technique.

## 11.1 Acteurs

- **Client** : navigue sur l’interface web, consulte les produits, gère son panier et effectue des commandes.
- **Employé** : administre le catalogue, les magasins, les stocks et consulte les rapports de vente.

## 11.2 Cas d’utilisation principaux

### Pour l’employé :
- Ajouter, modifier et consulter les produits
- Créer et lister les magasins
- Mettre à jour les niveaux de stock
- Générer des rapports de rupture et surstock

### Pour le client :
- Créer un compte client
- Gérer son panier (ajouter, supprimer des articles)
- Valider sa commande (checkout via saga orchestrée)

Le processus de **validation de commande (checkout)** est le cas d’utilisation le plus critique : il active la saga distribuée à travers plusieurs microservices, avec gestion d’échec et rollback.

---


![alt text](image-6.png)


# 12. Vue logique

La vue logique présente les principales entités du système et leurs relations dans le domaine de la gestion des commandes orchestrées. Elle reflète les classes et structures utilisées dans le microservice `orchestrateur-service` ainsi que leurs interactions avec les autres services via appels HTTP.

## 12.1 Entités principales

- **Commande** : entité centrale représentant une commande client. Identifiée par un `UUID`, elle contient l'identifiant du client, celui du magasin et son `état_actuel`, qui évolue au fil de la saga.
- **EtatCommande (Enum)** : définit les états possibles d’une commande (INITIÉE, STOCK_RÉSERVÉ, PAIEMENT_EFFECTUÉ, etc.). Utilisé comme machine d’état explicite.
- **EtatSaga** : enregistre l’historique de tous les changements d’état d’une commande. Permet la traçabilité fine du processus.
- **CommandeInput (schema Pydantic)** : objet d’entrée reçu lors d’une commande (checkout). Contient `client_id` et `magasin_id`.

## 12.2 Relations

- Une **Commande** possède un et un seul `etat_actuel`, et peut générer plusieurs entrées dans **EtatSaga** au fil de son évolution.
- La structure `EtatCommande` permet de suivre les transitions métier et de produire des métriques par état.
- `CommandeInput` est utilisée uniquement pour encapsuler les données entrantes de l'utilisateur avant orchestration.

## 12.3 Diagramme de classes

Le diagramme ci-dessous illustre les principales entités manipulées dans le service d’orchestration et leur structure interne.

---

![alt text](image-7.png)

# 13. Vue de développement

La vue de développement décrit l'organisation interne du code source du microservice `orchestrateur-service`, en mettant en évidence les principaux composants (fichiers, modules, packages) et leurs responsabilités. Cette vue est essentielle pour comprendre la structure logicielle et les points d’entrée de l’implémentation.

## 13.1 Organisation modulaire

Le service suit une architecture modulaire inspirée de l’architecture hexagonale (ports/adaptateurs) avec les composants suivants :

- **`main.py`** : point d’entrée de l’application FastAPI. Monte le routeur principal.
- **`routers/commande_orchestration.py`** : contient les endpoints REST exposés (`/checkout`, `/commande/{id}`).
- **`services/saga_checkout.py`** : implémente la logique métier de la saga orchestrée : coordination des appels interservices, gestion des états, déclenchement des rollbacks.
- **`services/etat_commande.py`** : gère les transitions d’état : mise à jour de la base, ajout au journal historique, incrémentation des métriques Prometheus.
- **`models/commande.py`** : classe SQLAlchemy représentant la commande (UUID, client, magasin, état).
- **`models/etat_saga.py`** : journalisation des transitions sous forme de tuples `(saga_id, état, timestamp)`.
- **`models/etat_commande_enum.py`** : énumération de tous les états possibles (de `INITIÉE` à `ANNULÉE`).
- **`schemas.py`** : modèles Pydantic (entrée utilisateur) pour valider les données entrantes.
- **`metrics.py`** : définition des compteurs Prometheus (`commande_etat_total`) pour l’observabilité.
- **`db/database.py`** : gestion de la connexion SQLAlchemy et création de sessions vers PostgreSQL.

## 13.2 Couplage et responsabilités

- Le `router` appelle le service `saga_checkout` qui orchestre toute la logique métier.
- La persistance est gérée dans `etat_commande.py` qui agit comme adaptateur entre logique et stockage.
- Tous les composants métiers (modèles, enums, services) sont découplés et testables individuellement.


