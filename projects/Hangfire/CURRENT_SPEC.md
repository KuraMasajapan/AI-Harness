# Hangfire CURRENT SPEC

Status: CURRENT SOURCE OF TRUTH  
Project: Hangfire  
Branch target: development  
Created from Human specification review through Q232  
Purpose: Consolidate the current gameplay rules before further Codex implementation.

> This document is the current gameplay specification checkpoint.
> When an older Hangfire document conflicts with this file, treat this file as the newer decision unless a later Human-approved specification explicitly supersedes it.
> Tuning values marked TEMPORARY are not final balance values.

---

## 0. Status labels

- **CURRENT**: approved current rule.
- **TEMPORARY**: approved direction with provisional numeric value or tuning.
- **FUTURE**: intended extension, not part of current beta implementation.
- **NOT IMPLEMENTED**: specified behavior that may not exist in the current code yet.
- **SUPERSEDED**: older rule that must not be used as the current design.

---

# 1. Battle modes

## 1.1 TEAM — CURRENT

- Maximum 8 players.
- Supported formats: 1v1 / 2v2 / 3v3 / 4v4.
- Red Team and Green Team.
- Teams must be numerically balanced before battle can start.
- Friendly Fire is always ON.
- A single destroyed/eliminated player does not end the battle.
- Battle ends when one team has no remaining active Gear.
- If all remaining sides are eliminated by the same resolved event, result can be DRAW.

## 1.2 FFA — CURRENT

- 2–8 players.
- Odd player counts are allowed.
- No team assignment.
- Every other participant is an enemy.
- Last surviving player wins.
- If no survivor remains after one fully resolved event, result is DRAW.

---

# 2. Room and battle start

## 2.1 Room state — CURRENT

Room contains:
- Gear selection.
- RANDOM Gear selection.
- TEAM assignment when TEAM mode is active.
- Item Storage access.
- READY.
- Fullscreen control.
- Map selection.
- Battle Mode selection.
- START by Room Master.

Gear selection is visible to other players in real time.

## 2.2 READY — CURRENT

While READY:
- Gear cannot be changed.
- Item loadout cannot be changed.
- Team cannot be changed.
- Player must unready before changing those values.

If Room Master changes Map or Battle Mode:
- All READY states reset.

## 2.3 Battle start — CURRENT

Battle does not auto-start when everyone becomes READY.

Requirements:
- All players READY.
- TEAM: valid equal team counts.
- FFA: 2–8 players.
- Room Master presses START.

---

# 3. Spawn

## 3.1 Spawn candidates — CURRENT

- Each map defines about 12 fixed spawn candidate positions.
- Battle start selects the required number of candidates randomly.
- TEAM does not intentionally alternate or cluster red/green spawn positions.
- FFA uses the same random candidate selection principle.
- Runtime minimum-distance checking is not required.
- Safe spacing is a map-design responsibility when spawn candidates are authored.

---

# 4. Phase and Turn system

## 4.1 Phase model — CURRENT

Hangfire uses a Phase-based variable turn-order system.

Within one Phase:
- Each active surviving player receives one Turn.
- A player destroyed or eliminated before their pending Turn is immediately removed from the Phase and loses that Turn.
- When every remaining player in the Phase has acted once, the Phase ends.

At Phase end:
- Each player's completed Turn Load determines the ordering of the next Phase.
- Lower Turn Load acts earlier.
- Equal Turn Load keeps the previous relative order.

This permits effective consecutive actions across a Phase boundary.

Example:
- Phase 1: A → B → C → D
- D records the lowest Turn Load.
- Phase 2 begins: D → A → C → B
- D effectively acts twice in succession across the Phase boundary.

## 4.2 First Phase order — CURRENT

FFA:
- Random player order.

TEAM:
- Team slots alternate Red / Green / Red / Green...
- Order inside each team is random.

After the first Phase:
- Team alternation restriction is removed.
- Turn Load alone determines the next Phase order.

## 4.3 SUPERSEDED

The following interpretation is not current:
- Continuously selecting the globally smallest nextActionTime after every individual Turn with no Phase boundary.
- Allowing one player to take a second action inside the same Phase before all other active players have acted.

The current rule is:
- One action per active player per Phase.
- Reorder only for the next Phase.

---

# 5. Turn Load

## 5.1 Purpose — CURRENT

Turn Load represents how heavy the player's completed Turn was.

Core components:
- Elapsed Time Cost.
- Movement Resource consumed.
- Weapon Turn Cost.
- Item Turn Cost.

Conceptually:

Turn Load = time component + movement component + weapon component + item component

Exact weights and curve are tuning values, not fixed here.

## 5.2 Effects — CURRENT

Lower Turn Load:
- Earlier position in the next Phase.
- Higher next-turn Resource recovery.

Higher Turn Load:
- Later position in the next Phase.
- Lower next-turn Resource recovery.
- Recovery may reach zero above a tuning threshold.

Early Skip is intended to produce a low-load Turn and strong recovery/initiative benefit.

## 5.3 Player display — CURRENT

