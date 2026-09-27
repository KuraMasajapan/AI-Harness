import { randomUUID } from 'node:crypto';

const MAX_NAME = 32, MAX_TEXT = 500, HISTORY_LIMIT = 100;
const CHANNELS = new Set(['LOBBY', 'ROOM', 'BATTLE_GLOBAL', 'BATTLE_TEAM', 'WHISPER']);
const modes = new Set(['1v1', '2v2', '3v3', '4v4']);
const now = () => Date.now();

function code() { return randomUUID().replaceAll('-', '').slice(0, 6).toUpperCase(); }
function publicPlayer(p) { return { playerId: p.playerId, displayName: p.displayName, status: p.status, roomId: p.roomId, battleId: p.battleId }; }

export class LobbyError extends Error { constructor(message, status = 400) { super(message); this.status = status; } }

export function createLobby() {
  const sessions = new Map(), rooms = new Map(), battles = new Map(), messages = [], rate = new Map();
  const sessionsByPlayer = id => [...sessions.values()].find(s => s.playerId === id);
  const session = id => { const s = sessions.get(id); if (!s) throw new LobbyError('Unknown session.', 401); return s; };
  const room = id => { const r = rooms.get(id); if (!r) throw new LobbyError('Unknown room.', 404); return r; };
  const publicRoom = r => ({ roomId: r.roomId, code: r.code, hostId: r.hostId, mode: r.mode,
    status: r.status, battleId: r.battleId, players: r.players.map(id => publicPlayer(sessionsByPlayer(id))),
    teams: Object.fromEntries(Object.entries(r.teams).map(([k, v]) => [k, v.map(id => publicPlayer(sessionsByPlayer(id)))])) });
  function login(displayName) {
    if (typeof displayName !== 'string' || !displayName.trim() || displayName.trim().length > MAX_NAME)
      throw new LobbyError('displayName is required and must be at most 32 characters.');
    const playerId = 'p_' + randomUUID().replaceAll('-', '').slice(0, 16);
    const sessionId = 's_' + randomUUID().replaceAll('-', '');
    const s = { sessionId, playerId, displayName: displayName.trim(), status: 'connected', roomId: null, battleId: null };
    sessions.set(sessionId, s); return { sessionId, player: publicPlayer(s), state: snapshot(sessionId) };
  }
  function createRoom(sessionId, mode = '1v1') {
    const s = session(sessionId); if (s.roomId) throw new LobbyError('Already in a room.', 409);
    if (!modes.has(mode)) throw new LobbyError('Invalid team mode.');
    const r = { roomId: 'r_' + randomUUID().slice(0, 12), code: code(), hostId: s.playerId,
      mode, status: 'waiting', battleId: null, players: [s.playerId], teams: { A: [s.playerId], B: [] }, createdAt: now() };
    s.roomId = r.roomId; rooms.set(r.roomId, r); return publicRoom(r);
  }
  function joinRoom(sessionId, inviteCode) {
    const s = session(sessionId); if (s.roomId) throw new LobbyError('Already in a room.', 409);
    const r = [...rooms.values()].find(x => x.code === String(inviteCode).toUpperCase());
    if (!r) throw new LobbyError('Unknown room code.', 404);
    if (r.status !== 'waiting' || r.players.length >= 8) throw new LobbyError('Room is not joinable.', 409);
    r.players.push(s.playerId); r.teams[r.players.length % 2 === 1 ? 'A' : 'B'].push(s.playerId); s.roomId = r.roomId;
    return publicRoom(r);
  }
  function leaveRoom(sessionId) {
    const s = session(sessionId); if (!s.roomId) throw new LobbyError('Not in a room.', 409);
    const r = room(s.roomId); if (r.status === 'battle') throw new LobbyError('Battle cannot be left.', 409);
    r.players = r.players.filter(id => id !== s.playerId); for (const key of ['A', 'B']) r.teams[key] = r.teams[key].filter(id => id !== s.playerId);
    s.roomId = null; if (r.hostId === s.playerId) r.hostId = r.players[0] ?? null;
    if (!r.players.length) rooms.delete(r.roomId); else { r.teams = { A: [], B: [] }; r.players.forEach((id, i) => r.teams[i % 2 ? 'B' : 'A'].push(id)); }
    return r.players.length ? publicRoom(r) : { roomId: null };
  }
  function startRoom(sessionId) {
    const s = session(sessionId), r = room(s.roomId); if (r.hostId !== s.playerId) throw new LobbyError('Only host can start.', 403);
    const required = Number(r.mode[0]) * 2;
    if (r.players.length !== required || ![2, 4, 6, 8].includes(r.players.length) || r.teams.A.length !== r.teams.B.length)
      throw new LobbyError('Battle requires 2, 4, 6 or 8 players with equal teams.', 409);
    r.status = 'battle'; r.battleId = 'b_' + randomUUID().slice(0, 12);
    const b = { battleId: r.battleId, roomId: r.roomId, players: [...r.players], activePlayers: [...r.players], teams: structuredClone(r.teams), winnerTeam: null, startedAt: now() };
    battles.set(b.battleId, b); for (const p of r.players) { const x = [...sessions.values()].find(y => y.playerId === p); x.battleId = b.battleId; x.status = 'connected'; }
    return publicRoom(r);
  }
  function disconnect(sessionId) {
    const s = session(sessionId); s.status = 'disconnected';
    if (s.roomId) { const r = room(s.roomId); if (r.hostId === s.playerId) r.hostId = r.players.find(id => id !== s.playerId) ?? null; }
    if (s.battleId) { const b = battles.get(s.battleId); if (b) b.activePlayers = b.activePlayers.filter(id => id !== s.playerId); }
    return snapshot(sessionId);
  }
  function setBattleStatus(sessionId, status) {
    const s = session(sessionId); if (!['connected', 'disconnected', 'destroyed', 'eliminated', 'npc_controlled'].includes(status)) throw new LobbyError('Invalid battle status.');
    if (!s.battleId) throw new LobbyError('Player is not in a battle.', 409);
    s.status = status; const b = battles.get(s.battleId); if (status !== 'connected') b.activePlayers = b.activePlayers.filter(id => id !== s.playerId);
    const active = team => b.activePlayers.some(id => b.teams[team].includes(id));
    b.winnerTeam = active('A') && !active('B') ? 'A' : active('B') && !active('A') ? 'B' : null;
    return { battle: structuredClone(b), player: publicPlayer(s) };
  }
  function recipientIds(m) {
    if (m.channelType === 'LOBBY') return [...sessions.values()].filter(s => s.status === 'connected' && !s.roomId).map(s => s.playerId);
    if (m.channelType === 'ROOM') return [...room(m.roomId).players].filter(id => sessionsByPlayer(id)?.status === 'connected');
    if (m.channelType === 'BATTLE_GLOBAL') return [...battles.get(m.battleId).players].filter(id => sessionsByPlayer(id)?.status === 'connected');
    if (m.channelType === 'BATTLE_TEAM') return (battles.get(m.battleId).teams[m.teamId] ?? []).filter(id => sessionsByPlayer(id)?.status === 'connected');
    if (m.channelType === 'WHISPER') return [m.senderId, m.targetId].filter((x, i, a) => x && a.indexOf(x) === i && sessionsByPlayer(x)?.status === 'connected');
    throw new LobbyError('Invalid channel.');
  }
  function sendChat(sessionId, input) {
    const s = session(sessionId), type = input?.channelType;
    if (!CHANNELS.has(type) || typeof input.text !== 'string' || !input.text.trim() || input.text.length > MAX_TEXT) throw new LobbyError('Invalid chat message.');
    const last = rate.get(s.playerId) ?? []; const recent = last.filter(t => now() - t < 10000); if (recent.length >= 5) throw new LobbyError('Chat rate limit.', 429); recent.push(now()); rate.set(s.playerId, recent);
    if (type === 'LOBBY' && s.roomId) throw new LobbyError('Lobby chat is unavailable inside a room.', 409);
    if (type === 'ROOM' && !s.roomId) throw new LobbyError('Room chat requires a room.', 409);
    if (['BATTLE_GLOBAL', 'BATTLE_TEAM'].includes(type) && !s.battleId) throw new LobbyError('Battle chat requires a battle.', 409);
    const b = s.battleId ? battles.get(s.battleId) : null;
    const derivedTeam = (b && Object.entries(b.teams).find(([, ids]) => ids.includes(s.playerId))?.[0]) ?? null;
    const m = { channelType: type, senderId: s.playerId, senderDisplayName: s.displayName, targetId: input.targetId ?? null,
      roomId: type === 'ROOM' ? s.roomId : null, battleId: b ? b.battleId : null, teamId: type === 'BATTLE_TEAM' ? derivedTeam : null, text: input.text.trim(), timestamp: new Date().toISOString(), deliveredTo: [] };
    if (type === 'WHISPER' && !sessionsByPlayer(m.targetId)) throw new LobbyError('Unknown whisper target.');
    const recipients = recipientIds(m); m.deliveredTo = recipients; messages.push(m); while (messages.length > HISTORY_LIMIT) messages.shift(); return m;
  }
  function chatFor(sessionId) {
    const s = session(sessionId); return messages.filter(m => recipientIdsSafe(m).includes(s.playerId));
  }
  function recipientIdsSafe(m) { try { return recipientIds(m); } catch { return []; } }
  function snapshot(sessionId) {
    const s = session(sessionId); return { player: publicPlayer(s), rooms: [...rooms.values()].filter(r => r.status === 'waiting').map(publicRoom), room: s.roomId ? publicRoom(room(s.roomId)) : null, battle: s.battleId ? battles.get(s.battleId) : null, chat: chatFor(sessionId) };
  }
  return { login, createRoom, joinRoom, leaveRoom, startRoom, disconnect, setBattleStatus, sendChat, snapshot, session, limits: { MAX_NAME, MAX_TEXT, history: HISTORY_LIMIT } };
}
