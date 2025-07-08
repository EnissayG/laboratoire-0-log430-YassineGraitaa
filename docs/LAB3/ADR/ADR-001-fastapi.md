# ADR-001 : Choix de FastAPI comme backend REST

## Statut
Accepté

## Contexte
Dans le cadre de l’évolution du système de caisse vers une architecture plus distribuée (Lab 2), il est nécessaire d’introduire une couche serveur (API) entre le client (console ou futur web) et la base de données.

L’architecture précédente était 2-tier : la console appelait directement les services et la base (via SQLAlchemy). Cette structure est rigide et ne permet pas un accès distant ou multi-client.

## Décision
Nous avons choisi d’utiliser **FastAPI** comme framework pour construire l’API REST du backend.

## Raisons
- ✅ **Performance** : FastAPI est basé sur Starlette et Uvicorn, très performant pour des APIs web.
- ✅ **Support natif des types (type hints)** : facilite la documentation, la validation et l’introspection.
- ✅ **Swagger UI auto-généré** : idéal pour tester rapidement et exposer l’API.
- ✅ **Intégration avec SQLAlchemy** : facile à intégrer avec l’ORM existant.
- ✅ **Communauté active** et documentation claire.

## Alternatives considérées
- **Flask** : plus minimaliste, mais nécessiterait plus de configuration manuelle (docs, validation).
- **Django REST Framework** : trop lourd pour les besoins du projet actuel.
- **Node.js (Express)** : bon choix pour le web, mais l’écosystème Python était plus cohérent avec le projet initial.

## Conséquences
- Toute interaction avec les données passe désormais par l’API FastAPI.
- L’ancienne console directe est isolée dans `console.py`.
- Les tests unitaires et intégration doivent désormais viser les routes HTTP.
- Le projet évolue vers une architecture **3-tier** : Client ↔ API ↔ DB.

## Auteurs
Yassine Graitaa – Étudiant LOG430
