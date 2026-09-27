# Layer 5 plan

- Base latest `development` 23cf229; preserve existing Layer 4 test mode and runtime mechanics.
- Add one in-memory Lobby hub for temporary sessions, Room lifecycle, join-order Team assignment,
  Battle metadata and communication routing. Keep ID issuance and all scope checks server-side.
- Switch normal CLI startup to Lobby mode; retain explicit legacy/realtime test construction for
  Layer 1–4 regression. Client becomes a lightweight login/Lobby/Room/Chat surface.
- Do not implement account persistence, reconnect, NPC, voice transport, Stage, Gear balance,
  Turn Load or terrain destruction. Record provisional boundaries in checkpoint.
- Tests: session/ID, room/mode/host/leave, Battle status, all channel routing, team non-delivery,
  whisper, limits, HTTP integration plus existing39 tests.
