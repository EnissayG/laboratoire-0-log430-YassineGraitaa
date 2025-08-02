import uuid
from sqlalchemy.orm import Session
from app.models.commande import Commande
from app.models.etat_commande_enum import EtatCommande
from app.models.etat_saga import EtatSaga
from app.metrics import commande_etat_total


def changer_etat_commande(
    db: Session,
    saga_id: uuid.UUID,
    nouvel_etat: EtatCommande,
    client_id: int = None,
    magasin_id: int = None,
):
    print(f"📌 [SAGA {saga_id}] Transition -> {nouvel_etat.value}")

    commande = db.query(Commande).filter_by(id=saga_id).first()

    if commande is None:
        commande = Commande(
            id=saga_id,
            etat_actuel=nouvel_etat.value,
            client_id=client_id,
            magasin_id=magasin_id,
        )
        db.add(commande)
    else:
        commande.etat_actuel = nouvel_etat.value

    db.add(EtatSaga(saga_id=saga_id, etat=nouvel_etat.value))
    commande_etat_total.labels(etat=nouvel_etat.value).inc()
    db.commit()
