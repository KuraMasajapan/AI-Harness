import http from 'node:http';
import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { resolve } from 'node:path';
import { TUNING, TURN_TUNING, HIT_TUNING, INPUT_TUNING } from './tuning.js';
import { createGame } from './game.js';
import { createRealtimeGame } from './realtime.js';

const assets = new Map([
  ['/', ['index.html', 'text/html; charset=utf-8']],
  ['/app.js', ['app.js', 'text/javascript; charset=utf-8']],
  ['/style.css', ['style.css', 'text/css; charset=utf-8']],
]);
const clientRoot = new URL('../client/', import.meta.url);
const MAX_BODY_BYTES = 1024;

export function createApp({ wind = 0, legacyTestMode = false, clock } = {}) {
  const game = legacyTestMode ? createGame(wind) : createRealtimeGame(wind, { clock });
  const publicState = () => ({ ...game.snapshot(), tuning: TUNING, turnTuning: TURN_TUNING,
    hitTuning: HIT_TUNING, inputTuning: INPUT_TUNING });
  const json = (res, code, data) => {
    res.writeHead(code, { 'Content-Type': 'application/json; charset=utf-8' });
    res.end(JSON.stringify(data));
  };
  const server = http.createServer(async (req, res) => {
    res.setHeader('Cache-Control', 'no-store');
    res.setHeader('X-Content-Type-Options', 'nosniff');
    res.setHeader('Content-Security-Policy',
      "default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; frame-ancestors 'none'");
    try {
      if (req.method === 'GET' && req.url === '/api/state') {
        return json(res, 200, publicState());
      }
      if (req.method === 'POST' && (legacyTestMode ? ['/api/fire', '/api/move'] : ['/api/input']).includes(req.url)) {
        if (req.headers['content-type']?.split(';')[0] !== 'application/json') {
          return json(res, 415, { error: 'Use application/json.' });
        }
        let size = 0;
        const chunks = [];
        for await (const chunk of req) {
          size += chunk.length;
          if (size > MAX_BODY_BYTES) {
            json(res, 413, { error: 'Request too large.' });
            return;
          }
          chunks.push(chunk);
        }
        let input;
        try {
          input = JSON.parse(Buffer.concat(chunks).toString('utf8'));
          if (legacyTestMode) game.act(req.url === '/api/fire' ? 'FIRE' : 'MOVE', input);
          else game.act(input);
        } catch (error) {
          return json(res, error.status ?? 400, { error: error.message });
        }
        return json(res, 200, publicState());
      }
      const asset = req.method === 'GET' && assets.get(req.url);
      if (asset) {
        const body = await readFile(new URL(asset[0], clientRoot));
        res.writeHead(200, { 'Content-Type': asset[1] });
        return res.end(body);
      }
      json(res, 404, { error: 'Not found.' });
    } catch {
      if (!res.headersSent) json(res, 500, { error: 'Server request failed.' });
      else res.end();
    }
  });
  server.requestTimeout = 5000;
  server.headersTimeout = 5000;
  let timer;
  server.on('listening', () => {
    if (!legacyTestMode) timer = setInterval(() => game.advance(), INPUT_TUNING.SERVER_TICK_MS);
    timer?.unref();
  });
  server.on('close', () => clearInterval(timer));
  return server;
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const wind = Number(process.env.WIND ?? 0);
  const port = Number(process.env.PORT ?? 3000);
  const host = process.env.HOST ?? '127.0.0.1';
  const server = createApp({ wind });
  server.on('error', error => { console.error(error.message); process.exitCode = 1; });
  server.listen(port, host, () => console.log(
    'Hangfire: http://' + host + ':' + server.address().port + ' | server wind=' + wind));
}
