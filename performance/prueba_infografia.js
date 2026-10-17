import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 5,
  duration: '30s',
  thresholds: {
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['p(95)<800'],
  },
};

export default function () {
  const res = http.get('https://mauriciomubravo.github.io/Historia-de-Liga-MX/');
  check(res, {
    'status 200': (r) => r.status === 200,
    'responde en menos de 800 ms': (r) => r.timings.duration < 800,
    'trae contenido HTML': (r) => r.body.includes('<html'),
  });
  sleep(1);
}