Normal player UI:
- Show only the local player's Turn Load.
- Do not show other players' Turn Load.
- Do not show the live changing Turn Load during the Turn.
- At Turn end, show the final confirmed Turn Load.
- Keep that value visible until the player's next Turn begins.
- Clear/reset the displayed prior value at the beginning of the next Turn.

Display name:
- **Turn Load**

DEV mode:
- Show all players' values.
- Show component breakdowns.
- Show intermediate calculations.
- Show tuning weights and derived values.

## 5.4 Tuning — TEMPORARY

The exact formula, weights, ordering scale, recovery curve, and zero-recovery threshold are intentionally provisional.

Implementation rule:
- Start with reasonable seed values.
- Expose them in DEV.
- Tune through playtesting.

---

# 6. Resource

## 6.1 Capacity — CURRENT

- All standard Gear share the same maximum Resource.
- Maximum Resource = 200.

Gear identity is not created by different maximum capacities.

## 6.2 Battle start — CURRENT / TEMPORARY

- Every player begins with Resource = 0.
- Immediately before each player's first Turn, perform a first recovery.
- First recovery is currently approximately +35.
- Therefore every player begins their first action under the same initial Resource rule.

Initial recovery value +35 is TEMPORARY and tunable.

## 6.3 Later recovery — CURRENT

From the second personal Turn onward:
- Recovery is based on the player's previous Turn Load.
- Light Turn → larger recovery.
- Heavy Turn → smaller recovery.
- Heavy enough Turn → recovery can be zero.
- Clamp to Resource max 200.

## 6.4 Shared Resource — CURRENT

The same Resource pool is used for:
- Movement.
- Primary Weapon.
- Secondary Weapon.
- Special Weapon.

Items do not consume Resource.

Weapon cost relationship:
- Primary < Secondary < Special.

Special Weapon has no separate energy gauge.
Its use condition is sufficient shared Resource.

## 6.5 Insufficient weapon Resource — CURRENT

A weapon remains selectable even when Resource is insufficient.

If Fire/Charge is attempted without enough Resource:
- No charge starts.
- No projectile is fired.
- Short muzzle smoke effect.
- Failure sound such as "pshh".
- No Resource consumed.
- Turn does not end.
- The failed attempt itself does not stop Time Cost.
- Player may still move, aim, switch weapon, or Skip afterward.

Selected weapon's required Resource should be visually indicated on the Resource gauge.
Movement is allowed to consume through that displayed reservation zone down to zero.

## 6.6 SUPERSEDED

- MAX Resource 100.
- Fixed +20 recovery each Turn.
- Cap 100.

Those are old temporary implementation values and must not be treated as current design.

---

# 7. Turn timer and action finalization

## 7.1 Timer — CURRENT

Normal Turn input window:
- 20 seconds.

At 20 seconds:
- If no Power Charge is already active, force Turn end with no automatic shot.
- If Charge began before the deadline, the player may finish that active Charge and release/fire.
- After timeout during that existing Charge:
  - no movement,
  - no aim change,
  - no item use,
  - no new charge.

## 7.2 Time Cost stop point — CURRENT

Time Cost runs until the action that finalizes the Turn.

Examples:
- Weapon: stops at actual firing moment.
- Large Heal: stops when used because it ends Turn.
- Teleport projectile: stops at actual firing moment.
- Small Heal / Shield: use does not stop Time Cost because Turn continues.
- Skip: finalizes Turn immediately.

---

# 8. Controls

## 8.1 Fixed shortcuts — CURRENT

- F1: Primary Weapon
- F2: Secondary Weapon
- F3: Special Weapon
- F5: Item slot 1
- F6: Item slot 2
- F7: Item slot 3
- F8: Item slot 4
- F9: Skip / Turn End
- F12: Fullscreen toggle

F4 / F10 / F11 remain free for future use.

Item keys immediately use the item; they are not item-preselection keys.

---

# 9. Aim and facing

## 9.1 Aim — CURRENT

- Keyboard Aim uses a constant angular speed.
- Aim speed is common across standard Gear.
- No acceleration from long key hold.
- Barrel stops at its Gear-specific local aim limit.
- Aim does not automatically move the Gear to gain more angle.

Aim and facing are generally adjustable even when it is another player's Turn.

Other-player Turn:
- Movement unavailable.
- Keyboard Aim available.
- Facing left/right available.
- Weapon selection F1–F3 available.
- Fire unavailable.
- Item use unavailable.
- Skip unavailable.

Aim movement/facing changes are visible to other players in real time.
Enemy weapon selection itself remains hidden.

## 9.2 Facing — CURRENT

- Right input sets Gear facing right.
- Left input sets Gear facing left.
- On the player's own Turn, the same input also moves the Gear.
- On another player's Turn, movement is disabled but facing still changes.
- Facing change itself costs no Resource and no Turn Load.
- During own Turn, any actual movement caused by the input consumes normal movement Resource.
- Facing flips immediately with no turning animation.

## 9.3 Mouse Aim — CURRENT

- Aim Circle is shown for the local player during that player's own Turn.
- Mouse drag on the Aim Circle changes aim.
- Mouse Aim is unavailable when the Aim Circle is not shown.
- Keyboard Aim remains available regardless of Aim Circle visibility.

