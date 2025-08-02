## 1. Introduction

Ce rapport présente l'évolution d'une application de gestion de commandes multi-magasins vers une architecture distribuée fondée sur les événements. Ce travail s'inscrit dans le cadre du Laboratoire 7 du cours LOG430 – Architecture logicielle (Été 2025) à l'ÉTS.

Après avoir introduit des microservices avec orchestrateur (Lab 6), cette itération vise à remplacer le contrôle centralisé par une coordination asynchrone entre services à l’aide :
- d’un système de messagerie de type Pub/Sub (Redis Streams),
- d’un Event Store persistant,
- de vues séparées de lecture/écriture (CQRS),
- et d’une saga chorégraphiée pour la gestion des transactions distribuées.

L’approche événementielle adoptée permet une meilleure résilience, un découplage fort entre services, une auditabilité complète via les événements, et une meilleure extensibilité fonctionnelle.


## 2. Scénario métier retenu

Le scénario métier choisi pour ce laboratoire repose sur un processus central du domaine e-commerce : le traitement d’une commande client à partir d’un panier multi-produits, dans un système multi-magasins. Ce processus distribué implique plusieurs microservices, chacun responsable d’un sous-domaine métier. Le client ajoute d’abord des produits à son panier, puis soumet une commande. Cette action déclenche une série d’interactions asynchrones entre services.

Concrètement, lorsqu’un client valide son panier, le `panier-service` publie un événement métier de type `CommandeCreee` sur un canal Redis Streams. Cet événement déclenche alors une réaction en chaîne, sans coordination centralisée : le `stock-service` tente de réserver les quantités demandées pour chaque produit. Si les quantités sont suffisantes, il publie à son tour un événement `StockReserve`. Dans le cas contraire, il publie `StockIndisponible`, ce qui met fin prématurément à la transaction.

Si le stock a été correctement réservé, le `client-service` est notifié et procède au débit du montant total de la commande. En cas de solde suffisant, il émet l’événement `PaiementAccepte`. Sinon, l’événement `PaiementRefuse` est publié, déclenchant des actions de compensation (libération du stock réservé). Finalement, si le paiement est accepté, le `ventes-service` enregistre la vente et publie l’événement `VenteConfirmee`.

Chacune de ces étapes repose sur un mécanisme Pub/Sub assurant un fort découplage. Aucun service ne connaît les services abonnés, ni n’attend de réponse directe. Cette architecture permet une grande souplesse pour ajouter de nouveaux consommateurs (audit, notification, supervision) sans modifier la logique métier existante. Tous les événements sont parallèlement persistés dans un `event-store`, ce qui permet leur relecture, la reconstruction d’état à partir de projections, et une auditabilité complète.

Ce scénario, bien que simple dans son déroulement, permet de démontrer la combinaison efficace de plusieurs concepts d’architecture logicielle moderne : la communication événementielle, l’Event Sourcing, la séparation des responsabilités (CQRS), et la coordination décentralisée des transactions (saga chorégraphiée).


## 3. Architecture événementielle globale

L’architecture du système repose désormais sur un modèle événementiel distribué, fondé sur la publication et la consommation d’événements métier à travers un bus de messages implémenté avec Redis Streams. Chaque microservice émet ses propres événements en réponse à une action métier locale (par exemple : création de commande, réservation de stock, acceptation de paiement), tout en s’abonnant à certains événements produits par d’autres services.

Ce modèle suit le paradigme Pub/Sub : les producteurs n’ont pas connaissance des consommateurs, ce qui permet un couplage très faible entre services. Ainsi, il est possible d’ajouter ou de retirer des consommateurs (ex. audit, notification) sans modifier la logique des producteurs. Cette souplesse est l’un des avantages majeurs d’une architecture fondée sur les événements.

