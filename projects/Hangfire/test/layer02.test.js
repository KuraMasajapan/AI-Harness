import test from 'node:test';
import assert from 'node:assert/strict';
import { once } from 'node:events';
import { createGame, selectNextPlayer } from '../server/game.js';
import { createApp } from '../server/index.js';
import { TUNING, TURN_TUNING as T } from '../server/tuning.js';
import { simulate } from '../server/projectile.js';

const fire = { angle: TUNING.DEFAULT_ANGLE, power: TUNING.DEFAULT_POWER };
const move = { direction: 'right', amount: T.DEFAULT_MOVE_DISTANCE };
const inputFor = (game, fields) => ({
  playerId: game.snapshot().currentPlayer, expectedRevision: game.snapshot().revision, ...fields,
});
const act = (game, type, fields) => game.act(type, inputFor(game, fields));
const player = (state, id) => state.players.find(p => p.id === id);
function rejectUnchanged(game, type, input, pattern) {
  const before = game.snapshot();
  assert.throws(() => game.act(type, input), pattern);
  assert.deepEqual(game.snapshot(), before);
}

test('initial state, deterministic minimum/tie selection and detached snapshots', () => {
  const game = createGame(0), first = game.snapshot();
  assert.equal(first.currentPlayer, 'A');
  assert.equal(first.logicalTime, 0);
  assert.equal(first.players.length, 2);
  assert.ok(first.players.every(p => p.resource === T.RESOURCE_MAX && p.nextActionTime === 0));
  assert.equal(selectNextPlayer([...first.players].reverse()).id, 'A');
  const changed = structuredClone(first.players);
  changed[0].nextActionTime = 50;
  changed[1].nextActionTime = 10;
  assert.equal(selectNextPlayer(changed).id, 'B');
  first.players[0].resource = 999;
  first.wind = 999;
  first.currentPlayer = 'B';
  assert.equal(game.snapshot().currentPlayer, 'A');
  assert.equal(game.snapshot().players[0].resource, T.RESOURCE_MAX);
  assert.equal(game.snapshot().wind, 0);
});
test('FIRE spends resource, updates delay, uses original projectile and selects B', () => {
  const game = createGame(0);
  const next = act(game, 'FIRE', fire);
  assert.equal(player(next, 'A').resource, T.RESOURCE_MAX - T.FIRE_RESOURCE_COST);
  assert.equal(player(next, 'A').nextActionTime, T.FIRE_ACTION_COST);
  assert.equal(next.currentPlayer, 'B');
  assert.equal(next.logicalTime, 0);
  assert.deepEqual(next.latestShot, { id: 1, playerId: 'A', ...simulate(fire, 0) });
});
test('different costs produce B,B,B,A rather than strict alternation', () => {
  const game = createGame(0);
  act(game, 'FIRE', fire); // A 30, B 0
  assert.equal(act(game, 'MOVE', move).currentPlayer, 'B'); // B 10
  assert.equal(act(game, 'MOVE', move).currentPlayer, 'B'); // B 20
  const next = act(game, 'MOVE', move); // B 30; tie -> A
  assert.equal(next.currentPlayer, 'A');
  assert.equal(next.logicalTime, T.FIRE_ACTION_COST);
  assert.equal(player(next, 'B').resource, T.RESOURCE_MAX - 3 * move.amount * T.MOVE_RESOURCE_COST_PER_UNIT);
  assert.equal(player(next, 'B').nextActionTime, 3 * T.MOVE_ACTION_COST);
  const after = act(game, 'FIRE', fire);
  assert.equal(player(after, 'A').nextActionTime, 2 * T.FIRE_ACTION_COST);
  assert.equal(after.logicalTime, T.FIRE_ACTION_COST);
});
test('left/right move commits X and resource; later fire starts at server position', () => {
  const game = createGame(0);
  act(game, 'MOVE', { ...move, direction: 'left' });
  act(game, 'MOVE', move);
  const before = game.snapshot();
  assert.equal(player(before, 'A').position.x, T.PLAYER_A_X - move.amount);
  assert.equal(player(before, 'B').position.x, T.PLAYER_B_X + move.amount);
  const next = act(game, 'FIRE', fire);
  assert.deepEqual(next.latestShot.impact, simulate(fire, 0, player(before, 'A').position.x).impact);
  assert.equal(next.latestShot.initial.x, player(before, 'A').position.x);
  assert.equal(next.latestShot.path[0].x, player(before, 'A').position.x);
});
test('invalid actor/action/input/state injection always preserves full state', () => {
  const game = createGame(0);
  rejectUnchanged(game, 'FIRE', { ...inputFor(game, fire), playerId: 'B' }, /current/);
  rejectUnchanged(game, 'FIRE', { ...inputFor(game, fire), playerId: 'unknown' }, /Unknown/);
  for (const key of ['resource', 'resourceCost', 'actionCost', 'nextActionTime',
    'currentPlayer', 'logicalTime', 'position', 'wind', 'impact', 'players']) {
    rejectUnchanged(game, 'FIRE', { ...inputFor(game, fire), [key]: 999 }, /fields/);
    rejectUnchanged(game, 'MOVE', { ...inputFor(game, move), [key]: 999 }, /fields/);
  }
  for (const amount of [0, -1, 1.5, T.MOVE_MAX_DISTANCE + 1, Infinity, NaN, '5', null]) {
    rejectUnchanged(game, 'MOVE', inputFor(game, { ...move, amount }), /MOVE/);
  }
  rejectUnchanged(game, 'MOVE', inputFor(game, { ...move, direction: 'up' }), /MOVE/);
  rejectUnchanged(game, 'FIRE', inputFor(game, { ...fire, angle: 1000 }), /angle/);
  rejectUnchanged(game, 'PASS', inputFor(game, {}), /fields/);
  for (const bad of [null, [], {}, fire]) rejectUnchanged(game, 'FIRE', bad, /fields/);
});
test('exhaustion rejects FIRE and MOVE without changing anything; no silent refill/skip', () => {
  const game = createGame(0);
  for (let i = 0; i < 2 * T.RESOURCE_MAX / T.FIRE_RESOURCE_COST; i++) act(game, 'FIRE', fire);
  assert.ok(game.snapshot().players.every(p => p.resource === 0));
  rejectUnchanged(game, 'FIRE', inputFor(game, fire), /Insufficient/);
  rejectUnchanged(game, 'MOVE', inputFor(game, move), /Insufficient/);
});
test('insufficient MOVE rejected when some resource remains; stale same-player retry rejected', () => {
  const game = createGame(0);
  for (let i = 0; i < 8; i++) act(game, 'FIRE', fire); // 20 each
  rejectUnchanged(game, 'MOVE', inputFor(game, { ...move, amount: T.MOVE_MAX_DISTANCE }), /Insufficient/);
  const fresh = createGame(0);
  act(fresh, 'FIRE', fire);
  const request = inputFor(fresh, move);
  fresh.act('MOVE', request);
  assert.equal(fresh.snapshot().currentPlayer, 'B');
  rejectUnchanged(fresh, 'MOVE', request, /Stale/);
});

