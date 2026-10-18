# grokbot-local-agent — durable local task handoff and webhook wake-up

- Recorded: 2026-10-18
- Origin: Grok daily observer, Airtable Harness Inbox `reczxjnXZyxdJaePy`; Observer Runs `recUiJWurDxQvMyOr`
- Stage 1 (Grok): HIGH
- Stage 2 (ChatGPT): **A+ / CANDIDATE**
- Implementation: **HOLD / NOT IMPLEMENTED**
- Human decision: **SAVE research record** (2026-10-18); no adoption or installation approval
- Evidence: CONFIRMED for repository and described design; UNVERIFIED for cost-savings amount and real-world reliability

## Source and confirmed design

- Primary: https://github.com/robbin/grokbot-local-agent
- Official README reviewed on 2026-10-18.
- Grok Bot delegates heavy work to a **Pi coding agent on the same machine** through a wrapper task script; this is not a demonstrated remote connection to a separate household PC.
- Each task persists state and artifacts in `~/.pi/tasks/<task-id>/`, records an owner, and can be queried using pending/list/ack. The owner constraint reduces accidental cross-bot acknowledgments.
- Completion sends a minimal webhook notification with source, task ID, owner, state and exit code; the Bot wakes, verifies output/diff/tests, reports, and acknowledges.
- Disk state, **not webhook delivery**, is the durable source of truth. Pending tasks can be recovered if the webhook is missed.
- README itself suggests Cursor Cloud Agent for longer, more complex multi-step project work; its local Pi pattern is positioned as a lightweight second pair of hands.

## Why relevant to AI-Harness

**A+** because this is a concrete, small reference implementation of task durability, owner attribution, resume and result verification, aligned with low-cost local-agent experimentation. Potential architectural references:
- `incubator/proposals/2026-10-14-temporal-runtime-discussion-checkpoint.md` — time axis / runtime event semantics, not an existing deployed scheduler.
- `incubator/proposals/2026-09-20-temporal-context-layer.md` — event freshness and activity signals.
- `incubator/proposals/2026-10-09-pidurablekit-iphone-durable-runtime.md` — durable task state and mobile control candidate.
- `projects/Hermes_Local_Agent/` — local agent investigation, currently not permission to implement.
- `incubator/proposals/2026-10-18-heldkeys-agent-credential-exposure.md` — complementary credential-exposure review if agents execute commands.

## Trade-offs / uncertainties

- No verified benchmark of subscription/token savings. Model and provider pricing, workload and execution environment determine actual savings.
- Webhook secrets, replay protection, sender authentication, failure handling, filesystem permissions and process isolation require separate security review.
- Task states may become inconsistent under crashes; recovery and idempotency need testing.
- Do **not** treat this as proof that Grok Bot, ChatGPT or Hermes can currently wake each other or operate a remote local PC.

## Future research (not approved for execution)

1. Compare task-state / owner / pending / ack design against existing AI-Harness checkpoint and Temporal Runtime proposals; reuse rather than duplicate.
2. In an isolated proof of concept, test crash recovery, lost webhook, duplicate notification, incorrect owner, and partial task completion.
3. Check human approval boundaries before any file write, external access, secret use or autonomous agent action.
4. Measure cost and context savings with matched workloads; evaluate against simpler scheduled/manual polling.

**Boundary:** Research note only. No installs, webhooks, scheduled tasks, GitHub workflow changes, Core/Trinity edits or remote access were authorized.
