import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  vus: 10,
  duration: '30s',
};

export default function () {
  let payload = JSON.stringify({
    nom: "Produit modifié",
    categorie: "catégorie test",
    prix: 9.99,
    quantite_stock: 100
  });

  let res = http.put('http://host.docker.internal:8000/api/produits/1', payload, {
    headers: {
      'Content-Type': 'application/json',
      'x-token': 'mon-token-secret'
    }
  });

  check(res, {
    'status is 200': (r) => r.status === 200
  });

  sleep(1);
}