---

# 10. Gear posture and barrel geometry

## 10.1 Standard Gear posture — CURRENT

Standard Gear follows terrain slope.

The Gear body angle is estimated from the ground contact profile and local terrain.
Barrel local aim range is defined relative to the Gear body, so terrain posture affects world firing angle.

Final firing direction is derived from:
- Gear terrain posture.
- Left/right facing.
- Local barrel angle.

Changing facing mirrors the barrel range.

This makes movement and terrain posture part of aiming strategy.

## 10.2 Barrel pivot — CURRENT

Standard Gear:
- Barrel rotates around a Gear-defined pivot.
- Pivot follows body rotation and left/right facing.
- Gear can have different barrel length and visual geometry.
- Barrel length changes actual Muzzle position and is a legitimate Gear characteristic.

Future Gear may use nonstandard articulation.

## 10.3 Muzzle — CURRENT / IMPORTANT

Projectile origin is always the actual Muzzle at the barrel tip.

Never spawn normal weapon projectiles from the Gear Core when a visible barrel muzzle exists.

Muzzle world position must include:
- Gear world position.
- Gear posture.
- Left/right facing.
- Barrel pivot.
- Local barrel angle.
- Barrel length.

## 10.4 Barrel vs terrain — CURRENT

The barrel itself has no Terrain collision.

Therefore:
- Barrel may visually pass through terrain while aiming.
- Aim is not blocked by terrain.
- Only the Muzzle position matters when projectile creation begins.

If Muzzle is inside white Terrain Mask:
- Projectile is created at that Muzzle location.
- Immediate terrain collision / underground explosion may occur.

If Muzzle has passed through terrain and is already in black empty space:
- Projectile starts from that empty-space Muzzle location normally.
- Terrain between Gear Core and Muzzle is not retroactively tested.

This intentionally prioritizes gameplay over realism.

---

# 11. Gear Core and collision model

## 11.1 Shared Foot Core — CURRENT

Standard Gear share a common conceptual Foot Core:
- Located around the bottom-center / foot-center region.
- Acts as the main local origin for ground interaction and damage-distance logic.

Visible Gear image bounds are not the collision bounds.

## 11.2 Separate collision purposes — CURRENT

Do not force one geometric shape to serve every purpose.

Use the same Foot Core origin but separate roles:

1. Ground Contact Profile:
   - Short horizontal contact bar / support sampling structure.

2. Projectile Direct-Hit region:
   - Small circular hit area around the shared Core concept.
   - Common size for standard Gear.

3. Explosion Damage:
   - Distance from explosion center to Gear Core.
   - Not distance to sprite edge.

Standard Gear do not gain smaller/larger projectile hit regions merely because the art is visually smaller/larger.

---

# 12. Ground Contact Profile

## 12.1 Standard profile — CURRENT

Standard Gear use a common contact-bar design.

- Horizontal bar centered at Foot Core.
- Bar length independent of sprite width.
- Same standard dimensions for standard Gear.
- Future special Gear may override the movement/ground-contact profile.

## 12.2 Central support zone — CURRENT

Do not use a single pixel as support truth.

Around Foot Core, use a small central support zone:
- Evaluate terrain occupancy in the zone.
- If occupancy meets a threshold, Gear is supported.
- If central support fails, Gear falls.

The support zone avoids jitter from tiny mask irregularities.

The exact zone width and occupancy threshold are tuning values.

## 12.3 Edge support — CURRENT

- One side of the contact bar may be over empty space.
- If central support is still valid, Gear remains supported.
- Gear may stand on a very narrow or visually precarious piece of terrain.
- No separate minimum terrain width is required.
- This is intentional gameplay: preserving tiny footholds can matter.

## 12.4 Terrain slope estimate — CURRENT

For standard Gear:
- Sample representative left/right ground heights across the contact-bar region.
- Approximate the supporting terrain as one slope.
- Use that slope to rotate the Gear body.
- Do not chase every 1-pixel terrain irregularity.

If one side lacks useful terrain:
- Fall back to the remaining side plus center region for a simple slope estimate.
- Do not automatically force body angle to 0° merely because one side hangs over a ledge.

Start simple; add filtering only if real playtesting shows visible instability.

---

# 13. Slope movement

## 13.1 Standard limits — TEMPORARY

Initial tuning:
- 0° to 60° inclusive: climb and descend.
- Over 60° and under 85°: descend only.
- 85° or more: cannot maintain ground contact; enter falling state.

These thresholds are provisional DEV-tunable values.

Implementation may use a small hysteresis around the falling threshold to prevent state chatter, but the visible gameplay rule above remains the target.

## 13.2 No automatic sliding — CURRENT

On steep but descendable terrain:
- Gear moves only while the player provides input.
- Releasing input stops the Gear.
- Do not auto-slide merely because the slope is steep.

## 13.3 Slope Resource cost — CURRENT

Movement Resource cost varies continuously with slope:
- Uphill: higher cost.
- Flat: baseline cost.
- Downhill: lower cost.
- Downhill still has a positive minimum cost and never generates Resource.