Les événements sont sérialisés en JSON, enrichis de métadonnées (horodatage, type, ID d’agrégat, source), puis publiés dans des **streams Redis** nommés de façon explicite (`commande.evenements`, `paiement.evenements`, etc.). Les microservices consomment ces événements via des **groupes de consommateurs**, assurant ainsi une gestion de la concurrence, des redéliveries et une répartition du traitement.

En complément de la propagation des événements, un composant `event-store` a été introduit pour assurer une **persistance durable** de tous les événements métiers. Il stocke chaque événement dans une base PostgreSQL, avec un endpoint permettant leur relecture et leur projection. Ce mécanisme d’**Event Sourcing** permet de reconstruire l’état courant d’un agrégat (commande, panier, etc.) à tout moment, en rejouant les événements le concernant.

Certains services adoptent en plus le modèle **CQRS** : ils séparent leurs opérations de lecture (projection, consultation) des opérations d’écriture (commande, émission d’événement). Cela permet de disposer de modèles de lecture optimisés, par exemple des vues indexées ou matérialisées, tout en conservant une logique métier pure dans la partie écriture.

La communication inter-service est donc asynchrone, orientée événement, persistante et extensible. L’infrastructure technique repose sur Docker Compose, avec Prometheus pour l’observabilité, Grafana pour la visualisation des métriques, et un système de monitoring qui expose des compteurs Prometheus au niveau de chaque service.

![alt text](image.png)

## 4. Diagramme de séquence – Saga chorégraphiée

La coordination de la commande ne repose plus sur un orchestrateur central (comme dans le laboratoire précédent), mais sur une **saga chorégraphiée**. Dans ce modèle, chaque microservice réagit à des événements, déclenche des actions locales, puis publie à son tour un nouvel événement. Ainsi, l’état de la commande progresse de manière distribuée, chaque service étant responsable de sa propre logique de traitement et de compensation.

Le processus est initialisé par le `panier-service`, qui publie un événement `CommandeCreee` lorsque le client valide son panier. Cet événement est consommé par le `stock-service`, qui tente de réserver les produits nécessaires. Si le stock est suffisant, il émet un événement `StockReserve`, permettant au `client-service` de procéder au paiement. Si le solde du client est adéquat, ce dernier publie `PaiementAccepte`, ce qui permet au `ventes-service` d’enregistrer la vente et de clôturer la transaction.

À tout moment, un service peut constater un échec (stock insuffisant, solde insuffisant) et publier un événement d’échec (`StockIndisponible`, `PaiementRefuse`). Les services ayant déjà effectué des actions peuvent alors effectuer des **compensations locales** : libération de stock, remboursement du client, annulation de vente.

Ce modèle de coordination par événements rend le système plus résilient aux pannes partielles, plus flexible à étendre, et plus simple à monitorer via les événements émis.

![alt text](image-1.png)

## 4.1 Contexte et cas d'utilisation

Le système multi-magasins repose sur des interactions entre plusieurs acteurs (employé, client, observateur Prometheus) et des cas d’utilisation métiers variés : gestion de produits, de stock, de clients, de ventes, et coordination de commandes via une saga.

Le diagramme ci-dessous présente le contexte d’utilisation général du système, avec les cas d’usage associés.

![alt text](image-4.png)

Voici une vue détaillée des cas d’utilisation, regroupés par domaine fonctionnel. On y retrouve la validation de commande, les mises à jour de stock, la création de clients et la gestion de la saga.

![alt text](image-5.png)


## 5. ADR 1 – Choix de Redis Streams comme système de messagerie Pub/Sub

### Contexte

Dans le cadre du Laboratoire 7, le projet devait implémenter une communication événementielle entre microservices à l’aide d’un système de messagerie. Plusieurs options étaient possibles, notamment Kafka, RabbitMQ, NATS, ou Redis Streams. Il était crucial de choisir une solution compatible avec Docker Compose, légère à déployer, et suffisamment puissante pour supporter les schémas de type Pub/Sub avec gestion des groupes de consommateurs.

### Décision

