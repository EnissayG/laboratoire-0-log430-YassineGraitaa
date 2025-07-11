## 📡 1.2 Observabilité de base

Dans cette section, nous avons instrumenté l’API FastAPI afin de collecter et visualiser des métriques via Prometheus et Grafana.  
L’objectif est d’observer les **4 Golden Signals** décrits par les pratiques SRE de Google : **latence, trafic, erreurs et saturation**.

Un endpoint `/metrics` a été exposé grâce à `prometheus_fastapi_instrumentator`, et les données sont collectées toutes les 5 secondes par Prometheus. Grafana est utilisé pour l’exploration et l’affichage graphique.

---

### 🔧 Mise en place technique

- 📦 Exportation des métriques via `prometheus_fastapi_instrumentator`
- 🐳 Déploiement de Prometheus et Grafana avec `docker-compose`
- 🔁 Test de charge généré avec `k6` pour simuler du trafic
- 📊 Dashboard Grafana personnalisé, incluant les 4 signaux

---

### 📈 Golden Signals observés

#### 1. **Latence moyenne**

La latence est mesurée par la division de `rate(http_request_duration_seconds_sum)` sur `rate(http_request_duration_seconds_count)`, agrégée par `handler`.  
Cela nous donne un aperçu précis du temps moyen de traitement par endpoint.

![Latence moyenne](images/latence_moyenne.png)

> 💬 On observe une latence moyenne relativement stable (~120–350 ms), avec une hausse lors des tests de stress.

---

#### 2. **Trafic HTTP**

Le trafic est mesuré en **requêtes par seconde (RPS)** à l’aide de :
```promql
sum by (handler) (rate(http_requests_total[1m]))
```

![Trafic HTTP](images/trafic_http.png)

> 💬 Le volume de requêtes augmente fortement durant les phases de test (jusqu'à ~120 RPS).

---

#### 3. **Erreurs HTTP**

Les erreurs 4xx (utilisateur) et 5xx (serveur) sont agrégées séparément.

- 4xx :
```promql
sum by (handler) (rate(http_requests_total{status=~"4.."}[1m]))
```
- 5xx :
```promql
rate(http_requests_total{status=~"5.."}[1m])
```

![Erreurs 4xx](images/erreurs_4xx.png)  
![Erreurs 5xx](images/erreurs_5xx.png)

> 💬 Les erreurs 422 et 404 ont été générées volontairement lors des tests pour valider la robustesse des routes.

---

#### 4. **Saturation (CPU)**

Nous avons utilisé :
```promql
rate(process_cpu_seconds_total[1m])
```
pour estimer la charge CPU du processus FastAPI.

![Saturation CPU](images/saturation_cpu.png)

> 💬 Une montée progressive de l'utilisation CPU est visible lors des tests de stress (jusqu'à 0.8s/s ≈ 80% d’un cœur CPU).

---

### ✅ Résultat

L’observabilité est en place et a permis de :
- Diagnostiquer les limites de performance avant optimisations
- Quantifier les effets des tests de charge
- Préparer les bases pour l’étape suivante : **mise en place d’un Load Balancer**



## 🔍 Analyse des points faibles de l’architecture

L’analyse des métriques collectées via Prometheus et visualisées dans Grafana a permis d’identifier plusieurs points sensibles au sein de notre système actuel :

---

### 1. Goulets d’étranglement observés

#### 🔸 Endpoint lent : `/api/ventes/rapport`

La latence moyenne mesurée sur ce point d’accès s’élevait à plus de **350 ms** en p95 durant les tests de stress. Ce comportement indique une requête complexe, probablement causée par :
- des **agrégations SQL** coûteuses (`GROUP BY`, `JOIN`)
- un **volume de données croissant** dans les tables `ventes`, `produits` ou `magasins`
- l’absence d’un **mécanisme de cache**

#### 🔸 Endpoint `/api/magasins/{id}/stock`

Bien que performant en moyenne, cet endpoint a montré une **hausse de la latence** à fort trafic. Cela peut indiquer :
- des **requêtes SQL non indexées** sur les colonnes `magasin_id` ou `produit_id`
- un **pool de connexions limité** côté backend ou base de données

---

### 2. Taux d’erreurs observé

Grâce aux requêtes filtrées sur les `status=~"4.."` et `status=~"5.."`, on a identifié :
- des erreurs 422 volontaires générées via des requêtes invalides (expected ✅)
- aucun 5xx en temps normal, ce qui indique **une bonne stabilité serveur**

Cependant, il conviendrait d'**anticiper les cas de charge extrême** où les ressources serveur ou la base pourraient devenir indisponibles.

---

### 3. Saturation progressive

Le panel de saturation basé sur :
```promql
rate(process_cpu_seconds_total[1m])
```
montre une montée significative du CPU vers **0.7s/s** (soit ~70 % d'un cœur) lors des tests à 100 utilisateurs virtuels (VU). Cela indique une **proximité du point de rupture**.

---

### ✅ Recommandations (sans augmenter les ressources)

| Amélioration | Détail |
|--------------|--------|
| ✅ **Indexation** | Ajouter des index sur `magasin_id`, `produit_id`, `date` dans les tables `ventes` et `stocks` |
| ✅ **Requêtes SQL** | Optimiser les requêtes de `/rapports` pour limiter les agrégations inutiles |
| ✅ **Cache applicatif** | Mettre en cache les résultats de `/rapports` ou `/stock` via Redis ou cache mémoire |
| ✅ **Taille du pool SQLAlchemy** | Augmenter la taille du pool de connexions si tu observes des blocages fréquents |
| ✅ **Prévoir le load balancing** | Étape suivante du labo : NGINX + plusieurs instances FastAPI |

---

L'ensemble de ces actions permettra de **mieux préparer l'application à la montée en charge**, tout en conservant la même infrastructure de base.