Use a common slope-cost behavior for standard Gear, then apply Gear movement-efficiency differences separately.

---

# 14. Step Height

## 14.1 Small steps — CURRENT

Step Height is separate from the slope-angle rule.

If a vertical change is within Step Height:
- Upward: automatically Step Up.
- Downward: treat as normal movement down.
- Do not enter a jump state.
- Position/posture may update abruptly rather than smoothly.

This deliberate "click" in posture can be used as an aiming tactic.

If vertical change exceeds Step Height:
- Upward: movement blocked.
- Downward: enter falling state.

Use the same Step Height threshold for upward/downward handling initially.

## 14.2 Value — TEMPORARY

Exact Step Height is not fixed.
Expose and tune in DEV.

---

# 15. Movement and falling

## 15.1 Ground movement — CURRENT

- No acceleration.
- No inertia.
- Move only while input is held.
- Releasing input stops immediately.
- Resource is consumed based on actual movement amount and slope-adjusted cost.

## 15.2 Air movement — CURRENT

While falling:
- No horizontal movement control.
- Aim remains available.
- Facing remains available.
- No movement Resource is consumed.

## 15.3 Air posture — CURRENT

When falling begins:
- Gear body instantly returns to horizontal.
- Facing is preserved.
- Barrel local angle is preserved.

On landing:
- Gear body instantly adopts the new terrain slope.
- Facing remains.
- Local barrel angle remains.
- Therefore world barrel angle changes naturally with the new posture.

## 15.4 Fall damage — CURRENT

Falling itself causes no damage.

Crossing the Death Line:
- Gear is Eliminated regardless of HP.

---

# 16. Gear / Wreck movement interaction

## 16.1 Movement obstacle rule — CURRENT

Living Gear and Wrecks are not movement obstacles.

- Gear may overlap Gear.
- Gear may overlap Wreck.
- Gear may move through Gear.
- Gear may move through Wreck.
- Gear and Wreck do not act as terrain support.

Projectile collision is separate:
- Living Gear can intercept projectiles.
- Wrecks can intercept projectiles.

---

# 17. Falling contact damage

## 17.1 Falling Gear → living Gear — CURRENT

When a falling living Gear contacts another living Gear below:
- The contacted Gear receives fixed 1 damage.
- The falling Gear receives no damage.
- Contact is treated as an attack event.
- Shield can block it and is consumed if triggered.
- No push/knockback from this contact.
- The falling Gear does not stop on the other Gear.
- If no terrain support exists, it continues falling.
- Friendly Fire applies.
- Multiple contacted Gear may each receive 1 damage.
- If an unusual trajectory causes repeat contact with the same Gear, each contact may deal another 1.

## 17.2 Falling Wreck → living Gear — CURRENT

- Fixed 1 damage to each living Gear contacted.
- Treated as an attack event.
- Shield can block it.
- Wreck does not stop because of Gear contact.
- No extra terrain damage from the contact.
- Wreck itself does not take damage.

## 17.3 Living Gear → Wreck while falling — CURRENT

- No damage.
- No Shield interaction.
- No push.
- Continue according to terrain/fall state.

---

# 18. Projectile collision and self-hit

## 18.1 Direct hit region — CURRENT

Standard Gear use a small shared circular projectile hit region around the common Core concept.

Exact radius is TEMPORARY/tunable.

## 18.2 Self-hit — CURRENT

Own projectile can hit the firing Gear.

- No launch-time immunity.
- If projectile spawns/travels into the firing Gear's valid hit region, resolve it normally.
- Self-damage is allowed.
- Shield can protect if applicable.
- Terrain destruction and knockback follow normal weapon rules.

## 18.3 Overlapping Gear — CURRENT

If Gear overlap:
- A projectile may hit another Gear immediately after leaving the Muzzle.
- This is a valid close-range direct hit.
- Overlap does not prohibit firing.

---

# 19. Damage

## 19.1 HP — CURRENT

- Maximum HP = 300 for all standard Gear.

Gear survivability differences are expressed through Defense / Durability, not different max HP.

## 19.2 Damage distance — CURRENT

For ordinary explosive attacks:
- Use one explosion/impact center.
- Compute distance from that center to each Gear Core.
- Closer to Core → stronger damage.
- Edge/direct visual contact does not automatically mean 100% damage.
- Do not add separate "direct hit damage + blast damage" as two independent damage packets unless a future weapon explicitly defines such behavior.

## 19.3 Falloff — CURRENT / TEMPORARY

- Use a steep / curved nonlinear damage falloff.
- Exact function is not fixed.
- Tune in DEV.

## 19.4 Defense — CURRENT

Defense/Durability modifies attack damage.
It does not prevent:
- falling,
- Death Line elimination,
- terrain support loss.

---

# 20. Knockback

## 20.1 Rule — CURRENT

Explosions can cause a very small knockback.

- Direction: from explosion center toward Gear Core.
- Distance from explosion affects amount.
- Gear weight affects amount.
- Lighter Gear moves more; heavier Gear moves less.
- Intended magnitude is small.

