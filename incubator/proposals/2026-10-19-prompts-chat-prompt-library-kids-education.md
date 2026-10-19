---
status: research-candidate
created: 2026-10-19
origin: "Human-shared f/prompts.chat promotional post; official GitHub README, licenses and selected Japanese kids lessons inspected"
decision: CANDIDATE
implementation: HOLD
current_priority: LOW
stage_1_rank: A+
stage_2_rank: A
evidence_status: "UPSTREAM SOURCE CONFIRMED / EDUCATIONAL EFFECT UNVERIFIED"
human_decision: "Save research information now; verify usefulness later; preserve children's AI-education information as particularly valuable"
tags:
  - prompts-chat
  - prompt-library
  - prompt-engineering
  - role-pattern-library
  - skills
  - education
  - kids
  - japanese
  - growgle
  - research-candidate
trigger_topics:
  - prompts.chat
  - f/prompts.chat
  - prompt-library
  - Promi
  - Prompting for Kids
  - growgle
  - 子ども向けAI教育
  - プロンプト教材
---

# prompts.chat — 公開プロンプト集と子ども向けAI教育教材

## Human decision (2026-10-19)

- User supplied https://github.com/f/prompts.chat and asked whether **the actual prompts are published**.
- Human decision: **"いつか検証しよう。とりあえず保存だね。子供向けの情報は貴重だよ！"**, then explicitly authorized creating this note on branch `development`.
- Save as **research knowledge only**, not as a new installed tool, adopted Skill, validated educational program, or change to growgle.
- **Stage 1: A+ / Stage 2 provisional: A / CANDIDATE / implementation HOLD / adoption priority LOW.**
- Children-facing resource has **high future reference value** independently of the current library adoption priority.
- Only this Incubator note is authorized; do not alter Core, Skills, runtime, growgle implementation or other files.

## 1. Verified primary sources

- Official repository: https://github.com/f/prompts.chat
- Prompt browser: https://prompts.chat/prompts
- Complete prompt contents in Markdown: https://github.com/f/prompts.chat/blob/main/PROMPTS.md
- Prompt dataset in CSV: https://github.com/f/prompts.chat/blob/main/prompts.csv
- CLI / MCP / Claude Code plugin instructions: https://github.com/f/prompts.chat/blob/main/README.md and https://github.com/f/prompts.chat/blob/main/CLAUDE-PLUGIN.md
- Self-hosting: https://github.com/f/prompts.chat/blob/main/SELF-HOSTING.md
- License declaration: https://github.com/f/prompts.chat/blob/main/LICENSE
- Harvard reference (linked by author): https://www.huit.harvard.edu/news/ai-prompts
- Columbia reference (linked by author): https://etc.cuit.columbia.edu/news/columbia-prompt-library-effective-academic-ai-use

### Established

1. **Prompts are published verbatim**, not merely as names/descriptions: browse them online or read `PROMPTS.md` / `prompts.csv`. The collection was formerly Awesome ChatGPT Prompts.
2. Repository included **CLI**, an **MCP integration**, and a **Claude Code plugin**, documented by the maintainer and supported by code/configuration files in the repository.
3. Repository's dual licensing explicitly distinguishes **prompt text/data: CC0 1.0 Universal** from **source code and site-authored material: MIT**. CC0 does not warrant absence of third-party rights in each item; check individual content when necessary.
4. GitHub API reported **173,465 stars at the 2026-10-19 inspection**. This is a time-sensitive popularity measure, not quality evidence.
5. The README cites Harvard and Columbia university resource pages. Such educational referencing is **not** a scientific endorsement or performance benchmark of every prompt.
6. The developer offers self-hosting, but that implies Node.js/PostgreSQL, maintenance, and possibly hosting/API costs. **Free public browsing ≠ zero cost for every deployment option.**
7. "World's largest" is **a maintainer marketing claim**, not independently verified.

### Not established

- Prompt accuracy, reliability, model-independent performance or measured instructional benefit.
- Security of every community-submitted prompt or MCP installation under all agent contexts.
- Educational results, child comprehension across ages, privacy properties or usability of live kids website on the intended device.
- No installation, live user trial, prompt benchmark or independent comprehensive code audit was performed.

## 2. Children's resource — PRIORITIZED FOR LATER REVIEW

### Prompting for Kids / Promi

- Entry page: https://prompts.chat/kids
- Intended audience per maintainer: **ages 8–14**; a game-like introduction to communicating with AI through a robot character called **Promi**.
- **Japanese lesson source exists**, not only a Japanese-language navigation shell:
  - https://github.com/f/prompts.chat/blob/main/src/content/kids/ja/1-1-meet-promi.mdx
  - https://github.com/f/prompts.chat/blob/main/src/content/kids/ja/2-4-detail-detective.mdx
  - https://github.com/f/prompts.chat/blob/main/src/content/kids/ja/5-1-perfect-prompt.mdx
