# Obsidian Proposal Incubator Setup

Date: 2026-09-20

Purpose: record the actual setup used to connect the AI-Harness GitHub repository with Obsidian for Proposal Incubator experiments.

This document is a human-facing setup record. It does not define Core Harness behavior.

---

## 1. Architecture

```text
ChatGPT / AI-Harness
        ↓
GitHub development branch
        ↓
local AI-Harness clone
        ↓
Obsidian opens the same folder as a Vault
        ↓
Smart Connections performs local semantic discovery
        ↓
Obsidian Git periodically pulls remote updates
```

Roles:

- GitHub = durable storage, history, AI-readable source
- Obsidian = human-facing exploration and semantic discovery
- Smart Connections = related-note candidate discovery
- Obsidian Git = automatic Git pull into the local Vault
- AI-Harness = interpretation, synthesis, prioritization
- Human = approval gate for consequential system changes

Obsidian is not the Source of Truth by itself. The repository remains the durable source.

---

## 2. Clone AI-Harness to Windows

Open PowerShell.

Example using the Documents folder:

```powershell
cd "$HOME\Documents"
git clone -b development https://github.com/KuraMasajapan/AI-Harness.git
cd AI-Harness
git branch --show-current
```

Expected branch:

```text
development
```

No additional Obsidian-specific Git branch is required.

---

## 3. Open the repository as an Obsidian Vault

Start Obsidian.

Choose:

```text
保管庫としてフォルダを開く
(Open folder as vault)
```

Select:

```text
Documents\AI-Harness
```

The Git repository itself becomes the Vault.

Expected top-level items include:

```text
agents/
core/
evaluation/
experiments/
memory/
projects/
skills/
HARNESS.md
HANDBOOK.md
README.md
```

Do not create a separate copy of the repository for Obsidian.

---

## 4. Local Obsidian files excluded from Git

The development branch contains a root `.gitignore` with:

```gitignore
.obsidian/
.DS_Store
Thumbs.db
```

Purpose:

- keep local Obsidian settings out of the public repository
- avoid committing OS metadata

Checkpoint commit:

```text
334de9a66cef11fe0d857b2347b7fc56417ddb4a
```

---

## 5. Install Smart Connections

In Obsidian:

```text
設定
→ コミュニティプラグイン
→ 閲覧
→ Smart Connections
→ インストール
→ 有効化
```

Plugin observed during setup:

- Name: Smart Connections
- Author: Brian Petro
- Version observed: 4.7.2

No cloud API key was configured for the initial test.

---

## 6. Verify local embeddings

Open:

```text
Smart Connections
→ オプション
→ Smart Environment
→ Open settings
```

Observed configuration:

```text
Default embedding model:
transformers - TaylorAI/bge-micro-v2
```

The model is shown as Current.

For the initial experiment:

- use local embeddings
- do not configure OpenAI / Gemini / other cloud API keys
- leave unrelated Smart Environment settings unchanged

This keeps the semantic-discovery test local and simple.

---

## 7. Open the Connections view

To view related notes:

```text
Ctrl + P
→ Smart Connections
→ Smart Connections: Open: Connections view
```

Open a proposal note and inspect the right sidebar.

The score shown next to each note is treated only as a semantic-relatedness signal.

Important:

```text
Semantic similarity ≠ final system judgment
```

Smart Connections proposes candidates. AI-Harness and the human decide whether the relationship is meaningful.

---

## 8. Initial semantic-discovery test

Test fixtures:

```text
experiments/proposal-incubator/semantic-test/2026-09-20/
```

Observed from `01-execution-receipt.md`:

- `03-save-state-boundary.md` — 0.78
- `02-permission-checkpoint.md` — 0.75
- hardware-layout distractor ranked lower

Initial feasibility result:

```text
PASS
```

Result record:

```text
experiments/proposal-incubator/semantic-test/2026-09-20/RESULTS.md
```

---

## 9. Real Proposal test

Real proposal fragments were added under:

```text
experiments/proposal-incubator/real-set/2026-09-20/
```

Observed bridge candidate:

```text
16-proposal-recall-trigger.md
```

Reverse-probe results included:

- `18-proposal-incubator-setup-trigger` — 0.87
- `04-decision-integrity` — 0.85
- `14-proposal-synthesis` — 0.84
- `17-proposal-collector` — 0.83
- `01-action-receipt` — 0.83
- `15-latent-structure-discovery` — 0.81
- `02-save-boundary` — 0.78

Interpretation:

Proposal Recall may act as a bridge between several apparently different improvement areas.

This does not prove those proposals should become one system. It supports using semantic search as a candidate-discovery layer.

Result record:

```text
experiments/proposal-incubator/real-set/2026-09-20/RESULTS.md
```

---

## 10. Install Obsidian Git

In Obsidian:

```text
設定
→ コミュニティプラグイン
→ 閲覧
→ Git
→ インストール
→ 有効化
```

The purpose in the current design is automatic pull only.

We do not want Obsidian to automatically push local edits back to GitHub.

---

## 11. Obsidian Git settings used

### Automatic

```text
Split timers for automatic commit and sync = ON
Auto commit interval = 0
Auto push interval = 0
Auto pull interval = 10 minutes
```

Interpretation:

- auto commit is disabled
- auto push is disabled
- remote changes are pulled every 10 minutes

### Pull

```text
Merge strategy = Merge
Merge strategy on conflicts = None (git default)
Pull on startup = ON
```

### Commit-and-sync

```text
Push on commit-and-sync = OFF
Pull on commit-and-sync = ON
```

This produces the intended direction:

```text
GitHub → Obsidian = automatic
Obsidian → GitHub = not automatic
```

Do not enable automatic push unless the workflow is deliberately redesigned and reviewed.

---

## 12. Auto-pull verification

A test file was committed to:

```text
experiments/proposal-incubator/auto-pull-test/2026-09-20/AUTO_PULL_TEST.md
```

Checkpoint commit:

```text
6f2ad24ab255a0cd4a26afa088a716b751635161
```

Expected behavior:

- do not run manual `git pull`
- wait for the configured 10-minute interval or restart Obsidian
- confirm the file appears locally

At the time this document was created, the local observation result had not yet been recorded here.

---

## 13. Screenshots

Useful screenshots were captured during setup for:

1. Opening an existing folder as an Obsidian Vault
2. Smart Connections installed/enabled
3. Smart Environment local embedding model
4. Connections view and semantic scores
5. Obsidian Git automatic settings
6. Obsidian Git pull / push settings

These screenshots currently exist in the ChatGPT conversation used for setup, but the GitHub connector used in this workflow writes UTF-8 repository files and does not directly attach the existing conversation screenshots.

Recommended future image paths:

```text
docs/images/obsidian/
  01-open-folder-as-vault.png
  02-smart-connections-installed.png
  03-smart-environment-local-embedding.png
  04-connections-view.png
  05-obsidian-git-automatic.png
  06-obsidian-git-pull-settings.png
```

Once image upload is available through the chosen workflow, add the screenshots and embed them in this guide.

---

## 14. Current operational principle

```text
GitHub
= durable storage + history + AI-readable source

Obsidian + Smart Connections
= semantic candidate discovery

AI-Harness
= interpretation + synthesis + prioritization

Human
= consequential-change approval
```

The goal is not to let semantic similarity automatically rewrite the Harness.

The goal is to keep weak ideas available long enough for previously invisible relationships to become discoverable.