Shield:
- Prevents damage when triggered.
- Does not prevent explosion knockback.

If knockback leaves Gear unsupported:
- Resolve falling.
- No fall damage.
- Death Line can eliminate.

Exact knockback formula is TEMPORARY.

---

# 21. Terrain destruction

## 21.1 Source of Truth — CURRENT

Terrain collision/destruction uses the authoritative terrain mask.
For Stage E:
- white = terrain/collision/destructible,
- black = empty.

## 21.2 Weapon terrain parameter — CURRENT

Each weapon has its own:
- Terrain Destruction Radius.

Do not require a separate generic "destruction strength" parameter in the base model.
The basic destruction scale is represented by the weapon's terrain-destruction radius.

Gear damage radius and terrain-destruction radius are independent.

Therefore a weapon may have:
- large damage radius + small terrain radius,
- small damage radius + large terrain radius.

## 21.3 Gear direct-hit reduction — CURRENT / TEMPORARY

When a projectile directly hits a living Gear:
- Reduce the weapon's normal Terrain Destruction Radius by about 20%.
- Initial shared multiplier: approximately 0.8.
- Use one common direct-hit terrain multiplier across weapons.

Exact 20% value remains tunable.

---

# 22. Explosion event resolution

## 22.1 One-event result snapshot — CURRENT / IMPORTANT

For one explosion/attack event:
- Determine all affected Gear.
- Determine Shield results.
- Determine damage.
- Determine terrain destruction.
- Determine knockback.
- Resolve these from the same attack-event state so iteration order does not unfairly change the result.

Do not let "the first Gear processed died, therefore later Gear calculations changed" alter what should be one shared explosion event.

## 22.2 Post-explosion support and falling — CURRENT

After terrain is updated:
- Re-evaluate support for all relevant Gear/Wrecks.
- Any that lose support begin falling as part of the same resolution sequence.
- If multiple objects lose support, they begin falling together.
- Resolve every object's landing / Death Line / destruction state before advancing to the next Turn.
- Only after all related falling resolves should win/draw determination be finalized.

---

# 23. Battle Event Resolution Order

## 23.1 Core principle — CURRENT / IMPORTANT

Do not overlap major battle actions in a way that skips visible resolution.

A Turn-ending attack resolves conceptually as:

1. Fire.
2. Projectile flight / camera follow.
3. Impact.
4. Explosion / attack-event result determination.
5. Damage / Shield / terrain / knockback effects.
6. Support re-evaluation.
7. Falling.
8. Landing / Death Line.
9. Destroyed / Eliminated state.
10. Win / Draw evaluation.
11. Required camera/visual completion.
12. Next Turn.

A new Turn must not begin while the prior action's required game-state and visual resolution are still pending.

---

# 24. Win / elimination states

## 24.1 Destroyed vs Eliminated — CURRENT

Destroyed:
- HP reaches 0.
- Gear becomes a Wreck.

Eliminated:
- Gear leaves battle through rules such as crossing Death Line or current beta disconnect handling.

Both remove the player from future Turn/Phase participation.

## 24.2 Kill count — CURRENT

There is currently no kill-count scoring system.

Do not add kill attribution merely because a player caused another to fall.

Future point scoring may consider:
- damage dealt,
- destruction,
- victory,
but this is FUTURE only.

---

# 25. Wrecks

## 25.1 Wreck behavior — CURRENT

When HP reaches 0:
- Gear becomes a Wreck.
- Wreck remains in battle.
- Wreck can intercept projectiles.
- Wreck does not block Gear movement.
- Wreck does not support Gear.
- Wreck is supported by terrain and can fall if terrain is removed.
- Wreck is not further destructible.
- Wreck does not take additional damage.
- Wreck may disappear after crossing Death Line.

Projectile hitting a Wreck:
- Impact/explosion occurs at the collision point under normal weapon rules.

---

# 26. Shield

## 26.1 Shield item — CURRENT

- Uses no Resource.
- Counts as the one Item use for that Turn.
- Does not end the Turn.
- Prepared state persists until it blocks one attack event.
- No automatic turn expiration.
- Enemy is not shown a visible shield aura while merely prepared.

When triggered:
- One complete attack event's damage is blocked.
- If that attack event contains multiple hits, block all hits belonging to that same attack event.
- Shield is consumed.
- Show a barrier/shield visual effect at trigger time.
- Do not need text revealing "SHIELD".

Shield does not prevent:
- terrain destruction,
- explosion knockback.

Shield does protect against the special 1-damage attack events defined for:
- Teleport direct hit,
- falling Gear contact,
- falling Wreck contact.

---

# 27. Teleport

## 27.1 Basic item behavior — CURRENT

- Item uses no Resource.
- Item use arms Teleport.
- May be fired in the same Turn.
- May carry into the player's next own Turn.
- If not fired by the end of that next own Turn, it expires.
- Firing Teleport ends the Turn.
- Time Cost stops at actual Teleport projectile firing.

## 27.2 Projectile behavior — CURRENT

- Teleport projectile follows ordinary projectile trajectory principles.
- Teleport projectile is affected by wind.
- Impact position determines the teleport destination.

