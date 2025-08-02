| 🔢 Port | 🔧 Service            | 📝 URL à ouvrir                                          | 📌 Remarques                         |
|--------:|----------------------|----------------------------------------------------------|--------------------------------------|
| 5432    | PostgreSQL principal | —                                                        | Base de données du monolithe         |
| 8000    | API Monolithique     | [http://localhost:8000/docs](http://localhost:8000/docs) | `api` FastAPI monolithique           |
| 3000    | Frontend React       | [http://localhost:3000](http://localhost:3000)           | Dashboard utilisateur                |
| 8020    | produits-service     | [http://localhost:8020/docs](http://localhost:8020/docs) | Microservice Produits                |
| 8021    | stock-service        | [http://localhost:8021/docs](http://localhost:8021/docs) | Microservice Stock                   |
| 8022    | ventes-service       | [http://localhost:8022/docs](http://localhost:8022/docs) | Microservice Ventes                  |
| 8023    | magasin-service      | [http://localhost:8023/docs](http://localhost:8023/docs) | Microservice Magasins                |
| 8024    | client-service       | [http://localhost:8024/docs](http://localhost:8024/docs) | Microservice Client                  |
| 8025    | panier-service       | [http://localhost:8025/docs](http://localhost:8025/docs) | Microservice Panier                  |
| 8026    | checkout-service     | [http://localhost:8026/docs](http://localhost:8026/docs) | Microservice Checkout                |
| 8027    | orchestrateur-service| [http://localhost:8027/docs](http://localhost:8027/docs) | **Orchestrateur** de commande (saga) |
| 8081    | NGINX Load Balancer  | [http://localhost:8081](http://localhost:8081)           | Load balancing entre FastAPI 1-2-3   |
| 8090    | KrakenD Gateway      | [http://localhost:8090](http://localhost:8090)           | API Gateway KrakenD                  |
| 9090    | Prometheus           | [http://localhost:9090](http://localhost:9090)           | Monitoring Prometheus                |
| 9113    | NGINX Exporter       | [http://localhost:9113/metrics](http://localhost:9113/metrics) | Exportateur Prometheus (NGINX)  |
| 3009    | Grafana              | [http://localhost:3009](http://localhost:3009)           | Dashboard Grafana                    |
| 8028    | Eventstore              | [http://localhost:8028/docs](http://localhost:8028/docs)          | Event store                   |



docker-compose -f docker-compose.yml -f docker-compose.loadbalancer.yml -f docker-compose.prometheus.yml up --build
docker-compose -f docker-compose.prometheus.yml up --build