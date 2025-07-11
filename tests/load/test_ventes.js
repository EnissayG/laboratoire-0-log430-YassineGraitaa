import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  vus: 15,
  duration: '30s',
};

export default function () {
  const url = 'http://host.docker.internal:8000/api/ventes/rapport';
  let res = http.get(url, {
    headers: {
      'x-token': 'mon-token-secret'
    }
  });
  check(res, { 'status is 200': (r) => r.status === 200 });
  sleep(1);
}
