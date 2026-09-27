import http from 'node:http';
import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { resolve } from 'node:path';
import { TUNING, TURN_TUNING, HIT_TUNING, INPUT_TUNING } from './tuning.js';
import { createGame } from './game.js';
import { createRealtimeGame } from './realtime.js';
import { createLobby, LobbyError } from './lobby.js';

const assets = new Map([
  ['/', ['index.html', 'text/html; charset=utf-8']],
  ['/app.js', ['app.js', 'text/javascript; charset=utf-8']],
  ['/style.css', ['style.css', 'text/css; charset=utf-8']],
]);
const clientRoot = new URL('../client/', import.meta.url);
const MAX_BODY_BYTES = 1024;
async function readBody(req) {
  if (req.headers['content-type']?.split(';')[0] !== 'application/json') throw new LobbyError('Use application/json.', 415);
  let size = 0; const chunks = [];
  for await (const chunk of req) { size += chunk.length; if (size > MAX_BODY_BYTES) throw new LobbyError('Request too large.', 413); chunks.push(chunk); }
  try { return JSON.parse(Buffer.concat(chunks).toString('utf8')); } catch { throw new LobbyError('Invalid JSON.'); }
}

export function createApp({ wind = 0, legacyTestMode = false, layer5 = false, clock } = {}) {
  const game = legacyTestMode ? createGame(wind) : createRealtimeGame(wind, { clock });
  const lobby = layer5 ? createLobby() : null;
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
      if (layer5 && req.method === 'GET' && req.url.startsWith('/api/lobby')) {
        const id = new URL(req.url, 'http://localhost').searchParams.get('sessionId');
        return json(res, 200, lobby.snapshot(id));
      }
      if (layer5 && req.method === 'POST' && req.url === '/api/session') {
        const body = await readBody(req); return json(res, 201, lobby.login(body.displayName));
      }
      if (layer5 && req.method === 'POST' && ['/api/rooms', '/api/rooms/join', '/api/rooms/leave', '/api/rooms/start', '/api/session/disconnect', '/api/chat'].includes(req.url)) {
        const body = await readBody(req);
        const result = req.url === '/api/rooms' ? lobby.createRoom(body.sessionId, body.mode) :
          req.url === '/api/rooms/join' ? lobby.joinRoom(body.sessionId, body.code) :
          req.url === '/api/rooms/leave' ? lobby.leaveRoom(body.sessionId) :
          req.url === '/api/rooms/start' ? lobby.startRoom(body.sessionId) :
          req.url === '/api/session/disconnect' ? lobby.disconnect(body.sessionId) : lobby.sendChat(body.sessionId, body);
        return json(res, 200, result);
      }
      if (req.method === 'GET' && req.url === '/api/state') {
        return json(res, 200, publicState());
      }
      if (req.method === 'POST' && (legacyTestMode ? ['/api/fire', '/api/move'] : ['/api/input']).includes(req.url)) {
        if (req.headers['content-type']?.split(';')[0] !== 'application/json') {
          return json(res, 415, { error: 'Use application/json.' });
        }
        const body = await readBody(req);
        let input;
        try {
          input = body;
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
    } catch (error) {
      if (!res.headersSent) json(res, error.status ?? 500, { error: error.message ?? 'Server request failed.' });
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
  const server = createApp({ wind, layer5: true });
  server.on('error', error => { console.error(error.message); process.exitCode = 1; });
  server.listen(port, host, () => console.log(
    'Hangfire: http://' + host + ':' + server.address().port + ' | server wind=' + wind));
}
