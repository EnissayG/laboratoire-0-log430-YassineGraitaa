# Utilise une image Python légère
FROM python:3.11-slim

# Répertoire de travail dans le conteneur
WORKDIR /app

# Copie le contenu local dans le conteneur
COPY . .

# Installe pytest
RUN pip install pytest

# Point d'entrée : exécute ton app
CMD ["python", "app.py"]
