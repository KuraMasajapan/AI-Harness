# Hangfire — Layer 5 Lobby / Room / Team / Communication

Status: HUMAN-APPROVED TASK
Date: 2026-09-28

## Scope

Implement the first post-login Lobby, guest session identity, invite-code Rooms,
server Team assignment, even-player Battle start and independent text Communication
routing. Keep state in one lightweight process; no database, Redis, persistence,
matchmaking, NPC, Gear differences, Turn Load, Cooling, Stage or terrain destruction.

## Adopted rules

- Display name login creates a server-issued temporary session ID and Player ID.
  Client cannot choose IDs. Restart invalidates sessions. This is conceptually separate
  from a future persistent Account ID.
- Room creator is host. Host leave/disconnect transfers host to the oldest remaining player.
- Join order assigns Team A, Team B, A, B. Modes are exactly 1v1/2v2/3v3/4v4.
- Start requires the exact mode size, equal Team sizes and no NPC. No mid-battle join,
  Team change, spectator or voluntary Battle leave.
- Team win means zero active Battle players in that Team. Connected, disconnected,
  destroyed, eliminated and npc_controlled remain distinct. Layer 5 does not implement
  reconnect or NPC takeover; disconnected/destroyed/eliminated players leave turn scope.

## Communication

Channels are independent routing records reusable by future Text/Voice transports:
LOBBY, ROOM, BATTLE_GLOBAL, BATTLE_TEAM and WHISPER. Server sends only authorized
recipients; BATTLE_TEAM never sends to the opposing Team. Messages identify channel,
sender, display name, target/scope, room/battle/team, text and server timestamp.
History is short-lived in memory. Text is limited to 500 characters and five messages
per ten seconds per Player.

## Acceptance

- Guest login issues server-only IDs and Lobby state.
- Create/join/leave, host transfer, room list, capacity 8, modes and start rules work.
- Room and Battle participant/team state is server authoritative.
- All five channel routing paths, Team non-delivery and Whisper work.
- Lobby/Room scroll history and Battle transparent overlay expose only received messages.
- Existing Layer 1–4 behavior remains 39/39 regression PASS.
