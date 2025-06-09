# 📊 Analyse des besoins – Système de caisse (Lab 1)

## 1. Objectif général du système

Développer une application console simple, robuste et évolutive qui permet à un petit magasin de quartier de gérer ses ventes, retours, produits et stock, avec 3 caisses fonctionnant en simultané.

---

## 2. Besoins fonctionnels

L’application doit permettre :

- 🔍 **Recherche de produit**  
  - Par identifiant
  - Par nom
  - Par catégorie

- 🛒 **Enregistrement d’une vente**  
  - Sélection de plusieurs produits
  - Calcul automatique du total
  - Déduction des quantités du stock

- ↩️ **Gestion des retours**  
  - Annulation d’une vente
  - Réajustement du stock

- 📦 **Consultation du stock**  
  - Afficher l’état du stock d’un ou plusieurs produits

- ⚙️ **Soutien multi-caisses**  
  - L’application doit gérer plusieurs sessions de vente sans conflit
  - Transactions simultanées (ex : 3 caisses)

---

## 3. Besoins non-fonctionnels

- 🧩 **Simplicité**  
  Interface console claire et intuitive

- ⚡ **Performance**  
  Temps de réponse rapide même avec 3 utilisateurs en simultané

- 🛡️ **Robustesse**  
  Tolérance aux erreurs, cohérence des données assurée

- 🚀 **Portabilité**  
  L’application doit fonctionner dans un conteneur Docker sur la VM fournie

- 🔁 **Évolutivité**  
  Préparer la base pour supporter une extension en Lab 2 (multi-succursales) et Lab 3 (e-commerce)

- ✅ **CI/CD**  
  Le projet doit être versionné, testé et buildé automatiquement avec GitHub Actions

---

## 4. Contraintes techniques

- 📦 Base de données locale (SQLite)
- ⚙️ Accès direct via ORM (SQLAlchemy)
- 🐍 Langage : Python
- 🐳 Conteneurisation avec Docker
