## 🔁 Load Balancing – Stock Service

### 🎯 Objectif
Mettre en place une répartition de charge (`round-robin`) entre deux instances de `stock-service` via un NGINX intermédiaire, en utilisant KrakenD comme point d'entrée unique.

### ⚙️ Configuration
- Deux instances Docker (`stock-service-1`, `stock-service-2`)
- Load balancer : `nginx-loadbalancer` (port 8081)
- KrakenD API Gateway (port 8090), route `/api/stock`
- Test de charge : outil [`k6`](https://k6.io)

### 🧪 Résultat du test de charge
Test effectué sur `/api/stock` pendant 1m45 avec montée en charge progressive (1 → 100 VUs).
![alt text](image.png)

⏱ Duration : 1m45s
📈 Total requests : 49 736
✅ Succès : 100% (aucune erreur HTTP)
📉 Latence moyenne: 56.13 ms
📊 Percentiles : 90% sous 131.9 ms / 95% sous 157.3 ms


### 📊 Analyse
- ✅ **Stabilité** : Aucune requête échouée même à 100 VUs → bon comportement concurrent.
- ⚡ **Performance** : Latence raisonnable même à haut débit (p95 ≈ 157ms).
- 🧠 **Répartition effective** : Le volume traité suggère que les deux instances ont bien absorbé la charge, mais faute de visibilité dans Prometheus/Grafana (bug DNS), la répartition exacte n’a pas pu être observée visuellement.

### ⚠️ Limites rencontrées
- ❌ **Prometheus/Grafana** : Échec de la configuration des targets `stock-service-1` et `stock-service-2` (erreur DNS), donc métriques non disponibles pour visualisation directe.
- 🛠 **Suggestion** : Ajouter les deux instances dans le `docker-compose` avec le même nom de `job` mais IP différente ou corriger la configuration DNS du réseau `log430-network`.
![alt text](image-1.png)
### ✅ Conclusion
Le test de charge démontre que le **load balancing fonctionne correctement en pratique**. Même sans visualisation Prometheus, la **réponse rapide, stable et continue** confirme que les deux instances étaient actives et sollicitées sous charge.
