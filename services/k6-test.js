// portfolio-stress-test.js
import { check, group } from 'k6';
import http from 'k6/http';
import { htmlReport } from "https://raw.githubusercontent.com/benc-uk/k6-reporter/main/dist/bundle.js";

const BASE_URL = 'https://yoganova.my.id';

export const options = {
  stages: [
    { duration: '30s', target: 20 },
    { duration: '2m', target: 100 },
    { duration: '1m', target: 200 },
    { duration: '30s', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<800'],
    http_req_failed: ['rate<0.01'],
    checks: ['rate>0.99']
  },
};

export default function () {
  group('Homepage Load Test', () => {
    const response = http.get(BASE_URL);

    check(response, {
      'Status 200': (r) => r.status === 200,
      'Response time < 800ms': (r) => r.timings.duration < 800,
      'Correct content type': (r) => r.headers['Content-Type'] === 'text/html; charset=UTF-8',
      'Homepage contains "Yoga Novaindra"': (r) => r.body.includes('Yoga Novaindra'),
  });
  });

  group('Static Assets', () => {
    const avatar = http.get(`${BASE_URL}/img/avatar.webp`);
    check(avatar, {
      'Avatar status 200': (r) => r.status === 200,
      'Correct content type': (r) => r.headers['Content-Type'] === 'image/webp'
    });
  });
}

export function handleSummary(data) {
  return {
    "summary.html": htmlReport(data),
  };
}