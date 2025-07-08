# Autoévaluation – LOG430 – Laboratoire 3

**Code permanent** : [À compléter]  
**Cours** : LOG430 – Architecture Logicielle  
**Session** : Été 2025

---

## 1.1 Structuration et REST API

| Éléments | Oui | Non | Commentaire / Justification |
|----------|-----|-----|-----------------------------|
| Les routes REST sont bien définies et respectent les conventions REST | ✅ | | URI claires (`/api/produits`, `/api/ventes/rapport`), utilisation des bons verbes HTTP. |
| L’architecture suit un modèle MVC ou hexagonal (ou une autre architecture justifiée) | ✅ | | Architecture 3-tier mise en place, avec séparation des responsabilités : `routers`, `services`, `models`. |
| Les URIs sont bien structurées (ex : /api/v1/resource) | ✅ | | L’API est regroupée sous le préfixe `/api/`, facilement versionnable. |
| La couche API est clairement séparée de la logique métier | ✅ | | Les fichiers `routers/*.py` appellent les fonctions de `services/*.py`, qui encapsulent la logique métier. |

---

## 1.2 Documentation des API

| Éléments | Oui | Non | Commentaire / Justification |
|----------|-----|-----|-----------------------------|
| La documentation Swagger (OpenAPI) est présente | ✅ | | Accessible à `/docs`, générée automatiquement avec Pydantic et enrichie manuellement. |
| Les méthodes, statuts, entrées/sorties sont décrites | ✅ | | Chaque endpoint définit `response_model`, des `summary`, et des exemples de payloads. |
| SwaggerUI ou Redoc est intégré | ✅ | | SwaggerUI est intégré par défaut à FastAPI, personnalisable avec `custom_openapi`. |
| Des exemples de requêtes/réponses sont fournis | ✅ | | Fournis à la fois dans Swagger (exemples `example=` dans les DTOs) et dans un fichier `.http`. |

---

## 1.3 Sécurité et accessibilité

| Éléments | Oui | Non | Commentaire / Justification |
|----------|-----|-----|-----------------------------|
| CORS est configuré correctement | ✅ | | Middleware `CORSMiddleware` configuré dans `main.py`, autorisant React à faire des requêtes cross-origin. |
| Une authentification est implémentée (token statique, BasicAuth, JWT) | ✅ | | Authentification minimale par `x-token` (vérification via dépendance FastAPI). |
| Les endpoints sensibles sont protégés | ✅ | | Les routes de modification ou rapport sont protégées par la vérification du token. |

---

## 1.4 Tests et validation

| Éléments | Oui | Non | Commentaire / Justification |
|----------|-----|-----|-----------------------------|
| Une collection Postman ou équivalente est fournie | ⚠️ | | Pas de collection Postman, mais un fichier `.http` utilisable dans VSCode. Amélioration possible. |
| Des tests automatisés (pytest, TestClient) sont présents | ✅ | | Tests unitaires via `pytest`, utilisant `TestClient` de FastAPI. |
| Les tests sont intégrés à la CI/CD | ✅ | | Exécutés automatiquement via GitHub Actions (`pytest` dans le workflow). |

---

## 1.5 Déploiement et exécution

| Éléments | Oui | Non | Commentaire / Justification |
|----------|-----|-----|-----------------------------|
| L’API est conteneurisée avec Docker | ✅ | | Dockerfile pour le backend, orchestré via `docker-compose.yml` (API, DB, React). |
| Les instructions d’exécution sont claires dans le README.md | ✅ | | Le README contient les commandes `docker-compose up`, accès Swagger, etc. |
| L’API est fonctionnelle en local ou via conteneur | ✅ | | Testée en local et via conteneurs ; React communique bien avec FastAPI. |

---

## 1.6 Bonnes pratiques REST

| Éléments | Oui | Non | Commentaire / Justification |
|----------|-----|-----|-----------------------------|
| Respect des verbes HTTP (GET, POST, PUT, DELETE, PATCH) | ✅ | | Bon usage des verbes selon la nature des opérations. |
| Utilisation de codes HTTP standard (200, 201, 400, etc.) | ✅ | | FastAPI retourne automatiquement les bons statuts, gestion manuelle des erreurs personnalisées aussi présente. |
| Pagination, tri et filtrage implémentés si pertinent | ✅ | | Implémenté pour les produits : `GET /produits/filtrer?page=...&sort=...&categorie=...`. |
| Messages d’erreur structurés et utiles | ✅ | | Gestion centralisée via `handlers`, logs JSON avec détails : timestamp, message, code, chemin. |

---

## ✅ Évaluation synthétique

Le système développé répond largement aux exigences du laboratoire. Toutes les **fonctions essentielles (Must Have)** ont été livrées, les **fonctions supplémentaires (Should / Could)** ont été partiellement ou totalement intégrées (filtrage, tri, Swagger enrichi, gestion d’erreurs). L’infrastructure technique (Docker, CI/CD, logs) est solide et bien structurée.

Quelques pistes d'amélioration réalistes :
- Fournir une vraie collection Postman (au lieu d’un `.http` uniquement)
- Aller plus loin dans la gestion des rôles et permissions (auth avancée)
- Ajouter des tests de validation croisée (ex: cohérence stock-vente)

---

**Note personnelle estimée :**  
🌟 **~95 %** – Projet complet, réaliste, soigné, avec des choix pertinents, de la rigueur dans la structure, et des bonus utiles. Quelques améliorations possibles mais non bloquantes.