Nous avons décidé d’utiliser **Redis Streams** comme mécanisme principal de communication Pub/Sub entre microservices.

### Raisons

- **Simplicité d’intégration** : Redis est déjà bien supporté dans l’écosystème Python/FastAPI, et son usage ne nécessite pas de configuration complexe.
- **Support natif des streams** : Redis Streams fournit un modèle d’append-only log avec gestion des groupes de consommateurs (`XGROUP`), accusés de réception (`XACK`), reprise (`XREADGROUP`), etc.
- **Légèreté et rapidité de déploiement** : Redis fonctionne très bien dans Docker, sans overhead majeur, contrairement à Kafka ou RabbitMQ qui nécessitent souvent plusieurs conteneurs pour fonctionner.
- **Performance raisonnable** : Redis Streams est adapté aux charges événementielles modérées, suffisantes pour un système académique ou de taille moyenne.
- **Support asynchrone** : La bibliothèque `redis.asyncio` permet une consommation non-bloquante efficace dans un contexte `async def`.

### Alternatives considérées

- **Apache Kafka** : bien plus robuste et adapté aux systèmes à grande échelle, mais très lourd à configurer dans un environnement local sans Confluent Platform. Idéal en production, mais surdimensionné ici.
- **RabbitMQ** : très populaire pour les cas d’usage métier classiques, mais nécessite un serveur AMQP dédié et une configuration spécifique pour les retries et dead-letter queues.
- **NATS / MQTT** : très performants, mais moins documentés dans l’écosystème FastAPI + SQL, et plus orientés IoT/messaging pur.

### Conséquences

- La solution est adaptée au contexte pédagogique et au besoin de coordination événementielle du système.
- Les microservices peuvent échanger des événements de manière fiable, rejouer des messages, ou les distribuer à plusieurs consommateurs sans se connaître.
- En cas d’évolution vers un usage à grande échelle, une migration vers Kafka serait envisageable, Redis servant alors de prototype fonctionnel.

### Statut

**Acceptée – implémentée dans tous les services à travers Redis Streams**


---

## 5.1 Vue de développement

Chaque microservice suit une structure modulaire basée sur FastAPI. Le diagramme ci-dessous montre l’organisation interne typique d’un microservice (`main.py`, routers, services, modèles, etc.).

![alt text](image-6.png)

Le diagramme suivant représente les **dépendances entre microservices**. Chaque service communique avec d’autres via appels HTTP ou événements Redis. Cette vue permet de comprendre les liens techniques entre services.

![alt text](image-7.png)

---

## 5.2 Vue des processus

