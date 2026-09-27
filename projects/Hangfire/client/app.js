const $ = id => document.getElementById(id);
const canvas = $('field');
const ctx = canvas.getContext('2d');
let state;
let shot;
let projection;
let sequence = 0;
let queue = Promise.resolve();
const held = new Set();
let dragging = false;

async function request(path, options) {
  const response = await fetch(path, { ...options, signal: AbortSignal.timeout(8000) });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || 'Server error');
  return data;
}
function showWind(wind) {
  $('wind').textContent = 'Wind: ' + (wind > 0 ? '→ 右' : wind < 0 ? '← 左' : '無風') +
    ' / 強さ ' + Math.abs(wind) + ' (Server)';
}
function draw(elapsed = Infinity) {
  const points = shot?.path ?? [{ x: state.tuning.LAUNCH_X, y: state.tuning.LAUNCH_Y }];
  const minX = Math.min(0, ...points.map(p => p.x), ...state.players.map(p => p.position.x));
  const maxX = Math.max(100, ...points.map(p => p.x), ...state.players.map(p => p.position.x));
  const maxY = Math.max(50, ...points.map(p => p.y));
  const scale = Math.min((canvas.width - 80) / (maxX - minX), (canvas.height - 80) / maxY);
  const xy = p => [40 + (p.x - minX) * scale, canvas.height - 40 - p.y * scale];
  projection = { xy, scale };
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.strokeStyle = '#647c8f';
  ctx.beginPath(); ctx.moveTo(0, xy({ x: 0, y: state.tuning.GROUND_Y })[1]);
  ctx.lineTo(canvas.width, xy({ x: 0, y: state.tuning.GROUND_Y })[1]); ctx.stroke();
  ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(...xy(points[0]), 5, 0, Math.PI * 2); ctx.fill();
  ctx.textAlign = 'center';
  for (const player of state.players) {
    const [x, y] = xy(player.visualOrigin);
    ctx.fillStyle = player.eliminated ? '#6b4f50' : player.id === state.currentPlayer ? '#6cdbef' : '#aaa';
    ctx.fillRect(x - 5, y - 10, 10, 10);
    ctx.fillText(player.id, x, y - 16);
    if (player.id === state.currentPlayer) {
      const a = state.turn.angle * Math.PI / 180;
      ctx.strokeStyle = '#fff'; ctx.beginPath(); ctx.moveTo(x, y - 7);
      ctx.lineTo(x + Math.cos(a) * 22, y - 7 - Math.sin(a) * 22); ctx.stroke();
    }
    if ($('dev-hit').checked) {
      const center = xy(player.hitPoint);
      ctx.strokeStyle = '#ff8696';
      ctx.beginPath(); ctx.arc(...center, player.directHitRadius * scale, 0, Math.PI * 2); ctx.stroke();
      ctx.fillRect(center[0] - 1, center[1] - 1, 2, 2);
    }
  }
  if (!shot) return;
  ctx.strokeStyle = '#6cdbef'; ctx.lineWidth = 2; ctx.beginPath();
  ctx.moveTo(...xy(points[0]));
  let current = points[0];
  for (let i = 1; i < points.length; i++) {
    const next = points[i];
    if (next.t > elapsed) {
      const alpha = Math.max(0, (elapsed - current.t) / (next.t - current.t));
      current = { x: current.x + (next.x - current.x) * alpha,
        y: current.y + (next.y - current.y) * alpha };
      ctx.lineTo(...xy(current)); break;
    }
    current = next; ctx.lineTo(...xy(current));
  }
  ctx.stroke();
  ctx.fillStyle = '#ffd27d'; ctx.beginPath(); ctx.arc(...xy(current), 5, 0, Math.PI * 2); ctx.fill();
  if (elapsed >= shot.duration) {
    if (state.turn.phase === 'effect') {
      ctx.fillStyle = '#ffbf6680'; ctx.beginPath();
      ctx.arc(...xy(shot.impact), 18, 0, Math.PI * 2); ctx.fill();
    }
    if ($('dev-hit').checked && shot.resolution) {
      const center = xy(shot.resolution.explosionCenter);
      ctx.strokeStyle = '#d2ac56';
      ctx.beginPath(); ctx.arc(...center, shot.resolution.blastRadius * scale, 0, Math.PI * 2); ctx.stroke();
      ctx.fillStyle = '#ff8696';
      ctx.fillRect(center[0] - 3, center[1] - 3, 6, 6);
    }
    ctx.fillStyle = '#ffd27d';
    ctx.textAlign = shot.impact.x > (minX + maxX) / 2 ? 'right' : 'left';
    ctx.fillText('Impact X=' + shot.impact.x.toFixed(2), ...xy({ x: shot.impact.x, y: 5 }));
  }
}

