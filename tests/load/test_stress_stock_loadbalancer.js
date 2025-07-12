import http from 'k6/http';
import { check } from 'k6';

export let options = {
  stages: [
    { duration: '15s', target: 10 },
    { duration: '15s', target: 30 },
    { duration: '15s', target: 60 },
    { duration: '15s', target: 100 },
    { duration: '15s', target: 0 },
  ],
};

export default function () {
  let res = http.get('http://host.docker.internal:8081/api/magasins/1/stock', {
    headers: { 'x-token': 'mon-token-secret' }
  });
  check(res, { 'status is 200': (r) => r.status === 200 });
}
