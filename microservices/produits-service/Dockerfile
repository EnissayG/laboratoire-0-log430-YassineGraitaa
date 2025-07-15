FROM python:3.11-slim

# Crée un dossier pour l'app
WORKDIR /app

# Copie les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie le dossier app (contenant ton code source)
COPY ./app ./app

# Ajoute le dossier app/ au PYTHONPATH
ENV PYTHONPATH=/app

# Lance Uvicorn avec app.main
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
