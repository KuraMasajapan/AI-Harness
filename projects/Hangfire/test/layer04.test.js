import test from 'node:test';
import assert from 'node:assert/strict';
import { once } from 'node:events';
import { createRealtimeGame } from '../server/realtime.js';
import { createApp } from '../server/index.js';
import { simulate } from '../server/projectile.js';
import { INPUT_TUNING as T } from '../server/tuning.js';

function fixture() {
  let time = 0, seq = 0;
  const game = createRealtimeGame(0, { clock: () => time });
  const at = t => { time = t; return game.snapshot(); };
  const send = (type, fields = {}) => {
    const s = game.snapshot();
    return game.act({ playerId: s.currentPlayer, turnId: s.turn.id, sequence: ++seq, type, ...fields });
  };
  return { game, at, send };
}
test('20 seconds: timeout without shot, stale input cannot control following turn', () => {
  const f = fixture();
  const initial = f.at(0);
  assert.equal(initial.turn.remainingSeconds, 20);
  f.send('HOLD', { move: 1, aim: 1 });
  assert.equal(f.at(19.999).currentPlayer, 'A');
  const after = f.at(20);
  assert.equal(after.currentPlayer, 'B'); assert.equal(after.latestShot, null);
  assert.equal(after.lastAction.type, 'TIMEOUT');
  assert.throws(() => f.game.act({ playerId: 'A', turnId: 1, sequence: 99, type: 'CHARGE' }));
  assert.equal(f.at(20).turn.remainingSeconds, 20);
});
test('linear power starts at zero, half at 2.5s; release uses server time and aim', () => {
  const f = fixture(); f.send('AIM', { angle: 60 });
  assert.equal(f.send('CHARGE').turn.power, 0);
  assert.equal(f.at(2.5).turn.power, 50);
  const s = f.send('RELEASE');
  assert.deepEqual(s.latestShot.input, { angle: 60, power: 50 });
  assert.equal(s.players[0].resource, 80); assert.equal(s.turn.phase, 'flight');
  assert.equal(s.currentPlayer, 'A');
  assert.equal(f.at(2.6).turn.chargeElapsedSeconds, 2.5);
});
test('MAX automatically fires once at exactly 5 seconds without client activity', () => {
  const f = fixture(); f.send('CHARGE');
  assert.equal(f.at(4.999).latestShot, null);
  const s = f.at(5);
  assert.equal(s.latestShot.input.power, 100); assert.equal(s.latestShot.firedAt, 5);
  assert.throws(() => f.send('RELEASE'));
  assert.equal(f.at(5.1).latestShot.id, 1);
});
test('predeadline charge survives; movement and aim stop at deadline; release valid', () => {
  const f = fixture(); f.at(19);
  f.send('HOLD', { move: 1, aim: 1 }); f.send('CHARGE');
  const deadline = f.at(20);
  assert.equal(deadline.turn.phase, 'overtime');
  assert.equal(deadline.players[0].position.x, 5); assert.equal(deadline.turn.angle, 81);
  f.at(21);
  for (const [type, fields] of [['HOLD', { move: 1, aim: -1 }], ['AIM', { angle: 90 }], ['CHARGE', {}]])
    assert.throws(() => f.send(type, fields));
  const shot = f.send('RELEASE');
  assert.equal(shot.latestShot.input.power, 40); assert.equal(shot.latestShot.input.angle, 81);
  assert.equal(shot.latestShot.initial.x, 5);
});
test('overtime MAX and deadline/MAX tie both resolve deterministically', () => {
  for (const start of [15, 19.999]) {
    const f = fixture(); f.at(start); f.send('CHARGE');
    const s = f.at(start + 5);
    assert.equal(s.turn.phase, 'flight'); assert.equal(s.latestShot.input.power, 100);
  }
});
test('flight then damage then effect then next turn; no early client completion', () => {
  const f = fixture(); f.send('CHARGE'); f.at(1.5);
  let s = f.send('RELEASE');
  const impact = s.turn.impactAt, finish = s.turn.resolveUntil;
  assert.equal(s.players[1].hp, 100);
  assert.equal(f.at(impact - 0.0001).currentPlayer, 'A');
  s = f.at(impact); assert.equal(s.players[1].hp, 40); assert.equal(s.turn.phase, 'effect');
  assert.throws(() => f.send('CHARGE'));
  assert.equal(f.at(finish - 0.0001).currentPlayer, 'A');
  s = f.at(finish); assert.equal(s.currentPlayer, 'B');
  assert.equal(s.players[0].nextActionTime, 30);
});
test('continuous movement plus aim: distance cost, not packet count, stop on release', () => {
  for (const repeated of [false, true]) {
    const f = fixture(); f.send('HOLD', { move: 1, aim: 1 });
    for (let i = 1; i <= 10; i++) { f.at(i / 10); if (repeated) f.send('HOLD', { move: 1, aim: 1 }); }
    const s = f.send('HOLD', { move: 0, aim: 0 });
    assert.ok(Math.abs(s.players[0].position.x - 5) < 1e-9);
    assert.ok(Math.abs(s.players[0].resource - 90) < 1e-9);
    assert.ok(Math.abs(s.turn.angle - 81) < 1e-9);
    assert.equal(f.at(2).players[0].position.x, s.players[0].position.x);
  }
});
test('180 degree five-second sweep, direct mouse aim and bounds', () => {
  const f = fixture(); f.send('AIM', { angle: 0 }); f.send('HOLD', { move: 0, aim: 1 });
  assert.equal(f.at(5).turn.angle, 180);
  assert.equal(f.send('AIM', { angle: 123 }).turn.angle, 123);
  assert.throws(() => f.send('AIM', { angle: 181 }));
  assert.throws(() => f.send('AIM', { angle: NaN }));
});
test('resource stops movement; charge reserves fire resource; anchors follow movement', () => {
  const f = fixture(); f.send('CHARGE'); f.send('HOLD', { move: 1, aim: 0 });
  const s = f.at(5);
  assert.equal(s.players[0].resource, 30);
  assert.equal(s.latestShot.initial.x, 25);
  assert.equal(s.players[0].groundContactPoint.x, 25);
  const g = fixture(); g.send('HOLD', { move: 1, aim: 0 });
  assert.equal(g.at(12).players[0].position.x, 50);
  assert.equal(g.at(12).players[0].resource, 0);
  assert.throws(() => g.send('CHARGE'));
});
test('schema injection, stale sequence, wrong actor and snapshot tampering rejected', () => {
  const f = fixture();
  const input = { playerId: 'A', turnId: 1, sequence: 1, type: 'CHARGE' };
  for (const extra of ['power', 'serverNow', 'deadline', 'position', 'damage'])
    assert.throws(() => f.game.act({ ...input, [extra]: 100 }));
  assert.throws(() => f.game.act({ ...input, playerId: 'B' }));
  f.game.act(input); assert.throws(() => f.game.act(input));
  const copy = f.at(0); copy.turn.deadline = 999; copy.players[0].resource = 999;
  assert.equal(f.at(0).turn.deadline, 20); assert.equal(f.at(0).players[0].resource, 100);
});
test('Layer 1 trajectory reused for timed shot: wind and accepted angle/power', () => {
  const f = fixture(); f.send('CHARGE'); f.at(2.75);
  const s = f.send('RELEASE');
  const expected = simulate({ angle: 45, power: 55 }, 0).impact;
  for (const key of ['x', 'y', 't']) assert.ok(Math.abs(s.latestShot.impact[key] - expected[key]) < 1e-10);
});
test('live HTTP prohibits legacy bypass and processes duplicate charge only once', async t => {
  let time = 0;
  const server = createApp({ clock: () => time }); server.listen(0, '127.0.0.1');
  await once(server, 'listening'); t.after(() => new Promise(r => server.close(r)));
  const root = 'http://127.0.0.1:' + server.address().port;
  const post = (path, input) => fetch(root + path, { method: 'POST',
    headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(input) });
  assert.equal((await post('/api/fire', {})).status, 404);
  assert.equal((await post('/api/move', {})).status, 404);
  const input = { playerId: 'A', turnId: 1, sequence: 1, type: 'CHARGE' };
  const results = await Promise.all([post('/api/input', input), post('/api/input', input)]);
  assert.deepEqual(results.map(r => r.status).sort(), [200, 409]);
  time = 5;
  await new Promise(r => setTimeout(r, T.SERVER_TICK_MS * 2));
  const s = await (await fetch(root + '/api/state')).json();
  assert.equal(s.latestShot.input.power, 100); assert.equal(s.players[0].resource, 80);
  assert.equal(s.inputTuning.TURN_INPUT_LIMIT_SEC, 20);
});

