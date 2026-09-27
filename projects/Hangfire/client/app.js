const $ = id => document.getElementById(id);
const canvas = $('field');
const ctx = canvas.getContext('2d');
let state;
let shot;
let animation = 0;

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
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.strokeStyle = '#647c8f';
  ctx.beginPath(); ctx.moveTo(0, xy({ x: 0, y: state.tuning.GROUND_Y })[1]);
  ctx.lineTo(canvas.width, xy({ x: 0, y: state.tuning.GROUND_Y })[1]); ctx.stroke();
  ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(...xy(points[0]), 5, 0, Math.PI * 2); ctx.fill();
  ctx.textAlign = 'center';
  for (const player of state.players) {
    const [x, y] = xy(player.position);
    ctx.fillStyle = player.id === state.currentPlayer ? '#6cdbef' : '#aaa';
    ctx.fillRect(x - 5, y - 10, 10, 10);
    ctx.fillText(player.id, x, y - 16);
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
    ctx.fillStyle = '#ffd27d';
    ctx.textAlign = shot.impact.x > (minX + maxX) / 2 ? 'right' : 'left';
    ctx.fillText('Impact X=' + shot.impact.x.toFixed(2), ...xy({ x: shot.impact.x, y: 5 }));
  }
}
function present(result, animate) {
  cancelAnimationFrame(animation);
  shot = result;
  showWind(result.wind);
  $('impact').textContent = 'Server着弾 #' + result.id + ': X=' +
    result.impact.x.toFixed(3) + ', Y=' + result.impact.y.toFixed(3) +
    ' / 飛行時間 ' + result.duration.toFixed(3) + 's';
  if (!animate) return draw();
  const start = performance.now();
  const frame = now => {
    const elapsed = (now - start) / 1000;
    draw(elapsed);
    if (elapsed < shot.duration) animation = requestAnimationFrame(frame);
  };
  animation = requestAnimationFrame(frame);
}
function setBusy(busy) {
  for (const id of ['fire', 'move-left', 'move-right', 'actor', 'refresh']) $(id).disabled = busy;
}
function showState(next, animate = false) {
  const newShot = next.latestShot && next.latestShot.id !== shot?.id;
  state = next;
  $('turn').textContent = 'Current Player: ' + state.currentPlayer +
    ' / logicalTime: ' + state.logicalTime + ' / revision: ' + state.revision;
  $('players').replaceChildren(...state.players.map(player => {
    const row = document.createElement('tr');
    for (const value of [player.id, player.position.x, player.resource, player.nextActionTime]) {
      const cell = document.createElement('td'); cell.textContent = value; row.append(cell);
    }
    return row;
  }));
  const action = state.lastAction;
  $('last-action').textContent = action ? action.playerId + ' ' + action.type +
    ': Resource -' + action.resourceCost + ' / Action Cost ' + action.actionCost +
    ' / 次回 ' + action.nextActionTime : '行動: なし';
  // Hotseat follows the server-selected actor after every response.
  $('actor').value = state.currentPlayer;
  showWind(state.wind);
  if (state.latestShot) present(state.latestShot, animate && newShot);
  else {
    cancelAnimationFrame(animation); shot = null;
    $('impact').textContent = '着弾: 未発射';
    draw();
  }
}
async function act(path, fields) {
  const input = { playerId: $('actor').value, expectedRevision: state.revision, ...fields };
  setBusy(true);
  $('status').textContent = 'Serverで処理中…';
  try {
    showState(await request(path, {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(input),
    }), true);
    $('status').textContent = 'Serverが行動を受理しました。';
  } catch (error) {
    let message = '行動拒否 / 通信失敗: ' + error.message;
    try { showState(await request('/api/state')); }
    catch { message += '。状態取得にも失敗しました。再接続後に状態を更新してください。'; }
    $('status').textContent = message;
  } finally { setBusy(false); }
}
$('controls').addEventListener('submit', event => {
  event.preventDefault();
  void act('/api/fire', { angle: Number($('angle').value), power: Number($('power').value) });
});
$('movement').addEventListener('submit', event => {
  event.preventDefault();
  void act('/api/move', { direction: event.submitter?.value, amount: Number($('amount').value) });
});
async function refresh() {
  setBusy(true);
  try {
    showState(await request('/api/state'));
    for (const key of ['angle', 'power']) {
      const input = $(key);
      input.min = state.tuning[key.toUpperCase() + '_MIN'];
      input.max = state.tuning[key.toUpperCase() + '_MAX'];
      if (!input.value) input.value = state.tuning['DEFAULT_' + key.toUpperCase()];
      input.disabled = false;
    }
    $('amount').min = state.turnTuning.MOVE_MIN_DISTANCE;
    $('amount').max = state.turnTuning.MOVE_MAX_DISTANCE;
    if (!$('amount').value) $('amount').value = state.turnTuning.DEFAULT_MOVE_DISTANCE;
    $('amount').disabled = false;
    $('status').textContent = '接続済み。Server状態を表示しています。';
    setBusy(false);
  } catch (error) {
    $('status').textContent = '接続失敗: ' + error.message;
    $('refresh').disabled = false;
  }
}
$('refresh').addEventListener('click', refresh);
await refresh();
