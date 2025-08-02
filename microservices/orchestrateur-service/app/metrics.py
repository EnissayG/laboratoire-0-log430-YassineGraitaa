from prometheus_client import Counter

commande_etat_total = Counter(
    "commande_etat_total", "Total des commandes par état", ["etat"]
)
