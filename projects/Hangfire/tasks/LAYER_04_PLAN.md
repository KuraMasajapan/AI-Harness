# Layer 4 pre-flight / plan

- Base: development 58999c9; Human GO received. Layer 1–3 baseline 25/25 PASS.
- Read ASTRA_START Resume/loop, PROJECT, Layer 1–3 checkpoints, Layer 4 task,
  TUNING_POLICY, TURN_LOAD_MODEL, architecture/collision and existing implementation.
- Current Task: LAYER_04_INPUT_TIMER.md. Adopted 20 seconds supersedes old 15-second labels.
- Reuse Node HTTP/Canvas and projectile/collision; no dependencies.
- Server monotonic clock controls input deadline, linear charge, continuous movement/aim,
  projectile flight and an explicit short effect duration before next-player selection.
- Strict turn ID + ordered input sequence prevents stale/replayed input. No client clock,
  power, position or result accepted. Old discrete HTTP actions disabled in live mode.
- Preserve legacy core as regression fixture (explicit server-side test option only).
- Adopted ranges: power 0..100 and aim 0..180. Existing values within ranges retain trajectories.
- Provisional Layer 4 seeds: shared movement 5 units/sec, world -100..200,
  impact effect 0.3 sec, server tick 50ms, client poll 100ms.
- Resource remains 2/unit and FIRE20. Logical move cost scales by accepted distance
  using old default 5-unit MOVE cost10; timeout base cost10, FIRE base cost30.
  This compatibility boundary is not the future four-component Turn Load formula.
- Record elapsed time, distance and resource consumed for later tuning; no recovery,
  Weapon/Item load, Gear cooling, Scout/Heavy efficiency, rooms or Layer 5 work.
- Validate fake-clock boundaries + live HTTP timer + legacy regression + Browser controls.
