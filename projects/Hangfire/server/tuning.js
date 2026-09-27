// AI-selected provisional values; world units, seconds, degrees. Not final balance.
const WIND_MAX = 12;
export const TUNING = Object.freeze({
  WIND_MAX,
  WIND_MIN: -WIND_MAX,
  GRAVITY: 36,
  POWER_MIN: 10,
  POWER_MAX: 100,
  PROJECTILE_SPEED_SCALE: 1.5,
  ANGLE_MIN: 5,
  ANGLE_MAX: 175,
  DEFAULT_ANGLE: 45,
  DEFAULT_POWER: 55,
  LAUNCH_X: 0,
  LAUNCH_Y: 8,
  GROUND_Y: 0,
  PATH_STEP_SECONDS: 1 / 30,
  MAX_PATH_POINTS: 1024,
});