function showState(next) {
  if (state && next.serverNow < state.serverNow) return;
  if (state?.turn.id !== next.turn.id) { held.clear(); dragging = false; sequence = 0; }
  state = next; shot = state.latestShot;
  sequence = Math.max(sequence, state.turn.lastSequence);
  const t = state.turn;
  $('match').textContent = 'Match: ' + state.matchState +
    (state.matchState === 'finished' ? ' / Winner: ' + (state.winner ?? 'Draw') : '');
  $('turn').textContent = 'Current Player: ' + (state.currentPlayer ?? '—') +
    ' / 残り ' + t.remainingSeconds.toFixed(1) + ' 秒 / ' + t.phase;
  $('power').value = t.power;
  $('power').max = state.tuning.POWER_MAX;
  $('readout').textContent = 'Aim ' + t.angle.toFixed(1) + '° / Power ' +
    t.power.toFixed(1) + (t.chargeStartedAt !== null && ['input', 'overtime'].includes(t.phase) ? ' / CHARGING' : '');
  $('health').textContent = state.players.map(p => p.id + ' HP ' + p.hp +
    (p.eliminated ? ' [eliminated]' : '')).join(' / ');
  $('players').replaceChildren(...state.players.map(p => {
    const row = document.createElement('tr');
    for (const value of [p.id, p.position.x.toFixed(2), p.resource.toFixed(2), p.nextActionTime.toFixed(2)]) {
      const cell = document.createElement('td'); cell.textContent = value; row.append(cell);
    }
    return row;
  }));
  const hit = shot?.resolution;
  $('hit-result').textContent = hit && t.phase !== 'flight' ? hit.result + ' / ' +
    hit.damage.map(d => d.playerId + ': ' + d.amount).join(' / ') : 'Hit: —';
  $('impact').textContent = shot ? 'Server着弾 #' + shot.id + ' X=' + shot.impact.x.toFixed(3) : '着弾: 未発射';
  showWind(state.wind);
  $('dev-state').hidden = !$('dev-hit').checked;
  if (! $('dev-state').hidden) $('dev-state').textContent = JSON.stringify({
    inputTuning: state.inputTuning, projectileTuning: state.tuning,
    turnTuning: state.turnTuning, hitTuning: state.hitTuning,
    aimSpeedDegPerSec: (state.tuning.ANGLE_MAX - state.tuning.ANGLE_MIN) / state.inputTuning.AIM_FULL_SWEEP_SEC,
    movementEfficiency: 'common; Gear differences deferred',
    serverNow: state.serverNow, turn: t, players: state.players,
    logicalTime: state.logicalTime, revision: state.revision, lastAction: state.lastAction,
    resolution: shot?.resolution, turnLoad: 'not implemented (Layer 2 compatibility)'
  }, null, 2);
  draw(shot && t.phase === 'flight' ? state.serverNow - shot.firedAt : Infinity);
}
function send(type, fields = {}) {
  if (!state) return;
  const input = { playerId: state.currentPlayer, turnId: state.turn.id,
    sequence: ++sequence, type, ...fields };
  queue = queue.then(async () => {
    try {
      showState(await request('/api/input', { method: 'POST',
        headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(input) }));
      $('status').textContent = '接続済み / Server入力受理';
    } catch (error) {
      $('status').textContent = '入力拒否 / 通信失敗: ' + error.message;
    }
  });
}
const moveValue = () => Number(held.has('KeyD')) - Number(held.has('KeyA'));
const aimValue = () => Number(held.has('ArrowUp')) - Number(held.has('ArrowDown'));
function hold() { send('HOLD', { move: moveValue(), aim: aimValue() }); }
document.addEventListener('keydown', e => {
  if (!['Space', 'KeyA', 'KeyD', 'ArrowUp', 'ArrowDown'].includes(e.code) ||
      ['INPUT', 'BUTTON', 'SELECT', 'TEXTAREA'].includes(e.target.tagName)) return;
  e.preventDefault();
  if (e.repeat || held.has(e.code) || state?.turn.phase !== 'input') return;
  held.add(e.code);
  if (e.code === 'Space') send('CHARGE'); else hold();
});
document.addEventListener('keyup', e => {
  if (!held.has(e.code)) return;
  e.preventDefault(); held.delete(e.code);
  if (e.code === 'Space') send('RELEASE'); else hold();
});
function releaseControls() {
  const charge = held.has('Space');
  held.clear(); dragging = false;
  if (state?.turn.phase === 'input') hold();
  if (charge) send('RELEASE');
}
window.addEventListener('blur', releaseControls);
document.addEventListener('visibilitychange', () => { if (document.hidden) releaseControls(); });
function canvasPoint(e) {
  const rect = canvas.getBoundingClientRect();
  return [(e.clientX - rect.left) * canvas.width / rect.width,
    (e.clientY - rect.top) * canvas.height / rect.height];
}
let lastMouseAt = 0;
function mouseAim(e) {
  const p = state.players.find(p => p.id === state.currentPlayer);
  if (!p || state.turn.phase !== 'input') return;
  const [x, y] = canvasPoint(e), [px, py] = projection.xy(p.visualOrigin);
  const angle = Math.max(0, Math.min(180, Math.atan2(py - 7 - y, x - px) * 180 / Math.PI));
  send('AIM', { angle });
}
canvas.addEventListener('pointerdown', e => {
  if (e.button !== 0 || state?.turn.phase !== 'input') return;
  const p = state.players.find(p => p.id === state.currentPlayer);
  const [x, y] = canvasPoint(e), [px, py] = projection.xy(p.visualOrigin);
  if (Math.abs(x - px) > 14 || Math.abs(y - (py - 5)) > 16) return;
  dragging = true; canvas.setPointerCapture(e.pointerId); mouseAim(e);
});
canvas.addEventListener('pointermove', e => {
  if (dragging && performance.now() - lastMouseAt >= state.inputTuning.SERVER_TICK_MS) {
    lastMouseAt = performance.now(); mouseAim(e);
  }
});
canvas.addEventListener('pointerup', e => { if (dragging) mouseAim(e); dragging = false; });
canvas.addEventListener('pointercancel', () => { dragging = false; });
$('dev-hit').addEventListener('change', () => { if (state) showState(state); });
async function poll() {
  try {
    showState(await request('/api/state'));
    if ($('status').textContent === 'Serverへ接続しています…') $('status').textContent = '接続済み / Server状態';
  }
  catch (error) { $('status').textContent = '接続失敗: ' + error.message; }
  setTimeout(poll, state?.inputTuning.CLIENT_POLL_MS ?? 100);
}
await poll();
