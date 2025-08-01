from pydantic import BaseModel, EmailStr


class ClientCreate(BaseModel):
    nom: str
    email: EmailStr
    adresse: str | None = None


class ClientDTO(ClientCreate):
    id: int

    class Config:
        orm_mode = True


class Paiement(BaseModel):
    montant: float
