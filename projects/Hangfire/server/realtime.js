import { performance } from 'node:perf_hooks';
import { createGame, selectNextPlayer, ActionError } from './game.js';
import { TUNING as P, TURN_TUNING as R, INPUT_TUNING as T } from './tuning.js';
import { simulate } from './projectile.js';
import { syncAnchors, resolveShot, applyDamage, victory } from './collision.js';

const clamp = (v, lo, hi) => Math.max(lo, Math.min(hi, v));
export function createRealtimeGame(wind, { clock = () => performance.now() / 1000 } = {}) {
  const state = createGame(wind).snapshot();
  let now = clock();
  let turnId = 0;
  const actor = () => state.players.find(p => p.id === state.currentPlayer);
  function begin(time) {
    state.turn = { id: ++turnId, startedAt: time, deadline: time + T.TURN_INPUT_LIMIT_SEC,
      phase: 'input', angle: P.DEFAULT_ANGLE, power: 0, move: 0, aim: 0,
      chargeStartedAt: null, lastSequence: -1, movementDistance: 0, resourceUsed: 0 };
  }
  begin(now);
  function end(time, type) {
    const t = state.turn;
    const p = actor();
    const actionCost = (type === 'FIRE' ? R.FIRE_ACTION_COST : T.TIMEOUT_ACTION_COST) +
      t.movementDistance / R.DEFAULT_MOVE_DISTANCE * R.MOVE_ACTION_COST;
    p.nextActionTime = state.logicalTime + actionCost;
    state.lastAction = { type, playerId: p.id, resourceCost: t.resourceUsed, actionCost,
      elapsedSeconds: time - t.startedAt, movementDistance: t.movementDistance,
      logicalTime: state.logicalTime, nextActionTime: p.nextActionTime,
      turnLoadModel: 'Layer 2 compatibility; four-component model not implemented' };
    Object.assign(state, victory(state.players));
    if (state.matchState === 'finished') {
      state.currentPlayer = null; t.phase = 'finished';
    } else {
      const next = selectNextPlayer(state.players);
      state.currentPlayer = next.id; state.logicalTime = next.nextActionTime; begin(time);
    }
    state.revision++;
  }
  function fire(time) {
    const t = state.turn, p = actor();
    t.power = P.POWER_MIN + (P.POWER_MAX - P.POWER_MIN) *
      clamp((time - t.chargeStartedAt) / T.POWER_CHARGE_TO_MAX_SEC, 0, 1);
    state.latestShot = { id: (state.latestShot?.id ?? 0) + 1, playerId: p.id,
      firedAt: time, ...resolveShot(simulate({ angle: t.angle, power: t.power }, wind,
        p.position.x), state.players) };
    p.resource -= R.FIRE_RESOURCE_COST; t.resourceUsed += R.FIRE_RESOURCE_COST;
    t.move = 0; t.aim = 0; t.phase = 'flight';
    t.impactAt = time + state.latestShot.duration;
    t.resolveUntil = t.impactAt + T.IMPACT_EFFECT_SEC;
    state.revision++;
  }
  function integrate(until) {
    const t = state.turn;
    if (t.phase === 'input' && now < t.deadline) {
      const dt = Math.max(0, Math.min(until, t.deadline) - now);
      t.angle = clamp(t.angle + t.aim * (P.ANGLE_MAX - P.ANGLE_MIN) /
        T.AIM_FULL_SWEEP_SEC * dt, P.ANGLE_MIN, P.ANGLE_MAX);
      const p = actor();
      // Reserve shot resource once a charge is accepted; movement cannot invalidate it.
      const available = Math.max(0, p.resource - (t.chargeStartedAt === null ? 0 : R.FIRE_RESOURCE_COST));
      const distance = Math.min(T.MOVE_SPEED_UNITS_PER_SEC * dt, available / R.MOVE_RESOURCE_COST_PER_UNIT);
      const x = clamp(p.position.x + t.move * distance, T.WORLD_MIN_X, T.WORLD_MAX_X);
      const accepted = Math.abs(x - p.position.x), cost = accepted * R.MOVE_RESOURCE_COST_PER_UNIT;
      p.position.x = x; syncAnchors(p); p.resource = Math.max(0, p.resource - cost);
      t.movementDistance += accepted; t.resourceUsed += cost;
    }
    if (t.chargeStartedAt !== null && ['input', 'overtime'].includes(t.phase)) {
      t.power = P.POWER_MIN + (P.POWER_MAX - P.POWER_MIN) *
        clamp((until - t.chargeStartedAt) / T.POWER_CHARGE_TO_MAX_SEC, 0, 1);
    }
    now = until;
  }
  function advance() {
    const target = Math.max(now, clock());
    while (state.matchState !== 'finished') {
      const t = state.turn;
      let eventAt = Infinity, kind;
      if (t.phase === 'input') { eventAt = t.deadline; kind = 'deadline'; }
      if (['input', 'overtime'].includes(t.phase) && t.chargeStartedAt !== null &&
          t.chargeStartedAt + T.POWER_CHARGE_TO_MAX_SEC < eventAt) {
        eventAt = t.chargeStartedAt + T.POWER_CHARGE_TO_MAX_SEC; kind = 'fire';
      }
      if (t.phase === 'flight') { eventAt = t.impactAt; kind = 'impact'; }
      if (t.phase === 'effect') { eventAt = t.resolveUntil; kind = 'end'; }
      if (eventAt > target) break;
      integrate(eventAt);
      if (kind === 'deadline') {
        t.move = 0; t.aim = 0;
        if (t.chargeStartedAt !== null) { t.phase = 'overtime'; state.revision++; }
        else end(eventAt, 'TIMEOUT');
      } else if (kind === 'fire') fire(eventAt);
      else if (kind === 'impact') {
        applyDamage(state.players, state.latestShot.resolution);
        t.phase = 'effect'; state.revision++;
      } else end(eventAt, 'FIRE');
    }
    integrate(target);
  }
  function snapshot() {
    advance();
    const t = state.turn;
    return structuredClone({ ...state, serverNow: now,
      turn: { ...t, elapsedSeconds: now - t.startedAt,
        remainingSeconds: Math.max(0, t.deadline - now),
        chargeElapsedSeconds: t.chargeStartedAt === null ? 0 :
          Math.min(T.POWER_CHARGE_TO_MAX_SEC,
            (['flight', 'effect', 'finished'].includes(t.phase) ? state.latestShot.firedAt : now) - t.chargeStartedAt),
        chargeRatio: t.power / P.POWER_MAX } });
  }
  function act(input) {
    advance();
    const t = state.turn;
    const fields = ['playerId', 'turnId', 'sequence', 'type'];
    if (input?.type === 'HOLD') fields.push('move', 'aim');
    if (input?.type === 'AIM') fields.push('angle');
    if (!input || Array.isArray(input) || Object.keys(input).length !== fields.length ||
        !fields.every(k => Object.hasOwn(input, k)) ||
        !['HOLD', 'AIM', 'CHARGE', 'RELEASE'].includes(input.type)) throw new ActionError('Invalid input fields.');
    if (state.matchState !== 'active' || input.playerId !== state.currentPlayer ||
        input.turnId !== t.id || !Number.isSafeInteger(input.sequence) || input.sequence <= t.lastSequence)
      throw new ActionError('Stale turn, sequence or actor.', 409);
    if (t.phase !== 'input' && !(t.phase === 'overtime' && input.type === 'RELEASE'))
      throw new ActionError('Input window closed.', 409);
    if (input.type === 'HOLD') {
      if (![-1, 0, 1].includes(input.move) || ![-1, 0, 1].includes(input.aim)) throw new ActionError('Invalid direction.');
      t.move = input.move; t.aim = input.aim;
    } else if (input.type === 'AIM') {
      if (!Number.isFinite(input.angle) || input.angle < P.ANGLE_MIN || input.angle > P.ANGLE_MAX)
        throw new ActionError('Invalid aim.');
      t.angle = input.angle;
    } else if (input.type === 'CHARGE') {
      if (t.chargeStartedAt !== null || actor().resource < R.FIRE_RESOURCE_COST)
        throw new ActionError('Already charging or insufficient resource.', 409);
      t.chargeStartedAt = now;
    } else {
      if (t.chargeStartedAt === null) throw new ActionError('No active charge.', 409);
      fire(now);
    }
    t.lastSequence = input.sequence; state.revision++;
    return snapshot();
  }
  return { snapshot, advance, act };
}
