import test from 'node:test';
import assert from 'node:assert/strict';
import { once } from 'node:events';
import { createGame, selectNextPlayer } from '../server/game.js';
import { createApp } from '../server/index.js';
import { segmentCircle, resolveShot, blastDamage, applyDamage, victory, syncAnchors } from '../server/collision.js';
import { HIT_TUNING as H } from '../server/tuning.js';
import { simulate } from '../server/projectile.js';

const request = (game, angle = 45, power = 30) => ({
  playerId: game.snapshot().currentPlayer, expectedRevision: game.snapshot().revision, angle, power,
});
const fire = (game, angle, power) => game.act('FIRE', request(game, angle, power));
const hit = state => state.latestShot.resolution;
const target = (id, x, y, radius = 1) => ({ id, hitPoint: { x, y }, directHitRadius: radius, hp: 100, eliminated: false });
function unchanged(game, type, input, pattern) {
  const before = game.snapshot();
  assert.throws(() => game.act(type, input), pattern);
  assert.deepEqual(game.snapshot(), before);
}

test('segment circle detects fast crossings, tangency, start inside and zero-length safely', () => {
  const a = { x: -10, y: 0 }, b = { x: 10, y: 0 };
  assert.equal(segmentCircle(a, b, { x: 0, y: 0 }, 1), .45);
  assert.equal(segmentCircle(a, b, { x: 0, y: 1 }, 1), .5);
  assert.equal(segmentCircle(a, b, { x: 0, y: 2 }, 1), null);
  assert.equal(segmentCircle({ x: 0, y: 0 }, b, { x: 0, y: 0 }, 1), 0);
  assert.equal(segmentCircle(a, a, { x: 0, y: 0 }, 1), null);
  assert.equal(segmentCircle(a, b, { x: 20, y: 0 }, 1), null);
});
test('earliest gear/terrain contact and deterministic gear tie, not array order', () => {
  const path = [{ t: 0, x: 0, y: 10 }, { t: 1, x: 10, y: -10 }];
  const behindGround = resolveShot({ path }, [target('B', 8, -6)]);
  assert.equal(behindGround.resolution.collision.kind, 'terrain');
  assert.equal(behindGround.impact.x, 5);
  assert.equal(behindGround.impact.y, 0);
  const beforeGround = resolveShot({ path }, [target('B', 2, 6)]);
  assert.equal(beforeGround.resolution.collision.playerId, 'B');
  assert.ok(beforeGround.impact.t < .5);
  assert.deepEqual(beforeGround.path.at(-1), beforeGround.impact);
  const tied = resolveShot({ path }, [target('B', 2, 6), target('A', 2, 6)]);
  assert.equal(tied.resolution.collision.playerId, 'A');
  const noDeadCollision = resolveShot({ path }, [{ ...target('A', 2, 6), eliminated: true }]);
  assert.equal(noDeadCollision.resolution.result, 'miss');
});
test('known trajectory hits B and truncates at first contact; resource unchanged by hit', () => {
  const game = createGame(0);
  const next = fire(game);
  assert.equal(hit(next).result, 'direct');
  assert.equal(hit(next).collision.playerId, 'B');
  assert.equal(next.players[1].hp, H.HP_MAX - H.DIRECT_HIT_DAMAGE);
  assert.equal(next.players[0].hp, H.HP_MAX);
  assert.equal(next.players[0].resource, 80);
  assert.ok(next.latestShot.duration < simulate({ angle: 45, power: 30 }, 0).duration);
  assert.equal(hit(next).damage.find(d => d.playerId === 'B').kind, 'direct');
});
test('nearby ground impact splashes by hitPoint distance; blast edge/outside gives zero', () => {
  const next = fire(createGame(0), 45, 28);
  assert.equal(hit(next).collision.kind, 'terrain');
  assert.equal(hit(next).result, 'splash');
  const damage = hit(next).damage.find(d => d.playerId === 'B');
  assert.ok(damage.amount > 0 && damage.amount < H.BLAST_DAMAGE_MAX);
  assert.equal(damage.distance, Math.hypot(60 - next.latestShot.impact.x, 4));
  assert.equal(blastDamage(0), H.BLAST_DAMAGE_MAX);
  assert.equal(blastDamage(H.BLAST_RADIUS), 0);
  assert.equal(blastDamage(H.BLAST_RADIUS + 1), 0);
  assert.ok(blastDamage(H.BLAST_RADIUS / 4) > blastDamage(H.BLAST_RADIUS / 2));
  const miss = fire(createGame(0), 45, 55);
  assert.equal(hit(miss).result, 'miss');
  assert.ok(hit(miss).damage.every(d => d.amount === 0));
});
test('self damage is not exempt; damage batch can eliminate both with draw result', () => {
  const next = fire(createGame(0), 90, 10);
  assert.equal(hit(next).collision.playerId, 'A');
  assert.equal(next.players[0].hp, H.HP_MAX - H.DIRECT_HIT_DAMAGE);
  const players = [target('A', 0, 4), target('B', 2, 4)];
  players.forEach(p => { p.hp = 1; });
  const resolved = resolveShot({ path: [{ t: 0, x: 0, y: 8 }, { t: 1, x: 0, y: 0 }] }, players);
  assert.ok(resolved.resolution.damage.every(d => d.amount > 0));
  applyDamage(players, resolved.resolution);
  assert.ok(players.every(p => p.hp === 0 && p.eliminated));
  assert.deepEqual(victory(players), { matchState: 'finished', winner: null });
  assert.equal(selectNextPlayer(players), undefined);
});
test('HP clamp, elimination, surviving winner, finished and eliminated action rejection', () => {
  const game = createGame(0);
  fire(game); fire(game, 45, 55);
  const next = fire(game);
  assert.equal(next.players[1].hp, 0);
  assert.equal(next.players[1].eliminated, true);
  assert.equal(next.winner, 'A');
  assert.equal(next.matchState, 'finished');
  assert.equal(next.currentPlayer, null);
  assert.equal(selectNextPlayer(next.players).id, 'A');
  for (const playerId of ['A', 'B']) {
    for (const type of ['FIRE', 'MOVE']) {
      const fields = type === 'FIRE' ? { angle: 45, power: 30 } : { direction: 'right', amount: 1 };
      unchanged(game, type, { playerId, expectedRevision: next.revision, ...fields }, /finished|eliminated/);
    }
  }
});
test('self elimination selects the opponent as winner', () => {
  const game = createGame(0);
  fire(game, 90, 10); fire(game, 45, 55);
  const next = fire(game, 90, 10);
  assert.equal(next.players[0].hp, 0);
  assert.equal(next.winner, 'B');
});
test('anchors follow MOVE; visual change alone does not change collision or damage', () => {
  const game = createGame(0);
  const moved = game.act('MOVE', { playerId: 'A', expectedRevision: 0, direction: 'left', amount: 5 });
  assert.equal(moved.players[0].hitPoint.x, -5 + H.HIT_POINT_X);
  assert.equal(moved.players[0].groundContactPoint.x, -5);
  const players = createGame(0).snapshot().players;
  const shot = simulate({ angle: 45, power: 30 }, 0);
  const original = resolveShot(shot, players);
  players[1].visualOrigin = { x: 999, y: 999 };
  assert.deepEqual(resolveShot(shot, players), original);
  assert.notStrictEqual(syncAnchors(players[0]).hitPoint, players[0].visualOrigin);
});
test('new state injection and stale fire reject without HP/shot/resource changes', () => {
  const game = createGame(0);
  for (const key of ['damage', 'hp', 'directHit', 'hitPoint', 'directHitRadius',
    'explosionCenter', 'blastDistance', 'winner', 'eliminated', 'matchState']) {
    unchanged(game, 'FIRE', { ...request(game), [key]: 999 }, /fields/);
    unchanged(game, 'MOVE', { playerId: 'A', expectedRevision: 0, direction: 'right', amount: 1, [key]: 999 }, /fields/);
  }
  const stale = request(game);
  fire(game); fire(game, 45, 55);
  unchanged(game, 'FIRE', stale, /Stale/);
});
test('HTTP duplicate hit commits damage once, client result injection rejected, winner locked', async t => {
  const server = createApp({ legacyTestMode: true });
  server.listen(0, '127.0.0.1'); await once(server, 'listening');
  t.after(() => new Promise(resolve => server.close(resolve)));
  const root = 'http://127.0.0.1:' + server.address().port;
  const get = async () => (await fetch(root + '/api/state')).json();
  const post = body => fetch(root + '/api/fire', { method: 'POST',
    headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
  const attack = { playerId: 'A', expectedRevision: 0, angle: 45, power: 30 };
  const results = await Promise.all([post(attack), post(attack)]);
  assert.deepEqual(results.map(r => r.status).sort(), [200, 409]);
  let before = await get();
  assert.equal(before.players[1].hp, 40);
  assert.equal(before.revision, 1);
  for (const key of ['hp', 'damage', 'winner', 'eliminated', 'directHit', 'explosionCenter', 'blastDistance']) {
    assert.equal((await post({ playerId: 'B', expectedRevision: 1, angle: 45, power: 55, [key]: 999 })).status, 400);
    assert.deepEqual(await get(), before);
  }
  await post({ playerId: 'B', expectedRevision: 1, angle: 45, power: 55 });
  await post({ ...attack, expectedRevision: 2 });
  before = await get();
  assert.equal(before.winner, 'A');
  assert.equal(before.matchState, 'finished');
  assert.equal((await post({ ...attack, expectedRevision: 3 })).status, 409);
  assert.deepEqual(await get(), before);
});
