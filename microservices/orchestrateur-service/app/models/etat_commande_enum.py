# app/models/etat_commande_enum.py

from enum import Enum


class EtatCommande(str, Enum):
    """Énumération des états possibles d'une commande dans la saga orchestrée."""

    INITIEE = "Initiée"
    PANIER_RECUPERE = "Panier récupéré"
    STOCK_RESERVE = "Stock réservé"
    PAIEMENT_EFFECTUE = "Paiement effectué"
    COMMANDE_ENREGISTREE = "Commande enregistrée"
    CONFIRMEE = "Confirmée"

    ECHEC_PANIER = "Échec panier"
    ECHEC_STOCK = "Échec stock"
    ECHEC_PAIEMENT = "Échec paiement"
    ECHEC_ENREGISTREMENT = "Échec enregistrement"
    ANNULEE = "Annulée"
