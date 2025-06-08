## Analyse du système existant (Lab 1)

### Architecture actuelle
Le système est basé sur une architecture 2-tier :
- Une application console (main.py) qui sert d'interface utilisateur.
- Une couche de services métier pour la gestion des ventes et des produits.
- Une base de données PostgreSQL, conteneurisée séparément via Docker Compose.
- Un ORM (SQLAlchemy) assure l'accès aux données.

### Forces
- Bonne modularité du code (services, modèles, configuration séparés).
- Tests unitaires déjà en place.
- Pipeline CI/CD fonctionnelle.
- Documentation structurée avec diagrammes et ADR.

### Limites
- Couplage fort entre interface console, services et DB.
- Non accessible à distance (console locale uniquement).
- Pas de séparation claire entre logique métier et infrastructure.
- Impossible d'ajouter facilement de nouveaux clients (web, mobile, autres magasins).
- Non scalable en l'état : une seule instance fonctionne à la fois.

### Besoin d’évolution
Le système doit évoluer vers une architecture distribuée ou 3-tier avec :
- Une couche API centralisée (ex. FastAPI)
- Des clients distants (magasins, maison mère)
- Un stockage de données centralisé
- Une synchronisation fiable des données
