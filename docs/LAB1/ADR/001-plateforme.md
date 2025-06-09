# ADR 001 – Choix de la plateforme

## Contexte

Le système doit être développé dans un environnement contrôlé et facilement déployable dans une machine virtuelle Linux (fournie dans le cadre du cours). La portabilité, la reproductibilité, et la facilité d'automatisation sont essentielles.

## Décision

Nous avons choisi :
- Le langage **Python 3.11**
- **Docker** pour conteneuriser l'application
- **Docker Compose** pour orchestrer les services (app + BDD)
- Une base de données **PostgreSQL** accessible dans un conteneur dédié

## Justification

- **Portabilité** : Docker permet d'assurer un environnement identique en développement, test et production.
- **Reproductibilité** : Docker Compose permet de lancer tous les services d’un seul coup.
- **Simplicité** : Python est clair, lisible, et bien adapté pour des applications console rapides à développer.

## Conséquences

- L'environnement est maîtrisé, isolé et reproductible
- La configuration initiale peut être légèrement plus complexe qu’avec SQLite, mais elle respecte une architecture 2-tier réelle
