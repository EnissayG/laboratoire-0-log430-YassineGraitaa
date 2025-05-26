# Choix technologiques – Justification

| Élément            | Choix               | Justification                                                              |
|--------------------|---------------------|---------------------------------------------------------------------------|
| Langage            | Python 3.11         | Facile à apprendre, rapide à développer, bien supporté                   |
| ORM                | SQLAlchemy          | Abstraction des requêtes SQL, évolutif vers PostgreSQL ou autre          |
| BDD                | PostgreSQL          | Transactions fiables, relations fortes, adapté aux scénarios multi-tables|
| Conteneurisation   | Docker              | Exécution isolée, déploiement reproductible                              |
| Orchestration      | Docker Compose      | Déploiement multi-services (app + db) simple                             |
| CI/CD              | GitHub Actions      | Intégration continue légère, facile à maintenir                          |
| Tests              | Pytest              | Compatible avec Python, simple et modulaire                              |
| Lint               | Black               | Formatage automatique du code                                            |
