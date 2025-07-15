FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 👇 Copie ton dossier app dans /app/app
COPY ./app ./app

# ✅ Pour que "from app.models" fonctionne
ENV PYTHONPATH=/app

# ✅ Lance à partir du module app.main
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