- Source inspection confirmed Japanese explanatory panels, examples, answers, and exercise components, including `WordPredictor`, `PromptVsMistake`, `PromptParts`, `DragDropPrompt`, `MagicWords`, and `StepByStep`. Website implementation uses a staged, interactive game interface.

### Topics actually present in examined lessons

1. What AI is; a simple pattern/next-word guessing exercise and explanation of what a prompt is (`1-1-meet-promi.mdx`).
2. Why specific instructions give a clearer target than a vague request; compare examples, identify task/context/constraints (`1-1`, `2-4`).
3. A detective exercise about **who / what / when / where**, including assembling prompt elements (`2-4-detail-detective.mdx`).
4. Combine clarity, examples, background, formatting, role-play, and creativity in a prompt (`5-1-perfect-prompt.mdx`).
5. A worked arithmetic example illustrates showing calculation steps. **This is lesson content, not proof that chain-of-thought prompting always improves model accuracy, nor a guarantee that all models expose private reasoning.**

### Why particularly relevant to growgle

- Possible **children's AI-learning resource/category** for growgle, separate from evaluating prompts.chat as Harness runtime infrastructure.
- Reusable educational concepts: short challenges, progressive levels, compare good/bad prompts, fill-in-the-blank, immediate feedback, Japanese localization, friendly consistent mascot.
- It may work as a *linkable third-party activity* or *UI/pedagogical reference*; there is no approval to copy artwork, branding, audio, or the product wholesale.
- A good lesson should also teach **critical checking of AI answers**, limits of AI, avoiding personal-information disclosure, and when to ask an adult. These are **evaluation criteria proposed by AI-Harness**, not verified claims about the site's current curriculum.
- Especially important: inspect live functionality and age appropriateness in Japanese before recommending to children. Assess registration/data collection, interactions with any live model, external links, parental oversight, accessibility, and device compatibility.

### Future child-safety and educational verification checklist

- Does the actual website operate in Japanese through the full sequence, on mobile?
- Can children use the learning modules without creating an account or entering personal information?
- Is user text sent to a remote model/service, and what is retained? Check published privacy practices, not only source code.
- Can a younger child understand the instructions without continuous adult guidance?
- Does it teach that AI can be confidently wrong and that sensitive data must not be entered?
- Are the exercises engaging and genuinely instructive, rather than simply reward-driven?
- Check any reused images/audio/code licenses separately; prompt text CC0 does not automatically mean all site assets are CC0.

## 3. AI-Harness overlap and role

- Existing research: `incubator/proposals/2026-09-20-role-pattern-library.md`. It already treats public agent/prompt patterns as a **parts library, not authority**, with understanding/testing/Human adoption before reuse.
- Existing `skills/README.md`: Skills must be purposeful, limited, reusable and verified. Community prompts **are not automatically Skills**.
- Compared with existing ChatGPT/Codex/GitHub access, a new MCP server or full deployment has low demonstrated marginal benefit today.
- Do **not** bulk-import prompts into Core, persistent memory, or agent instruction context: individual external prompts may contain untrusted instructions; prevent prompt injection and context pollution.
- Use prompts.chat as an on-demand **reference library for examples and wording**, not as an authoritative configuration store.

## 4. Smallest future test (not approved now)

**General prompts:** choose 2–3 actual current tasks and compare existing Harness wording with relevant published prompts under the same model/settings; check compliance, task result, token/context cost, and Human revisions. Do not infer success from stars/votes.

**Children:** separately review the Japanese kids sequence from adult/educational/safety perspectives and run a short supervised usability test *only with Human approval and appropriate safeguards*. Record actual tasks, where the child is confused, and any privacy/safety gaps. Keep this evaluation distinct from Harness prompt benchmarking.

If there is no concrete use, the present official links are sufficient: no hosting/database, account registration, installation, dataset mirroring, or new Skill is necessary.

## 5. Decision and boundaries

| Aspect | Decision |
| --- | --- |
| Stage 1 | A+ (high novelty/visibility and possible educational value) |
| Stage 2 | A (upstream features/licenses/source confirmed; efficacy untested) |
| Research status | CANDIDATE |
| Implementation | HOLD |
| Immediate adoption priority | LOW |
| Child education reference | Preserve visibly; consider later growgle research |
| Next step | None until a targeted evaluation is requested |

**Approved work in this turn**: add this **one Markdown note** under `incubator/proposals/` on `development`. No installations, no account/API connections, no exports of private information, and no modifications to Core, Skills, growgle, or other existing files.
