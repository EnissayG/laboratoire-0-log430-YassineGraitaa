import logging
from logging.handlers import RotatingFileHandler
import os

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "app_errors.log")

# Créer dossier si inexistant
os.makedirs(LOG_DIR, exist_ok=True)

# Config du logger
logger = logging.getLogger("log430")
logger.setLevel(logging.INFO)

handler = RotatingFileHandler(LOG_FILE, maxBytes=5_000_000, backupCount=3)
formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] %(message)s (%(filename)s:%(lineno)d)"
)
handler.setFormatter(formatter)
logger.addHandler(handler)
