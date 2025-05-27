from app.db import init_db
from app.services.produit_service import rechercher_produit, afficher_tout_le_stock
from app.services.vente_service import enregistrer_vente, annuler_vente


def afficher_menu():
    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("0. Ajouter un produit")
        print("1. Rechercher un produit")
        print("2. Enregistrer une vente")
        print("3. Consulter le stock")
        print("4. Annuler une vente")
        print("5. Quitter")

        choix = input("Votre choix : ")

        if choix == "1":
            critere = input("Entrez un nom, catégorie ou ID de produit : ")
            produits = rechercher_produit(critere)
            if not produits:
                print("❌ Aucun produit trouvé.")
            else:
                for p in produits:
                    print(p)
        elif choix == "0":
            nom = input("Nom du produit : ")
            categorie = input("Catégorie : ")
            prix = input("Prix : ")
            stock = input("Quantité en stock : ")

            if not prix.replace(".", "").isdigit() or not stock.isdigit():
                print("❌ Prix ou quantité invalide.")
            else:
                from app.services.produit_service import ajouter_produit
                produit = ajouter_produit(nom, categorie, float(prix), int(stock))
                print(f"✅ Produit ajouté : {produit}")


        elif choix == "2":
            panier = []
            while True:
                produit_id = input("ID produit (ou 'fin' pour terminer) : ")
                if produit_id.lower() == "fin":
                    break
                quantite = input("Quantité : ")
                if not quantite.isdigit():
                    print("⚠️ Quantité invalide.")
                    continue
                panier.append(
                    {"produit_id": int(produit_id), "quantite": int(quantite)}
                )

            if panier:
                vente = enregistrer_vente(panier)
                if vente:
                    print(
                        f"✅ Vente enregistrée (total : {vente.total:.2f}$) — ID: {vente.id}"
                    )
                else:
                    print("❌ Erreur lors de la vente.")
            else:
                print("⚠️ Aucun produit sélectionné.")

        elif choix == "3":
            produits = afficher_tout_le_stock()
            for p in produits:
                print(f"[{p.id}] {p.nom} — {p.quantite_stock} unités")

        elif choix == "4":
            vente_id = input("ID de la vente à annuler : ")
            if vente_id.isdigit():
                success = annuler_vente(int(vente_id))
                if success:
                    print("✅ Vente annulée avec succès.")
                else:
                    print("❌ Vente introuvable ou erreur.")
            else:
                print("❌ ID invalide.")

        elif choix == "5":
            print("👋 Au revoir !")
            break

        else:
            print("❌ Choix invalide.")


def main():
    init_db()
    afficher_menu()


if __name__ == "__main__":
    main()