test('timed combat preserves HP/elimination/winner and locks finished game after effect', () => {
  const f = fixture();
  // A self-hit twice; intervening turns use ordinary timeout, with no refill.
  let s = f.send('CHARGE'); s = f.send('RELEASE');
  s = f.at(s.turn.resolveUntil);
  assert.equal(s.players[0].hp, 40);
  while (s.currentPlayer !== 'A') s = f.at(s.turn.deadline);
  f.send('CHARGE'); s = f.send('RELEASE');
  const finish = s.turn.resolveUntil;
  s = f.at(s.turn.impactAt);
  assert.equal(s.players[0].hp, 0); assert.equal(s.players[0].eliminated, true);
  assert.equal(s.currentPlayer, 'A'); assert.equal(s.matchState, 'active');
  s = f.at(finish);
  assert.equal(s.winner, 'B'); assert.equal(s.currentPlayer, null);
  assert.equal(s.turn.phase, 'finished'); assert.throws(() => f.send('CHARGE'));
});

test('no-client timeout clock advances continuously without request-driven timing', async t => {
  const server = createApp(); server.listen(0, '127.0.0.1'); await once(server, 'listening');
  t.after(() => new Promise(r => server.close(r)));
  const root = 'http://127.0.0.1:' + server.address().port;
  const initial = await (await fetch(root + '/api/state')).json();
  await new Promise(r => setTimeout(r, 150));
  const later = await (await fetch(root + '/api/state')).json();
  assert.ok(later.turn.remainingSeconds < initial.turn.remainingSeconds);
  assert.equal(later.turn.deadline, initial.turn.deadline);
});
