from .produits import router as produits
from .ventes import router as ventes
from .demandes import router as demandes
from .rapports import router as rapports
from .stock import router as stock
from .magasins import router as magasins  # ✅ Ajouté
from .performance import router as performance  # ✅ Ajouté

__all__ = ["produits", "ventes", "demandes", "rapports", "stock", "performance"]
