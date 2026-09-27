import test from 'node:test';
import assert from 'node:assert/strict';
import { once } from 'node:events';
import { createLobby } from '../server/lobby.js';
import { createApp } from '../server/index.js';

function people(hub, count, prefix = 'P') { return Array.from({ length: count }, (_, i) => hub.login(prefix + (i + 1))); }
test('guest login issues server-only session and player IDs', () => {
  const h = createLobby(); const a = h.login('Alice');
  assert.match(a.sessionId, /^s_/); assert.match(a.player.playerId, /^p_/); assert.equal(a.player.displayName, 'Alice');
  assert.notEqual(a.sessionId, a.player.playerId); assert.throws(() => h.session('p_bad'));
  assert.throws(() => h.login('x'.repeat(33)));
});
test('room invite, capacity, modes, host transfer and leave reassigns teams by join order', () => {
  const h = createLobby(), ps = people(h, 5); const r = h.createRoom(ps[0].sessionId, '2v2');
  assert.equal(r.hostId, ps[0].player.playerId); assert.match(r.code, /^[A-Z0-9]{6}$/);
  h.joinRoom(ps[1].sessionId, r.code); h.joinRoom(ps[2].sessionId, r.code);
  assert.throws(() => h.startRoom(ps[0].sessionId));
  h.leaveRoom(ps[1].sessionId); h.joinRoom(ps[3].sessionId, r.code);
  assert.equal(h.leaveRoom(ps[0].sessionId).hostId, ps[2].player.playerId);
  h.joinRoom(ps[4].sessionId, r.code);
  assert.equal(h.leaveRoom(ps[2].sessionId).hostId, ps[3].player.playerId);
  assert.equal(h.snapshot(ps[3].sessionId).room.teams.A.length, 1);
});
test('start only accepts exact even mode sizes, no NPC, no mid-battle join or leave', () => {
  for (const [mode, count] of [['1v1', 2], ['2v2', 4], ['3v3', 6], ['4v4', 8]]) {
    const h = createLobby(), ps = people(h, count, mode);
    const r = h.createRoom(ps[0].sessionId, mode); for (const p of ps.slice(1)) h.joinRoom(p.sessionId, r.code);
    const battleRoom = h.startRoom(ps[0].sessionId); assert.equal(battleRoom.status, 'battle'); assert.ok(battleRoom.battleId);
    assert.equal(battleRoom.players.length, count); assert.equal(battleRoom.teams.A.length, count / 2);
    assert.equal(battleRoom.teams.B.length, count / 2); assert.throws(() => h.leaveRoom(ps[1].sessionId), /cannot be left/); assert.throws(() => h.joinRoom(h.login('late').sessionId, r.code));
  }
});
test('host disconnect transfers only host and preserves battle', () => {
  const h = createLobby(), ps = people(h, 2); const r = h.createRoom(ps[0].sessionId); h.joinRoom(ps[1].sessionId, r.code); h.startRoom(ps[0].sessionId);
  const state = h.disconnect(ps[0].sessionId); assert.equal(state.battle.status, undefined); assert.equal(state.player.status, 'disconnected');
  const room = h.snapshot(ps[1].sessionId).room; assert.equal(room.hostId, ps[1].player.playerId); assert.equal(room.status, 'battle');
});
test('destroyed, eliminated, disconnected and npc_controlled remain distinct and affect active team winner', () => {
  const h = createLobby(), ps = people(h, 4), r = h.createRoom(ps[0].sessionId, '2v2'); ps.slice(1).forEach(p => h.joinRoom(p.sessionId, r.code)); h.startRoom(ps[0].sessionId);
  assert.equal(h.setBattleStatus(ps[0].sessionId, 'destroyed').player.status, 'destroyed');
  assert.equal(h.setBattleStatus(ps[1].sessionId, 'eliminated').player.status, 'eliminated');
  assert.equal(h.setBattleStatus(ps[3].sessionId, 'disconnected').battle.winnerTeam, 'A');
  const h2 = createLobby(), q = people(h2, 2), r2 = h2.createRoom(q[0].sessionId); h2.joinRoom(q[1].sessionId, r2.code); h2.startRoom(q[0].sessionId);
  assert.equal(h2.setBattleStatus(q[0].sessionId, 'npc_controlled').player.status, 'npc_controlled');
});
test('communication routing matrix never sends team messages to opponent', () => {
  const h = createLobby(), ps = people(h, 4), r = h.createRoom(ps[0].sessionId, '2v2'); ps.slice(1).forEach(p => h.joinRoom(p.sessionId, r.code)); h.startRoom(ps[0].sessionId);
  const b = h.snapshot(ps[0].sessionId).battle;
  const cases = [
    ['BATTLE_GLOBAL', { battleId: b.battleId }, 4],
    ['BATTLE_TEAM', { battleId: b.battleId }, 2],
  ];
  for (const [channelType, extra, expected] of cases) { const m = h.sendChat(ps[0].sessionId, { channelType, text: channelType, ...extra }); assert.equal(m.deliveredTo.length, expected); assert.ok(!m.deliveredTo.includes(ps[3].player.playerId) || channelType === 'BATTLE_GLOBAL'); }
  const lobby = h.login('Lobby'); assert.equal(h.sendChat(lobby.sessionId, { channelType: 'LOBBY', text: 'hello' }).deliveredTo.length, 1);
  const whisper = h.sendChat(ps[0].sessionId, { channelType: 'WHISPER', targetId: lobby.player.playerId, text: 'private' }); assert.deepEqual(new Set(whisper.deliveredTo), new Set([ps[0].player.playerId, lobby.player.playerId]));
});
test('chat short history, length limit and rate limit are server enforced', () => {
  const h = createLobby(), p = h.login('A'); for (let i = 0; i < 5; i++) h.sendChat(p.sessionId, { channelType: 'LOBBY', text: String(i) }); assert.throws(() => h.sendChat(p.sessionId, { channelType: 'LOBBY', text: 'six' }), /rate/); assert.throws(() => h.sendChat(p.sessionId, { channelType: 'LOBBY', text: 'x'.repeat(501) }), /Invalid/);
});
test('HTTP session, room and chat endpoints keep IDs server authoritative', async t => {
  const server = createApp({ layer5: true }); server.listen(0, '127.0.0.1'); await once(server, 'listening'); t.after(() => new Promise(r => server.close(r)));
  const root = 'http://127.0.0.1:' + server.address().port, post = (path, data) => fetch(root + path, { ...({ method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) }) });
  const a = await (await post('/api/session', { displayName: 'Alice', playerId: 'client-choice' })).json(); assert.match(a.player.playerId, /^p_/); assert.notEqual(a.player.playerId, 'client-choice');
  const room = await (await post('/api/rooms', { sessionId: a.sessionId, mode: '1v1' })).json(); assert.ok(room.code); const msg = await (await post('/api/chat', { sessionId: a.sessionId, channelType: 'LOBBY', text: 'should reject in room' })).json(); assert.match(msg.error, /unavailable/);
  assert.equal((await fetch(root + '/api/lobby?sessionId=' + a.sessionId)).status, 200);
});
