const $ = id => document.getElementById(id);
let session, view, pollTimer, overlaySide = 'left';
const theme = Object.freeze({ LOBBY: '#fff', ROOM: '#b9f5ff', BATTLE_GLOBAL: '#fff', BATTLE_TEAM_A: '#8fda9b', BATTLE_TEAM_B: '#ff8f8f', WHISPER: '#b9b9c8', SYSTEM: '#d9c982' });
async function request(path, options) { const r = await fetch(path, options); const data = await r.json(); if (!r.ok) throw Error(data.error || 'Server error'); return data; }
function body(data) { return { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) }; }
function targets(select, players) { select.replaceChildren(...players.filter(p => p.playerId !== session.player.playerId).map(p => { const o = document.createElement('option'); o.value = p.playerId; o.textContent = p.displayName + ' (' + p.playerId + ')'; return o; })); select.hidden = false; }
function renderChat(el, messages, battle = false) { el.replaceChildren(...messages.map(m => { const p = document.createElement('p'); p.textContent = '[' + m.channelType + '] ' + m.senderDisplayName + ': ' + m.text; p.style.color = theme[m.channelType === 'BATTLE_TEAM' ? 'BATTLE_TEAM_' + (m.teamId || 'A') : m.channelType] || theme.SYSTEM; return p; })); el.scrollTop = el.scrollHeight; }
function render(next) {
  view = next; $('identity').textContent = session.player.displayName + ' / Player ID ' + session.player.playerId;
  $('rooms').replaceChildren(...next.rooms.map(r => { const p = document.createElement('p'); p.textContent = r.code + ' (' + r.players.length + '/8, ' + r.mode + ')'; return p; }));
  renderChat($('lobby-chat'), next.chat.filter(m => m.channelType === 'LOBBY' || m.channelType === 'WHISPER'));
  const people = next.room?.players ?? next.battle?.players?.map(playerId => ({ playerId, displayName: playerId })) ?? [];
  for (const id of ['lobby-target', 'room-target', 'battle-target']) targets($(id), people);
  if (next.room) { $('room').hidden = false; $('room-code').textContent = next.room.code; $('room-status').textContent = next.room.status + ' / Host ' + next.room.hostId; $('room-players').textContent = next.room.players.map(p => p.displayName + ' [' + (next.room.teams.A.some(x => x.playerId === p.playerId) ? 'A' : 'B') + ']').join(' / '); renderChat($('room-chat'), next.chat.filter(m => m.channelType === 'ROOM' || m.channelType === 'WHISPER')); }
  else $('room').hidden = true;
  $('battle').hidden = !next.battle;
  if (next.battle) renderChat($('battle-overlay'), next.chat.filter(m => ['BATTLE_GLOBAL', 'BATTLE_TEAM', 'WHISPER'].includes(m.channelType)), true);
}
async function refresh() { if (!session) return; try { render(await request('/api/lobby?sessionId=' + encodeURIComponent(session.sessionId))); $('status').textContent = 'Server state updated'; } catch (e) { $('status').textContent = e.message; } pollTimer = setTimeout(refresh, 500); }
async function sendChat(channel, input, box) { const type = $(channel).value; const result = await request('/api/chat', body({ sessionId: session.sessionId, channelType: type, text: $(input).value, targetId: $(box).value || null, roomId: view.room?.roomId, battleId: view.battle?.battleId, teamId: view.room?.teams.A.some(p => p.playerId === session.player.playerId) ? 'A' : 'B' })); $(input).value = ''; render(await request('/api/lobby?sessionId=' + session.sessionId)); return result; }
function toggleWhisper(select, target) { $(select).addEventListener('change', () => { $(target).hidden = $(select).value !== 'WHISPER'; }); }
$('login-form').addEventListener('submit', async e => { e.preventDefault(); try { session = await request('/api/session', body({ displayName: $('display-name').value })); $('login').hidden = true; $('lobby').hidden = false; await refresh(); } catch (x) { $('status').textContent = x.message; } });
$('create').addEventListener('click', async () => { try { await request('/api/rooms', body({ sessionId: session.sessionId, mode: $('mode').value })); await refresh(); } catch (x) { $('status').textContent = x.message; } });
$('join').addEventListener('click', async () => { try { await request('/api/rooms/join', body({ sessionId: session.sessionId, code: $('invite-code').value })); await refresh(); } catch (x) { $('status').textContent = x.message; } });
$('leave').addEventListener('click', async () => { try { await request('/api/rooms/leave', body({ sessionId: session.sessionId })); await refresh(); } catch (x) { $('status').textContent = x.message; } });
$('start').addEventListener('click', async () => { try { await request('/api/rooms/start', body({ sessionId: session.sessionId })); await refresh(); } catch (x) { $('status').textContent = x.message; } });
$('lobby-send').addEventListener('click', () => void sendChat('lobby-channel', 'lobby-text', 'lobby-target').catch(x => $('status').textContent = x.message));
$('room-send').addEventListener('click', () => void sendChat('room-channel', 'room-text', 'room-target').catch(x => $('status').textContent = x.message));
$('battle-send').addEventListener('click', () => void sendChat('battle-channel', 'battle-text', 'battle-target').catch(x => $('status').textContent = x.message));
toggleWhisper('lobby-channel', 'lobby-target'); toggleWhisper('room-channel', 'room-target'); toggleWhisper('battle-channel', 'battle-target');
