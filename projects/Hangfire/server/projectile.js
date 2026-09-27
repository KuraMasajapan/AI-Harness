import { TUNING as T } from './tuning.js';

export function validateInput(input) {
  if (!input || typeof input !== 'object' || Array.isArray(input) ||
      Object.keys(input).length !== 2 ||
      !Object.hasOwn(input, 'angle') || !Object.hasOwn(input, 'power')) {
    throw new Error('Send only angle and power.');
  }
  for (const [key, min, max] of [
    ['angle', T.ANGLE_MIN, T.ANGLE_MAX], ['power', T.POWER_MIN, T.POWER_MAX],
  ]) {
    if (!Number.isFinite(input[key]) || input[key] < min || input[key] > max) {
      throw new Error(key + ' must be a finite number between ' + min + ' and ' + max);
    }
  }
}

export function validateWind(wind) {
  if (!Number.isFinite(wind) || wind < T.WIND_MIN || wind > T.WIND_MAX) {
    throw new Error('Server WIND must be between ' + T.WIND_MIN + ' and ' + T.WIND_MAX);
  }
  return wind;
}

export function simulate(input, wind, launchX = T.LAUNCH_X) {
  validateInput(input);
  validateWind(wind);
  if (!Number.isFinite(launchX)) throw new Error('Invalid server launch position.');
  const radians = input.angle * Math.PI / 180;
  const speed = input.power * T.PROJECTILE_SPEED_SCALE;
  const vx = speed * Math.cos(radians);
  const vy = speed * Math.sin(radians);
  const duration = (vy + Math.sqrt(vy * vy + 2 * T.GRAVITY *
    (T.LAUNCH_Y - T.GROUND_Y))) / T.GRAVITY;
  const count = Math.ceil(duration / T.PATH_STEP_SECONDS);
  if (count + 1 > T.MAX_PATH_POINTS) throw new Error('Trajectory exceeds path budget.');
  const pointAt = t => ({
    t, x: launchX + vx * t + 0.5 * wind * t * t,
    y: T.LAUNCH_Y + vy * t - 0.5 * T.GRAVITY * t * t,
  });
  // Adjacent points define ordered movement segments for a future collision layer.
  const path = Array.from({ length: count }, (_, i) => pointAt(i * T.PATH_STEP_SECONDS));
  const impact = { ...pointAt(duration), y: T.GROUND_Y };
  path.push(impact);
  return {
    input: { ...input }, wind,
    initial: { x: launchX, y: T.LAUNCH_Y, vx, vy },
    duration, path, impact,
  };
}
