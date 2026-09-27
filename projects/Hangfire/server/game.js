import { TUNING, TURN_TUNING as T } from './tuning.js';
import { simulate, validateInput, validateWind } from './projectile.js';

export class ActionError extends Error {
  constructor(message, status = 400) { super(message); this.status = status; }
}

// Deterministic tie-break independent of insertion order or locale.
export function selectNextPlayer(players) {
  return [...players].sort((a, b) => a.nextActionTime - b.nextActionTime ||
    (a.id < b.id ? -1 : a.id > b.id ? 1 : 0))[0];
}

export function createGame(wind) {
  validateWind(wind);
  let state = {
    wind, revision: 0, logicalTime: 0, currentPlayer: 'A',
    players: [
      { id: 'A', position: { x: T.PLAYER_A_X, y: TUNING.GROUND_Y },
        resource: T.RESOURCE_MAX, nextActionTime: 0 },
      { id: 'B', position: { x: T.PLAYER_B_X, y: TUNING.GROUND_Y },
        resource: T.RESOURCE_MAX, nextActionTime: 0 },
    ],
    latestShot: null, lastAction: null,
  };
  const snapshot = () => structuredClone(state);
  return {
    snapshot,
    act(type, input) {
      const fields = type === 'FIRE' ? ['playerId', 'expectedRevision', 'angle', 'power'] :
        type === 'MOVE' ? ['playerId', 'expectedRevision', 'direction', 'amount'] : null;
      if (!fields || !input || typeof input !== 'object' || Array.isArray(input) ||
          Object.keys(input).length !== fields.length ||
          !fields.every(key => Object.hasOwn(input, key))) {
        throw new ActionError('Send only the required action input fields.');
      }
      if (!Number.isSafeInteger(input.expectedRevision) || input.expectedRevision < 0) {
        throw new ActionError('Invalid expectedRevision.');
      }
      const actor = state.players.find(p => p.id === input.playerId);
      if (!actor) throw new ActionError('Unknown player.');
      if (actor.id !== state.currentPlayer) throw new ActionError('Not current player.', 409);
      if (input.expectedRevision !== state.revision) throw new ActionError('Stale action. Refresh state.', 409);
      let resourceCost, actionCost, newX = actor.position.x, shot = null;
      if (type === 'FIRE') {
        validateInput({ angle: input.angle, power: input.power });
        resourceCost = T.FIRE_RESOURCE_COST;
        actionCost = T.FIRE_ACTION_COST;
      } else {
        if (!['left', 'right'].includes(input.direction) ||
            !Number.isInteger(input.amount) || input.amount < T.MOVE_MIN_DISTANCE ||
            input.amount > T.MOVE_MAX_DISTANCE) {
          throw new ActionError('MOVE needs left/right and an integer amount within server limits.');
        }
        resourceCost = input.amount * T.MOVE_RESOURCE_COST_PER_UNIT;
        actionCost = T.MOVE_ACTION_COST;
        newX += (input.direction === 'left' ? -1 : 1) * input.amount;
      }
      if (actor.resource < resourceCost) throw new ActionError('Insufficient resource.', 409);
      if (type === 'FIRE') {
        shot = {
          id: (state.latestShot?.id ?? 0) + 1, playerId: actor.id,
          ...simulate({ angle: input.angle, power: input.power }, wind, actor.position.x),
        };
      }
      // All validation/calculation completed before the single authoritative commit.
      // No await here: competing HTTP actions are checked against the committed revision.
      const next = snapshot();
      const updated = next.players.find(p => p.id === actor.id);
      updated.position.x = newX;
      updated.resource -= resourceCost;
      updated.nextActionTime = state.logicalTime + actionCost;
      if (shot) next.latestShot = shot;
      next.lastAction = { type, playerId: actor.id, resourceCost, actionCost,
        logicalTime: state.logicalTime, nextActionTime: updated.nextActionTime };
      const selected = selectNextPlayer(next.players);
      next.currentPlayer = selected.id;
      next.logicalTime = selected.nextActionTime;
      next.revision++;
      state = next;
      return snapshot();
    },
  };
}
