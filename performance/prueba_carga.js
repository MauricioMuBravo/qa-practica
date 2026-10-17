import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 5,            // 5 usuarios virtuales
  duration: '30s',   // durante 30 segundos
  thresholds: {
    http_req_failed: ['rate<0.01'],     // menos de 1% de errores
    http_req_duration: ['p(95)<800'],   // p95 menor a 800 ms
  },
};

export default function () {
  const res = http.get('https://test.k6.io');
  check(res, {
    'status 200': (r) => r.status === 200,
    'responde en menos de 800 ms': (r) => r.timings.duration < 800,
  });
  sleep(1);
}
