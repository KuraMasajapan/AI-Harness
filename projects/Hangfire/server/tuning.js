// AI-selected provisional values; world units, seconds, degrees. Not final balance.
const WIND_MAX = 12;
export const TUNING = Object.freeze({
  WIND_MAX,
  WIND_MIN: -WIND_MAX,
  GRAVITY: 36,
  POWER_MIN: 0,
  POWER_MAX: 100,
  PROJECTILE_SPEED_SCALE: 1.5,
  ANGLE_MIN: 0,
  ANGLE_MAX: 180,
  DEFAULT_ANGLE: 45,
  DEFAULT_POWER: 55,
  LAUNCH_X: 0,
  LAUNCH_Y: 8,
  GROUND_Y: 0,
  PATH_STEP_SECONDS: 1 / 30,
  MAX_PATH_POINTS: 1024,
});

// Layer 2 provisional values only. Layer 1 values above remain unchanged.
export const TURN_TUNING = Object.freeze({
  RESOURCE_MAX: 100,
  FIRE_RESOURCE_COST: 20,
  MOVE_RESOURCE_COST_PER_UNIT: 2,
  FIRE_ACTION_COST: 30,
  MOVE_ACTION_COST: 10,
  MOVE_MIN_DISTANCE: 1,
  MOVE_MAX_DISTANCE: 20,
  DEFAULT_MOVE_DISTANCE: 5,
  PLAYER_A_X: TUNING.LAUNCH_X,
  PLAYER_B_X: 60,
});

// Layer 3 provisional values; independent of visual size and Layer 1/2 tuning.
export const HIT_TUNING = Object.freeze({
  HP_MAX: 100,
  HIT_POINT_X: 0,
  HIT_POINT_Y: 4,
  DIRECT_HIT_RADIUS: 2,
  BLAST_RADIUS: 18,
  DIRECT_HIT_DAMAGE: 60,
  BLAST_DAMAGE_MAX: 40,
  DAMAGE_FALLOFF: 1,
});

// Layer 4 input seeds. No Gear efficiency or future Turn Load coefficients.
export const INPUT_TUNING = Object.freeze({
  TURN_INPUT_LIMIT_SEC: 20,
  POWER_CHARGE_TO_MAX_SEC: 5,
  AIM_FULL_SWEEP_SEC: 5,
  MOVE_SPEED_UNITS_PER_SEC: 5,
  WORLD_MIN_X: -100,
  WORLD_MAX_X: 200,
  IMPACT_EFFECT_SEC: 0.3,
  SERVER_TICK_MS: 50,
  CLIENT_POLL_MS: 100,
  TIMEOUT_ACTION_COST: TURN_TUNING.MOVE_ACTION_COST,
});