La vue processus permet de visualiser le déroulement des scénarios métiers clés (succès, rollback, transitions d'état). Voici les principaux diagrammes associés :

### a) Validation de commande (checkout)

![alt text](image-8.png)

Ce diagramme montre le flux asynchrone entre les services `panier`, `stock`, `client` et `vente`, lors de la création d’une commande.

### b) Échec de paiement (rollback)

![alt text](image-9.png)

Ce diagramme illustre la compensation en cas de paiement refusé (libération du stock, arrêt de la vente).

### c) Machine d'état de la saga

![alt text](image-10.png)

Ce diagramme décrit les différents états d’une commande dans le cadre de la saga chorégraphiée (`en_attente_stock`, `stock_reserve`, `paiement_refuse`, etc.).

---
## 5.3 Vue de déploiement

Le système repose sur une infrastructure Docker avec plusieurs conteneurs : microservices FastAPI, bases PostgreSQL, Redis, Prometheus, Grafana et Krakend. La vue suivante montre le déploiement global des composants.

![alt text](image-11.png)

## 6. ADR 2 – Implémentation de l’Event Store avec PostgreSQL

### Contexte

Dans le cadre de l’approche Event Sourcing, il était nécessaire d’implémenter un composant `event-store` capable de stocker durablement tous les événements métier produits par les différents microservices. Ce composant devait également permettre la relecture des événements (replay), ainsi que la reconstruction de l’état courant d’un agrégat métier via une projection.

Il était donc impératif de choisir une solution de stockage persistant, fiable, interrogeable, et facilement intégrable avec les outils de l’écosystème Python/FastAPI.

### Décision

Nous avons choisi d’utiliser **PostgreSQL** comme base de données pour implémenter l’Event Store, avec une API FastAPI exposant des endpoints REST pour l’écriture et la lecture des événements.

### Raisons

- **Fiabilité et robustesse** : PostgreSQL est une base ACID largement éprouvée, adaptée au stockage de données séquentielles et historisées.
- **Requêtabilité** : Les événements étant stockés sous forme de lignes JSON, il est facile d’effectuer des projections ou des filtres via des requêtes SQL.
- **Intégration rapide** : PostgreSQL est déjà utilisé dans d'autres microservices du système, ce qui simplifie son déploiement avec Docker.
- **Pas de dépendance à des outils tiers** : Contrairement à Kafka (avec sa propre rétention de log) ou à MongoDB (nécessitant un modèle de document), PostgreSQL reste simple à configurer et documenté dans le contexte FastAPI + SQLAlchemy.
- **Contrôle sur la structure** : Le schéma des événements inclut des champs typés (type, source, timestamp, agrégat, données JSON), ce qui permet d’assurer une structure cohérente dans l’ensemble du système.


## 6.1 Structure technique – Event Store

Le microservice `event-store` joue un rôle clé dans l’approche Event Sourcing. Il stocke tous les événements métiers dans PostgreSQL, permet leur relecture et reconstruit l’état projeté d’un agrégat via `/projections/{id}`.

Le diagramme ci-dessous illustre l’architecture interne de ce microservice.

![alt text](image-12.png)
---

## 6.2 Vue logique (bonus)

Une vue logique complémentaire permet de visualiser les **classes métiers** du domaine (Commande, Produit, Client, etc.) et leurs attributs. Elle aide à mieux comprendre la structure sémantique des objets manipulés dans les événements.

![alt text](image-13.png)

### Alternatives considérées

- **Apache Kafka comme Event Store** : possible via les logs Kafka, mais nécessite un connecteur et une infrastructure plus lourde pour la persistance longue durée.
- **MongoDB** : adapté aux documents JSON, mais moins robuste pour les projections complexes ou les relations fortes.
- **Fichiers plats (JSONLines)** : simple mais non scalable, non interrogeable facilement, et peu résilient.

### Conséquences

- Tous les événements métier (commande, stock, paiement, vente) sont persistés avec horodatage, source et ID d’agrégat.
- Un endpoint `/events/` permet l’écriture via POST, tandis que `/projections/{aggregate_id}` permet de reconstruire un état projeté à la volée.
- Il est possible de rejouer les événements pour un agrégat, d’enrichir les projections, ou d’exporter les événements à des fins d’analyse.
- En cas d’évolution du projet, une migration vers Kafka ou EventStoreDB serait envisageable avec adaptation minimale.

### Statut

**Acceptée – Implémentée dans le microservice event-store**


## 7. Event Sourcing et Projections

L’architecture événementielle mise en place repose sur un principe fondamental : chaque changement d’état métier est représenté par un événement immuable, enregistré dans un journal d’événements (Event Store). Plutôt que de stocker uniquement l’état courant d’un objet métier (par exemple une commande ou un panier), le système conserve toute la séquence des événements qui ont mené à cet état.

Chaque événement est encodé en JSON, enrichi de métadonnées structurées (type, source, timestamp, ID d’agrégat), puis stocké dans une table relationnelle PostgreSQL. Ce mécanisme d’**Event Sourcing** offre plusieurs avantages : auditabilité, traçabilité complète, possibilité de rejouer le passé, et reconstruction dynamique de l’état.

Le microservice `event-store` expose deux endpoints REST :

- `POST /events/` : permet de persister un événement métier via un schéma structuré `EvenementIn`. Ce endpoint est invoqué par les producteurs d’événements, notamment dans le cadre de la saga chorégraphiée (commande, paiement, vente).
- `GET /events/projections/{aggregate_id}` : permet de rejouer tous les événements associés à un agrégat donné et de reconstruire son état courant.

La logique de projection repose sur un service `reconstruire_etat(aggregate_id)`, qui récupère les événements dans l’ordre chronologique et les applique à une structure Python (dictionnaire mutable représentant l’état agrégé). Ce mécanisme de **read model reconstruit à la volée** permet de générer des représentations légères, cohérentes et vérifiables sans créer de nouvelle base de données dédiée.

Par exemple, pour une commande identifiée par `cmd-1234`, le replay d’événements tels que `CommandeCreee`, `StockReserve`, `PaiementAccepte` et `VenteConfirmee` permet de générer un état final contenant tous les produits commandés, le client associé, le statut, le montant total, et l’issue de la transaction.

Ce mécanisme offre ainsi une **vue temporelle explicite** de chaque transaction métier, ce qui est particulièrement utile en contexte distribué où l’état est disséminé entre plusieurs microservices. En cas d’erreur, il est également possible de comparer la projection avec les journaux ou de rejouer une séquence d’événements pour diagnostiquer un comportement inattendu.

## 8. Séparation CQRS (Command Query Responsibility Segregation)

Dans l’architecture mise en place, le modèle CQRS est appliqué de manière ciblée pour séparer les responsabilités de modification d’état (commandes) et de consultation (requêtes). Cette séparation s’appuie sur le fait que les besoins techniques, fonctionnels et de performance sont très différents selon qu’un service manipule une commande ou interroge un état projeté.

Les commandes sont gérées de manière classique via des endpoints REST exposés par les microservices métiers (`POST /checkout`, `POST /paiement`, etc.). Ces commandes déclenchent des événements métier (`CommandeCreee`, `PaiementAccepte`, `VenteConfirmee`) qui sont publiés sur le bus Redis Streams. Ces événements sont ensuite stockés de manière persistante dans l’Event Store.

La lecture, quant à elle, s’appuie sur des **vues projetées** construites à partir de la relecture des événements. Le microservice `event-store` fournit ainsi un point d’entrée de type `GET /projections/{aggregate_id}`, qui permet de reconstruire à la volée l’état d’un agrégat (commande, panier, etc.) sans requêter directement les bases métiers des microservices producteurs.

Cette séparation permet plusieurs bénéfices concrets :
- **Performance** : les lectures sont simplifiées, centralisées, et ne nécessitent pas d’agréger dynamiquement les réponses de plusieurs services.
- **Résilience** : même en cas de panne d’un service métier (ex. `ventes-service`), l’état d’une commande peut être reconstitué de manière autonome à partir des événements enregistrés.
- **Auditabilité** : les vues projetées sont dérivées d’événements immuables, ce qui assure leur cohérence et permet une vérification facile en cas de litige ou d’incident.

Dans une version étendue, ces vues pourraient être matérialisées dans une base dédiée, ou optimisées pour la recherche (indexation, cache Redis, etc.). Toutefois, dans ce laboratoire, la projection à la volée s’est révélée suffisante et efficace pour démontrer le modèle CQRS, tout en limitant la complexité technique.


## 9. Observabilité

L’un des enjeux critiques d’une architecture distribuée fondée sur les événements est la capacité à comprendre, diagnostiquer et superviser le comportement global du système. Pour cela, l’observabilité a été intégrée de manière systématique dans chaque microservice, à l’aide de **Prometheus** pour la collecte des métriques, et **Grafana** pour la visualisation et l’analyse.

Chaque microservice expose un endpoint `/metrics`, instrumenté via la bibliothèque `prometheus_fastapi_instrumentator`. Ce middleware collecte des données techniques (latence, nombre de requêtes, erreurs HTTP) ainsi que des **métriques métiers personnalisées** spécifiques au scénario événementiel. Par exemple :

- `event_store_events_total{event_type="CommandeCreee", source="panier-service"}`  
  → Compte le nombre d’événements persistés par type et par origine.
- `commande_etat_total{etat="PaiementRefuse"}`  
  → Suit la répartition des commandes par état dans la machine à états distribuée.
- `saga_commande_succes_total` / `saga_commande_echec_total`  
  → Compte les sagas réussies vs échouées.
- `commande_latence_ms`  
  → Histogramme de latence entre l’émission et la consommation d’un événement.

Ces métriques sont récupérées par Prometheus à intervalle régulier, puis affichées dans plusieurs **dashboards Grafana** configurés pour ce laboratoire. Deux types de tableaux de bord ont été conçus :

- **Dashboard général d'activité** : flux d’événements, nombre total d’événements par service, latence moyenne, volume par topic Redis.
![alt text](image-2.png)
- **Dashboard saga** : suivi détaillé des commandes en cours, taux de succès/échec des transactions, métriques d’échec par service impliqué (stock, paiement, vente).
![alt text](image-3.png)

Ces tableaux offrent une visibilité complète sur le comportement du système en production, et permettent d’identifier rapidement les goulets d’étranglement, erreurs systématiques, ou instabilités.


## 10. Tests et Résilience

Pour valider le bon fonctionnement de l’architecture événementielle et de la coordination distribuée, plusieurs scénarios de tests ont été mis en place, incluant des cas de succès et d’échecs partiels. Ces tests ont permis de vérifier à la fois la robustesse de la saga chorégraphiée et la réactivité des services à différents événements.

### Scénario de succès

Un test de bout en bout a été réalisé à l’aide de Postman ou via appel direct HTTP :
1. Un client ajoute plusieurs produits à son panier (`panier-service`).
2. Il valide la commande, ce qui publie un événement `CommandeCreee`.
3. Le `stock-service` réserve les produits → `StockReserve`.
4. Le `client-service` valide le paiement → `PaiementAccepte`.
5. Le `ventes-service` enregistre la vente → `VenteConfirmee`.

La relecture de la commande via `/projections/{aggregate_id}` confirme la bonne propagation des événements et l’état final `VenteConfirmee`.

### Scénarios d’échecs simulés

Des cas d’échec volontaire ont été introduits pour tester la **compensation** :
- **Stock insuffisant** : si la quantité en stock est inférieure à la demande, un événement `StockIndisponible` est publié. Aucun paiement n’est déclenché, et la commande reste incomplète.
- **Solde client insuffisant** : un montant volontairement insuffisant a été défini pour le client. Le `client-service` publie alors `PaiementRefuse`, ce qui déclenche une **libération du stock** via un événement compensatoire.
- **Interruption réseau ou plantage d’un service** : en arrêtant manuellement un conteneur Docker (`ventes-service`), le reste de la chaîne continue de fonctionner. La résilience est assurée par le fait que l’événement reste disponible dans Redis jusqu’à sa consommation.

### Résultats

Les tests ont confirmé :
- L’indépendance des services grâce au modèle Pub/Sub.
- La possibilité de traiter des commandes en parallèle sans conflits.
- La robustesse du système en cas d’erreur, avec compensation adéquate.
- La traçabilité complète via les événements stockés et les métriques exposées.

## 11. Échantillons d’événements, logs et projections

Afin d’illustrer le comportement de l’architecture événementielle et de la saga chorégraphiée, plusieurs extraits ont été collectés durant les tests. Ces données montrent à la fois le contenu des événements publiés, la manière dont les logs structurés sont générés par les microservices, et le résultat des projections depuis l’Event Store.

### 📌 Événement métier – `CommandeCreee`

```json
{
  "event_type": "CommandeCreee",
  "aggregate_id": "cmd-1234",
  "timestamp": "2025-08-01T15:42:17.123Z",
  "source": "panier-service",
  "data": {
    "client_id": 42,
    "produits": [
      { "produit_id": 1, "quantite": 2, "sous_total": 10.0 },
      { "produit_id": 5, "quantite": 1, "sous_total": 5.0 }
    ],
    "total": 15.0
  }
}
```

### 📌 Log structuré – Réservation de stock réussie

```log
[stock-service] Stock réservé pour commande cmd-1234
Événement publié : StockReserve
Détails : {"produits": [...], "total": 15.0, "client_id": 42}
```

### 📌 Log structuré – Paiement refusé et compensation

```log
[client-service] Paiement refusé pour client 42, montant : 15.0
Événement publié : PaiementRefuse
[stock-service] Stock libéré pour commande cmd-1234 suite à échec de paiement
```

### 📌 Projection d’une commande (`/events/projections/cmd-1234`)

```json
{
  "client_id": 42,
  "produits": [
    { "produit_id": 1, "quantite": 2, "sous_total": 10.0 },
    { "produit_id": 5, "quantite": 1, "sous_total": 5.0 }
  ],
  "total": 15.0,
  "statut": "PaiementRefuse"
}
```

### 📌 Résilience constatée

Même en cas d’interruption temporaire du `ventes-service`, la commande reste dans un état cohérent. Dès redémarrage du service, les événements en attente sont consommés (`xreadgroup` Redis), garantissant **l’exact-once processing** grâce à l’acknowledgement (`XACK`).

Ces extraits démontrent que chaque service produit des logs exploitables, que les événements sont structurés et traçables, et que l’état métier peut être reconstitué de manière fiable.

## 12. Conclusion critique

Ce laboratoire a permis de faire évoluer une architecture de microservices vers un modèle événementiel avancé, intégrant les concepts de Pub/Sub, Event Sourcing, CQRS et saga chorégraphiée. Il a illustré concrètement les bénéfices liés au découplage, à la résilience et à la scalabilité, tout en imposant une rigueur accrue dans la gestion des états et des erreurs.

La transition vers une coordination par événements, sans orchestrateur central, a exigé une modélisation rigoureuse du flux métier et des événements publiés à chaque étape. La saga chorégraphiée s’est révélée particulièrement efficace pour gérer des transactions distribuées complexes, tout en permettant une compensation asynchrone robuste.

L’introduction d’un Event Store indépendant a renforcé la transparence et l’auditabilité du système. La logique de relecture d’événements pour reconstruire un état métier à partir de son historique ouvre la voie à des usages plus avancés, comme la rétro-analyse, le versionnement d’états, ou la migration de logique métier dans le temps.

La séparation CQRS a apporté de la clarté conceptuelle, en distinguant clairement les responsabilités de traitement et de lecture. Combinée à une projection légère, elle permet de construire des vues optimisées, sans coupler directement les services producteurs.

L’observabilité a joué un rôle essentiel dans le débogage et l’analyse du système. Les métriques exposées (latence, volumes, erreurs) ont permis de diagnostiquer rapidement les goulets d’étranglement ou les défaillances de consommation.

En contrepartie, cette architecture induit une complexité supérieure : gestion des duplications, ordering partiel des événements, logique idempotente, outillage de test plus lourd. Des aspects comme la sécurité, la gestion des erreurs silencieuses ou la résilience aux pannes réseau mériteraient d’être renforcés dans une version de production.

Ce projet constitue néanmoins une démonstration concrète de l’intérêt des architectures événementielles dans les systèmes distribués modernes. Il offre une base solide pour approfondir des thématiques comme les brokers distribués (Kafka), le versionnement d’événements, ou encore l’intégration avec des outils de monitoring centralisés (ELK stack, OpenTelemetry).

En résumé, cette expérience met en lumière l’équilibre nécessaire entre flexibilité architecturale, résilience technique et complexité maîtrisée.
