import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  vus: 20,
  duration: '30s',
};

export default function () {
  let res = http.get('http://host.docker.internal:8000/api/magasins/1/stock', {
    headers: {
      'x-token': 'mon-token-secret' // à adapter si besoin
    }
  });
  check(res, { 'status is 200': (r) => r.status === 200 });
  sleep(1);
}