## 27.3 Direct hit — CURRENT / HF-SPECIFIC

If Teleport projectile directly hits a living Gear:
- Deal fixed 1 damage.
- Treat as an attack event.
- Shield can block the 1 damage and is consumed if triggered.
- Teleport transfer processing still continues after the hit.
- If the 1 damage reduces HP to 0, destroy the target first, then continue Teleport resolution using the impact position.

Teleport does not have ordinary blast damage.
Teleport does not destroy terrain through a normal explosion radius.

If Teleport projectile hits a Wreck:
- No damage.
- Use that contact point as the Teleport impact point.

## 27.4 Transfer placement — CURRENT

Teleport destination may overlap:
- living Gear,
- Wreck.

Those are not placement blockers.

Terrain Mask remains the terrain truth.
If needed, placement logic may search upward on the same X to obtain a valid placement relationship with terrain.

Teleport does not guarantee safety:
- after transfer, normal support rules apply,
- unsupported Gear falls,
- Death Line can eliminate.

## 27.5 State preservation — CURRENT

After Teleport:
- facing preserved,
- local barrel angle preserved,
- weapon selection preserved,
- Power Pointer preserved.

## 27.6 Camera / sequence — CURRENT

Teleport resolution is sequential:
- projectile impact,
- destination transfer effect,
- source disappearance effect,
- transfer,
- destination appearance effect,
- camera focuses the transferred Gear,
- after that presentation completes, next Turn camera transition begins.

Do not overlap all of these into one simultaneous visual jump.

---

# 28. Items

## 28.1 Capacity — CURRENT

- 4 Item slots.
- Duplicate Items allowed.
- All 4 slots may contain the same Item.
- Maximum 1 Item use per Turn.

Items use no Resource.
Each Item may still have an Item Turn Cost used by Turn Load.

## 28.2 Small Heal — CURRENT

- +40 HP fixed.
- Clamp to max HP 300.
- Does not end Turn.
- Player may continue moving/aiming/firing/Skip afterward.
- Show healing visual and +40-style floating number.

## 28.3 Large Heal — CURRENT

- +100 HP fixed.
- Clamp to max HP 300.
- Ends Turn immediately when used.
- Player may move before using it.
- Time Cost stops at item use.
- Show healing visual and floating number.

## 28.4 Shield — CURRENT

See Shield section.

## 28.5 Teleport — CURRENT

See Teleport section.

## 28.6 Item secrecy — CURRENT

Prepared/used Item identity should not be unnecessarily revealed to enemies.

General principle:
- Generic Item-use effect at preparation/use where appropriate.
- Reveal the identity only when its actual effect naturally exposes it.

Examples:
- Heal becomes obvious from healing.
- Shield identity becomes obvious when barrier triggers.
- Teleport becomes obvious when fired/resolved.

This supports future hidden-preparation Items such as Damage Up or Double Attack.

---

# 29. Power

## 29.1 Charge — CURRENT

- One-way charge from 0 to MAX.
- Time to MAX: 3.0 seconds.
- Reaching MAX auto-fires.

While charging:
- Aim may change within allowed rules before timer lock.
- Weapon may be switched.
- Current charge amount carries across weapon switching.

## 29.2 Power Gauge — CURRENT

- Bottom center.
- Percentage interval marks at 0 / 20 / 40 / 60 / 80 / 100 positions.
- Do not show a continuously changing numeric live Power value in normal UI.

## 29.3 Power Pointer — CURRENT

- Always available as a visual reference.
- Left click on Power Gauge sets pointer.
- Persists across Turns.
- Does not automatically release/fire.
- Pure aiming reference.

---

# 30. Wind

## 30.1 Wind display — CURRENT

- WIND gauge with center zero.
- Extends left/right for direction and strength.
- Initially place above Power Gauge.

## 30.2 Wind evolution — CURRENT / TEMPORARY

- Server authoritative.
- Changes each Turn.
- Battle begins with gentle wind.
- Wind generally trends stronger in its current direction.
- Near extremes, trend can reduce/reverse and eventually cross zero.
- Per-Turn change includes randomness.
- Later battle phases increase random change amplitude.
- Long battles may become increasingly turbulent.

A provisional normalized internal range such as -100..+100 is acceptable, but the exact physics coefficient is tuning.

## 30.3 Projectile wind consistency — CURRENT

All projectile types use the same fundamental wind-influence behavior/scale.
Do not make individual Gear/weapon wind sensitivity a normal differentiation axis.

Teleport projectile is also affected by wind.

---

# 31. HP, Resource and damage information

## 31.1 Normal UI visibility — CURRENT

Self / ally:
- Name.
- HP gauge.
- Resource gauge.
- No total numeric HP.
- No total numeric Resource.

Enemy:
- Name.
- Gear type visible.
- HP gauge hidden.
- Resource hidden.
- Selected weapon hidden.

DEV mode may show exact numeric internals.

## 31.2 Floating numbers — CURRENT

- Damage: show near affected Gear, e.g. -37.
- Heal: show near Gear, e.g. +40.
- Resource recovery amount may be shown numerically.
- Selected weapon Resource cost may be shown numerically.