test('HTTP guards both routes, concurrent duplicate atomicity, invalid transport unchanged', async t => {
  const server = createApp();
  server.listen(0, '127.0.0.1');
  await once(server, 'listening');
  t.after(() => new Promise(resolve => server.close(resolve)));
  const root = 'http://127.0.0.1:' + server.address().port;
  const get = async () => (await fetch(root + '/api/state')).json();
  const post = (route, input) => fetch(root + route, {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(input),
  });
  let before = await get();
  for (const route of ['/api/fire', '/api/move']) {
    const fields = route.endsWith('fire') ? fire : move;
    assert.equal((await post(route, fields)).status, 400); // no legacy bypass
    assert.equal((await post(route, { playerId: 'B', expectedRevision: 0, ...fields })).status, 409);
    assert.equal((await post(route, { playerId: 'A', expectedRevision: 0, ...fields, resource: 999 })).status, 400);
    assert.deepEqual(await get(), before);
  }
  assert.equal((await post('/api/fire', { playerId: 'A', expectedRevision: 0, ...fire })).status, 200);
  const duplicate = { playerId: 'B', expectedRevision: 1, ...move };
  const results = await Promise.all([post('/api/move', duplicate), post('/api/move', duplicate)]);
  assert.deepEqual(results.map(r => r.status).sort(), [200, 409]);
  before = await get();
  assert.equal(before.revision, 2);
  assert.equal(player(before, 'B').position.x, T.PLAYER_B_X + move.amount);
  assert.equal(player(before, 'B').resource, T.RESOURCE_MAX - move.amount * T.MOVE_RESOURCE_COST_PER_UNIT);
  for (const body of ['{', ' '.repeat(2048), 'null']) {
    const response = await fetch(root + '/api/move', { method: 'POST',
      headers: { 'Content-Type': 'application/json' }, body });
    assert.ok([400, 413].includes(response.status));
    assert.deepEqual(await get(), before);
  }
  const copy = await get();
  copy.players[0].resource = 1000; copy.currentPlayer = 'A'; copy.logicalTime = -9;
  assert.deepEqual(await get(), before);
});
