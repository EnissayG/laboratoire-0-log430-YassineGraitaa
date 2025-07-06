# app/security.py
from fastapi import Header, HTTPException

API_TOKEN = "mon-token-secret"


def verifier_token(x_token: str = Header(...)):
    if x_token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Token invalide")
