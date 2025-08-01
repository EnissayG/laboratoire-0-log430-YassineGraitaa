from enum import Enum
from pydantic import BaseModel


class EtatCommande(str, Enum):
    INITIEE = "Initiée"
    STOCK_RESERVE = "Stock réservé"
    PAIEMENT_EFFECTUE = "Paiement effectué"
    COMMANDE_ENREGISTREE = "Commande enregistrée"
    CONFIRMEE = "Confirmée"
    ECHEC_STOCK = "Échec stock"
    ECHEC_PAIEMENT = "Échec paiement"
    ECHEC_ENREGISTREMENT = "Échec enregistrement"
    ANNULEE = "Annulée"


class CommandeInput(BaseModel):
    client_id: int
    magasin_id: int
