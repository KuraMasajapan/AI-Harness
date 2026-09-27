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
  const minX = Math.min(0, ...points.map(p => p.x));
  const maxX = Math.max(100, ...points.map(p => p.x));
  const maxY = Math.max(50, ...points.map(p => p.y));
  const scale = Math.min((canvas.width - 80) / (maxX - minX), (canvas.height - 80) / maxY);
  const xy = p => [40 + (p.x - minX) * scale, canvas.height - 40 - p.y * scale];
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.strokeStyle = '#647c8f';
  ctx.beginPath(); ctx.moveTo(0, xy({ x: 0, y: state.tuning.GROUND_Y })[1]);
  ctx.lineTo(canvas.width, xy({ x: 0, y: state.tuning.GROUND_Y })[1]); ctx.stroke();
  ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(...xy(points[0]), 5, 0, Math.PI * 2); ctx.fill();
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
$('controls').addEventListener('submit', async event => {
  event.preventDefault();
  $('fire').disabled = true;
  $('status').textContent = 'Serverで計算中…';
  try {
    const result = await request('/api/fire', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ angle: Number($('angle').value), power: Number($('power').value) }),
    });
    present(result, true);
    $('status').textContent = 'Server結果を受信しました。';
  } catch (error) { $('status').textContent = '発射失敗: ' + error.message; }
  finally { $('fire').disabled = false; }
});
try {
  state = await request('/api/state');
  for (const key of ['angle', 'power']) {
    const input = $(key);
    input.min = state.tuning[key.toUpperCase() + '_MIN'];
    input.max = state.tuning[key.toUpperCase() + '_MAX'];
    input.value = state.tuning['DEFAULT_' + key.toUpperCase()];
    input.disabled = false;
  }
  showWind(state.wind);
  if (state.latestShot) present(state.latestShot, false); else draw();
  $('fire').disabled = false;
  $('status').textContent = '接続済み。AngleとPowerを設定して発射できます。';
} catch (error) { $('status').textContent = '接続失敗: ' + error.message + '。再読み込みしてください。'; }
