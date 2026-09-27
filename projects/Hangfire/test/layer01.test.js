import test from 'node:test';
import assert from 'node:assert/strict';
import { once } from 'node:events';
import { simulate } from '../server/projectile.js';
import { TUNING as T } from '../server/tuning.js';
import { createApp } from '../server/index.js';

const ballistic = ({ resolution, ...shot }) => shot;
const input = { angle: T.DEFAULT_ANGLE, power: T.DEFAULT_POWER };
test('same input and zero wind give identical full trajectories', () => {
  assert.deepEqual(simulate(input, 0), simulate(input, 0));
});
test('angle, power, left and right wind change impact as intended', () => {
  const baseline = simulate(input, 0);
  assert.notEqual(simulate({ ...input, angle: 65 }, 0).impact.x, baseline.impact.x);
  assert.ok(simulate({ ...input, power: 75 }, 0).impact.x > baseline.impact.x);
  assert.ok(simulate(input, T.WIND_MAX).impact.x > baseline.impact.x);
  assert.ok(simulate(input, T.WIND_MIN).impact.x < baseline.impact.x);
});
test('bounded, finite, ordered segments finish exactly on flat ground at all extremes', () => {
  for (const angle of [T.ANGLE_MIN, 45, 90, T.ANGLE_MAX]) {
    for (const power of [T.POWER_MIN, T.POWER_MAX]) {
      for (const wind of [T.WIND_MIN, 0, T.WIND_MAX]) {
        const shot = simulate({ angle, power }, wind);
        assert.ok(shot.path.length <= T.MAX_PATH_POINTS);
        assert.deepEqual(shot.path.at(-1), shot.impact);
        assert.equal(shot.impact.y, T.GROUND_Y);
        shot.path.forEach((p, i) => {
          assert.ok(Number.isFinite(p.x) && Number.isFinite(p.y) && Number.isFinite(p.t));
          assert.ok(p.y >= T.GROUND_Y);
          if (i) assert.ok(p.t > shot.path[i - 1].t);
        });
      }
    }
  }
});
test('zero-wind range agrees with independent flat-ground physical identity', () => {
  const shot = simulate(input, 0);
  assert.ok(Math.abs(shot.impact.x - (shot.initial.x + shot.initial.vx * shot.duration)) < 1e-10);
  assert.ok(Math.abs(shot.initial.y + shot.initial.vy * shot.duration -
    T.GRAVITY * shot.duration ** 2 / 2 - T.GROUND_Y) < 1e-10);
});
test('invalid inputs and wind fail explicitly', () => {
  for (const value of [null, [], {}, { ...input, wind: 5 }, { ...input, impact: {} },
    { angle: '45', power: 55 }, { angle: NaN, power: 55 },
    { angle: Infinity, power: 55 }, { angle: -1, power: 55 },
    { angle: 45, power: T.POWER_MAX + 1 }]) {
    assert.throws(() => simulate(value, 0));
  }
  for (const wind of [NaN, Infinity, T.WIND_MAX + 1]) assert.throws(() => createApp({ wind }));
});
test('HTTP authority, rejection, static client and server-state persistence', async t => {
  const server = createApp({ wind: T.WIND_MAX });
  server.listen(0, '127.0.0.1');
  await once(server, 'listening');
  t.after(() => new Promise(resolve => server.close(resolve)));
  const root = 'http://127.0.0.1:' + server.address().port;
  const get = async () => (await fetch(root + '/api/state')).json();
  const fire = async body => {
    const current = await get();
    return fetch(root + '/api/fire', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ playerId: current.currentPlayer, expectedRevision: current.revision, ...body }),
    });
  };
  const first = await get();
  assert.equal(first.wind, T.WIND_MAX);
  assert.equal(first.latestShot, null);
  const result = await fire(input);
  assert.equal(result.status, 200);
  const shot = (await result.json()).latestShot;
  assert.deepEqual(ballistic(shot), { id: 1, playerId: 'A', ...simulate(input, T.WIND_MAX) });
  first.wind = T.WIND_MIN;
  shot.impact.x = -999;
  shot.path[0].x = -999;
  assert.deepEqual(ballistic((await get()).latestShot), { id: 1, playerId: 'A', ...simulate(input, T.WIND_MAX) });
  for (const key of ['wind', 'impact', 'path', 'initial', 'tuning']) {
    assert.equal((await fire({ ...input, [key]: -999 })).status, 400);
  }
  assert.equal((await fire({ ...input, power: 100000 })).status, 400);
  assert.equal((await fetch(root + '/api/fire', {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{',
  })).status, 400);
  assert.equal((await fetch(root + '/api/fire', {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: ' '.repeat(2048),
  })).status, 413);
  assert.equal((await fetch(root + '/api/fire', { method: 'POST', body: '{}' })).status, 415);
  assert.equal((await fetch(root + '/api/wind', { method: 'POST' })).status, 404);
  assert.equal((await get()).latestShot.id, 1);
  const again = (await (await fire(input)).json()).latestShot;
  const currentOrigin = (await get()).players.find(p => p.id === again.playerId).position.x;
  assert.deepEqual(again.impact, simulate(input, T.WIND_MAX, currentOrigin).impact);
  for (const path of ['/', '/app.js', '/style.css']) {
    assert.equal((await fetch(root + path)).status, 200);
  }
  assert.equal((await fetch(root + '/server/tuning.js')).status, 404);
});
test('HTTP integration for zero, left and right server wind', async t => {
  const impacts = [];
  for (const wind of [T.WIND_MIN, 0, T.WIND_MAX]) {
    const server = createApp({ wind });
    server.listen(0, '127.0.0.1');
    await once(server, 'listening');
    t.after(() => new Promise(resolve => server.close(resolve)));
    const result = await fetch('http://127.0.0.1:' + server.address().port + '/api/fire', {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ playerId: 'A', expectedRevision: 0, ...input }),
    });
    const shot = (await result.json()).latestShot;
    assert.equal(shot.wind, wind);
    impacts.push(shot.impact.x);
  }
  assert.ok(impacts[0] < impacts[1] && impacts[1] < impacts[2]);
  console.log('HTTP wind left/zero/right impact X:', impacts);
});
