# 🧠 ADR #2 – Gestion explicite des états de commande via machine d’état persistée

## 🎯 Contexte

Dans une saga orchestrée répartie sur plusieurs microservices, le suivi de l’évolution de l’état de la commande est **critique** pour la cohérence du système. Il est impératif de pouvoir savoir :

- où la commande se trouve dans le processus (stock, paiement, vente…),
- si un échec est survenu et à quelle étape,
- comment effectuer un rollback ou déclencher une action compensatoire.

## ✅ Décision

Nous avons mis en place une **machine d’état explicite et persistée**, pilotée par l’orchestrateur. Deux structures sont utilisées pour assurer cette gestion :

1. Un **enum** `EtatCommande` définit tous les états possibles de la commande (initiation, validation, échecs, confirmation).
2. Une **table Commande** contient un champ `etat_actuel` mis à jour à chaque transition.
3. Une **table EtatSaga** conserve l’historique complet des transitions (`saga_id`, `état`, `timestamp`).

Chaque transition est aussi **instrumentée avec Prometheus** pour permettre le monitoring temps réel de la répartition des commandes par état.

## 📌 Conséquences

- 📋 **Clarté** : chaque état est nommé explicitement et visible via un endpoint `/api/commande/{id}`.
- 🧪 **Testabilité** : permet de valider des cas d’échec (stock/paiement) en suivant l’évolution des états.
- 📊 **Observabilité** : les métriques permettent d’observer le taux d’échecs ou de confirmations dans Grafana.
- 💾 **Persistance** : même après redémarrage, l’historique et l’état sont disponibles.

## ⚙️ Implémentation

- La fonction `changer_etat_commande(...)` :
  - met à jour la table `Commande` avec l’état courant,
  - insère un enregistrement dans `EtatSaga`,
  - incrémente le compteur Prometheus `commande_etat_total{etat="..."}`
- Le service `saga_checkout.py` appelle cette fonction après chaque étape réussie ou échouée.

## 🚨 Alternatives considérées

- ❌ **Gestion en mémoire** :
  - plus rapide, mais perdue au redémarrage,
  - difficile à tester en environnement distribué.
- ❌ **État implicite dans les logs ou files d’attente** :
  - difficile à tracer,
  - nécessite un moteur externe de corrélation.

## 🧩 Justification

- Ce choix répond à des objectifs pédagogiques :
  - mettre en œuvre les **principes DDD (état explicite, persisté)**,
  - intégrer **l’observabilité** comme exigence non fonctionnelle (Prometheus, Grafana),
  - permettre une **analyse post-mortem** des commandes échouées.

---