## 31.3 Damage appearance stages — CURRENT

- 100–76%: normal.
- 75–51%: light damage.
- 50–21%: medium damage.
- 20–1%: heavy damage.
- 0%: destroyed.

Enemy HP is intentionally inferred partly through appearance rather than an exact gauge.

---

# 32. Camera

## 32.1 Turn focus — CURRENT

When the acting player changes:
- Camera transitions toward that player.

At the start of the local player's own Turn:
- Auto-center local Gear.
- Zoom to maximum aiming zoom.

If player manually zooms afterward:
- Cancel that auto-focus state for the rest of that Turn.

Middle mouse click:
- Recenter local Gear.
- Return to maximum aiming zoom.

## 32.2 Zoom — TEMPORARY

Initial tuning:
- approximately 0.5x to 3.0x.
- mouse wheel step approximately 0.2x.

Tune through playtesting.

## 32.3 Edge pan — CURRENT / TEMPORARY

- Pan using screen-edge zones on all four sides.
- Zone target around 10% of viewport dimension.
- Gentle variable speed:
  - slow near inner boundary,
  - faster toward outer edge,
  - capped maximum.
- Diagonal pan allowed.
- Exact curve/speeds are DEV tuning values.

## 32.4 Projectile follow — CURRENT

- Firing begins automatic projectile tracking.
- Player may manually pan/zoom during flight.
- Manual camera movement cancels auto projectile follow.
- If player cancels follow, do not forcibly snap camera back to impact.

---

# 33. Battle event communication

## 33.1 Chat channels — CURRENT

Communication subsystem supports:
- LOBBY
- ROOM
- BATTLE_GLOBAL
- BATTLE_TEAM
- WHISPER

Server authoritative routing.

TEAM battle:
- Other team's Team Chat is not sent to the client.

WHISPER:
- Target Player ID.
- Available across supported screens.

Battle display:
- Transparent text near upper left/right.
- Side can be switched.
- Global / Team / Whisper selector.

Voice Chat is FUTURE.

---

# 34. Guest Login and session

## 34.1 Beta Guest Login — CURRENT

- Player enters display name.
- Server issues temporary session / Player ID.
- No password/profile database required for beta.
- Server restart invalidates guest session.
- Relogin creates new session.
- Persistent account identity is FUTURE.

---

# 35. Battle disconnect

## 35.1 Beta — CURRENT

During an active Battle:
- Connection loss / browser close immediately Eliminates the player.
- Remove player from current/future Phase turns.
- Re-login cannot rejoin that same Battle.

## 35.2 Visual artifact after disconnect — OPEN

Not yet fixed:
- Whether the disconnected Gear visually disappears immediately,
- or becomes/leaves another battlefield representation.

Do not invent this behavior during implementation without Human decision.

## 35.3 Future reconnect model — FUTURE

Possible future:
- disconnected player transitions to NPC control,
- NPC continues play,
- restored authenticated/session state may return control to human.

Keep internal state extensible for:
- connected,
- disconnected,
- destroyed,
- eliminated,
- npc_controlled.

---

# 36. Battle result and Room return

## 36.1 Result — CURRENT

TEAM:
- winning Team,
- losing Team,
- DRAW when applicable.

FFA:
- final survivor,
- DRAW when applicable.

No current kill-count or detailed score result.

## 36.2 Return to Room — CURRENT

After Result:
- Return all participants to Room.
- Do not auto-return to Lobby.
- Clear all READY states.

Preserve:
- Gear selection.
- Team selection.

Items:
- Unused Items remain in their slots.
- Used Item slots become empty.
- No automatic refill.
- Player may refill/change via Item Storage.

A future Store/economy model remains possible but is not current beta behavior.

---

# 37. Fullscreen and screen flow

## 37.1 Screen flow — CURRENT

Use one application/game window with exclusive screen states:

Guest Login → Lobby → Room → Battle

Item Storage is another internal screen transition:
Room → Item Storage → Room

Do not vertically stack Login/Lobby/Room/Battle simultaneously.

## 37.2 Fullscreen — CURRENT

- Browser Fullscreen API supported.
- F12 toggles fullscreen.
- Room also exposes an easy fullscreen button.
- Esc may exit fullscreen through normal browser behavior.
- Reference viewport remains 1280×720 with responsive handling.

---

# 38. Stage E

## 38.1 Assets — CURRENT

Path:
projects/Hangfire/stages/pattern_e/

Assets:
- foreground.png
- mask.png
- background_far.png
- background_mid.png
- ASSET_MANIFEST.txt
- stage.json

Mask:
- 1920×720.
- Binary 0/255.
- white = authoritative terrain.
- black = empty.

Backgrounds:
- visual-only.

Reference viewport:
- 1280×720.

World:
- 1920×720.

Death Line:
- y = 720.

Crossing Death Line:
- Eliminated regardless of HP.

## 38.2 Current implementation state — NOT IMPLEMENTED / PARTIAL

At the last Human-tested local Layer5 integration state:
- Stage E visual assets were displayed.
- Terrain collision was still flat rather than fully mask-authoritative.
- Current CURRENT_SPEC terrain/support rules therefore require additional implementation.

