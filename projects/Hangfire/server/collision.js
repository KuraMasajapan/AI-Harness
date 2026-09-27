import { TUNING, HIT_TUNING as H } from './tuning.js';

export function syncAnchors(player) {
  player.visualOrigin = { ...player.position };
  player.groundContactPoint = { ...player.position };
  player.hitPoint = { x: player.position.x + H.HIT_POINT_X, y: player.position.y + H.HIT_POINT_Y };
  player.directHitRadius = H.DIRECT_HIT_RADIUS;
  return player;
}

// Earliest fraction of the segment intersecting the closed circle; catches tunneling.
export function segmentCircle(a, b, center, radius) {
  const dx = b.x - a.x, dy = b.y - a.y;
  const ox = a.x - center.x, oy = a.y - center.y;
  const c = ox * ox + oy * oy - radius * radius;
  if (c <= 0) return 0;
  const aa = dx * dx + dy * dy;
  if (aa === 0) return null;
  const bb = 2 * (ox * dx + oy * dy);
  const discriminant = bb * bb - 4 * aa * c;
  if (discriminant < 0) return null;
  const fraction = (-bb - Math.sqrt(discriminant)) / (2 * aa);
  return fraction >= 0 && fraction <= 1 ? fraction : null;
}

export function blastDamage(distance) {
  if (distance >= H.BLAST_RADIUS) return 0;
  return Math.ceil(H.BLAST_DAMAGE_MAX * (1 - distance / H.BLAST_RADIUS) ** H.DAMAGE_FALLOFF);
}

export function resolveShot(shot, players) {
  const alive = players.filter(p => !p.eliminated).sort((a, b) => a.id < b.id ? -1 : a.id > b.id ? 1 : 0);
  let collision = null, path = shot.path;
  for (let i = 1; i < path.length && !collision; i++) {
    const a = path[i - 1], b = path[i];
    let fraction = Infinity, kind = null, playerId = null;
    if (b.y <= TUNING.GROUND_Y) {
      fraction = a.y <= TUNING.GROUND_Y ? 0 : (a.y - TUNING.GROUND_Y) / (a.y - b.y);
      kind = 'terrain';
    }
    for (const player of alive) {
      const candidate = segmentCircle(a, b, player.hitPoint, player.directHitRadius);
      if (candidate !== null && candidate < fraction) {
        fraction = candidate; kind = 'direct'; playerId = player.id;
      }
    }
    if (kind) {
      const point = fraction === 1 ? { ...b } : { t: a.t + (b.t - a.t) * fraction,
        x: a.x + (b.x - a.x) * fraction, y: a.y + (b.y - a.y) * fraction };
      if (kind === 'terrain') point.y = TUNING.GROUND_Y;
      collision = { kind, playerId, point };
      path = fraction === 0 ? path.slice(0, i) : [...path.slice(0, i), point];
    }
  }
  if (!collision) throw new Error('Projectile path must terminate at a collision.');
  const damage = alive.map(player => {
    const distance = Math.hypot(player.hitPoint.x - collision.point.x, player.hitPoint.y - collision.point.y);
    const direct = collision.playerId === player.id;
    const amount = direct ? H.DIRECT_HIT_DAMAGE : blastDamage(distance);
    return { playerId: player.id, distance, amount, kind: direct ? 'direct' : amount > 0 ? 'splash' : 'miss' };
  });
  return {
    ...shot, path, impact: collision.point, duration: collision.point.t,
    resolution: { collision, explosionCenter: { ...collision.point }, blastRadius: H.BLAST_RADIUS,
      result: collision.kind === 'direct' ? 'direct' : damage.some(d => d.amount > 0) ? 'splash' : 'miss',
      damage },
  };
}

export function applyDamage(players, resolution) {
  // All damage is calculated from the pre-explosion state, then applied as a batch.
  for (const player of players) {
    const damage = resolution.damage.find(d => d.playerId === player.id)?.amount ?? 0;
    player.hp = Math.max(0, player.hp - damage);
    player.eliminated = player.hp === 0;
  }
}

export function victory(players) {
  const survivors = players.filter(p => !p.eliminated);
  return survivors.length <= 1
    ? { matchState: 'finished', winner: survivors[0]?.id ?? null }
    : { matchState: 'active', winner: null };
}
