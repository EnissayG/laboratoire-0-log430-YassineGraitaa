# Utilise une image Python légère
FROM python:3.11-slim

# Dépendances système pour PostgreSQL
RUN apt-get update && apt-get install -y gcc libpq-dev

# Répertoire de travail dans le conteneur
WORKDIR /app

# Copie les fichiers du projet dans le conteneur
COPY . .

# Installe les dépendances Python
RUN pip install -r requirements.txt

# Point d'entrée : exécute ton application console
CMD ["python", "app.py"]