---

# 39. Standard Gear and future Gear profiles

## 39.1 Standard Gear — CURRENT

Current base Gear identities include:
- Scout / Fast.
- Heavy.

Standard Gear share:
- max HP 300,
- max Resource 200,
- core damage concept,
- standard projectile hit-region concept,
- standard ground-contact profile,
- standard base slope rules,
- common Aim speed.

Differences can be created through:
- movement efficiency,
- Defense/Durability,
- Weight,
- weapon parameters,
- barrel geometry,
- local aim range,
- other explicit Gear parameters.

## 39.2 Future special movement/posture profiles — FUTURE

The architecture should permit future Gear such as:
- Climber capable of terrain normal Gear cannot climb.
- Hover-like Gear that stays slightly above ground.
- Always-horizontal Gear whose body/aim range does not rotate with terrain.
- Special leg/contact behavior.
- Nonstandard barrel pivot/articulation.

These may override Movement / Ground Contact / Posture Profile.

Unless explicitly redesigned later, do not use visual size alone to alter the shared damage-core philosophy.

---

# 40. DEV / Tuning policy

## 40.1 DEV visibility — CURRENT

DEV should expose gameplay-relevant authoritative and derived values, including as applicable:
- Turn timer.
- Phase index/order.
- Turn Load components and result.
- Resource current/recovery/cost.
- Weapon Resource Cost.
- Weapon Turn Cost.
- Item Turn Cost.
- Gear Core.
- Projectile hit circle.
- Ground contact bar.
- Central support zone.
- Support occupancy.
- Terrain slope estimate.
- Step Height.
- slope limits.
- damage radius/falloff.
- terrain destruction radius.
- direct-hit terrain multiplier.
- knockback values.
- wind value/effect coefficient.
- server current player/logical ordering/state revision.
- accepted authoritative values.

Normal player mode should hide debug internals.

---

# 41. Important superseded decisions

The following older values/interpretations are explicitly superseded by this document.

## 41.1 Resource — SUPERSEDED

Old:
- max 100,
- fixed +20 recovery.

Current:
- max 200,
- start 0,
- first-turn recovery approx +35,
- later recovery based on Turn Load.

## 41.2 Turn ordering — SUPERSEDED

Old interpretation:
- fully continuous global next-action scheduling with no Phase boundary.

Current:
- one Turn per active player per Phase,
- reorder at Phase end using Turn Load,
- effective consecutive Turns may occur across Phase boundaries.

## 41.3 Gear projectile hit size — SUPERSEDED

Old:
- per-Gear circular hit radius.

Current:
- standard Gear use a common projectile-hit region concept around the common Core.
- visual size does not automatically change hit size.

## 41.4 Terrain destruction strength — SUPERSEDED

Old:
- independent generic Terrain Destruction Strength plus radius.

Current:
- base weapon terrain destruction is primarily defined by Terrain Destruction Radius.
- damage radius remains independent.

## 41.5 Spawn runtime spacing — SUPERSEDED

Old:
- runtime minimum spacing check.

Current:
- map-authored spawn candidates already provide acceptable placement.
- randomly choose among candidates.

## 41.6 Gear/Wreck movement collision — SUPERSEDED

Any intermediate wording that treated Gear/Wreck as physical movement obstacles is superseded.

Current:
- they are pass-through for Gear movement,
- not terrain support,
- but retain projectile collision where defined.

---

# 42. Remaining OPEN tuning / implementation decisions

These are not contradictions. They remain intentionally unresolved.

1. Exact Turn Load formula and component weights.
2. Exact Resource recovery curve and zero-recovery threshold.
3. Exact Step Height.
4. Exact standard Ground Contact Bar dimensions.
5. Exact central Support Zone dimensions.
6. Exact Support occupancy threshold.
7. Exact standard projectile hit-circle radius.
8. Exact damage falloff curve.
9. Exact knockback formula and magnitude.
10. Exact wind physics coefficient/change curve.
11. Exact Gear/Weapon numerical balance values.
12. Exact disconnected-Gear visual battlefield behavior.

These should be handled through DEV tuning or a later Human specification decision rather than guessed during implementation.

---

# 43. Implementation checkpoint rule

Before implementing code from this specification:

1. Read this CURRENT_SPEC.md first.
2. Compare the target subsystem against older Hangfire documents.
3. If an older document conflicts with CURRENT_SPEC.md, do not silently blend them.
4. Treat CURRENT_SPEC.md as the newer Human-approved decision.
5. Mark required older-document updates separately.
6. Do not start unrelated Layer work.
7. Build/test/playtest after each bounded implementation step.
8. Report remaining NOT IMPLEMENTED items explicitly.

---

# 44. Current next step

This document is the specification checkpoint.

Next work should be:
1. Audit existing Hangfire specification files against CURRENT_SPEC.md.
2. Identify contradictions and stale values.
3. Update the relevant Source-of-Truth documents in a controlled pass.
4. Only then create the next Codex implementation task.

Do not begin large gameplay implementation directly from old documents before that audit.
