# Prompt Motion Reference — 2026-10-07

Status: REFERENCE / HIGH VALUE / NOT INTEGRATED

Source:
- https://www.prompt-motion.com/
- Curated by @p4nthera_
- Site description: a collection of motion videos made with Claude Opus 5.5, together with the prompts and skills behind them.

## Why this is worth preserving

Prompt Motion is not just a gallery of generated video.

It is a practical pattern library for **code-driven motion generation** where the creative result is expressed as:
- prompt / creative direction,
- reusable skill,
- deterministic HTML or component logic,
- browser-based rendering,
- audio / beat timing,
- validation and iteration.

That makes it relevant to future AI-Harness work around:
- visual generation,
- motion / video generation,
- reproducible creative workflows,
- skills as reusable production knowledge,
- browser-rendered artifacts,
- Human review of visual outputs.

## Patterns observed

Several examples on the site use a workflow roughly like:

```
Creative brief / prompt
        ↓
Structure / beat map
        ↓
Code-generated scene
        ↓
Deterministic time-based animation
        ↓
Browser render (often Playwright)
        ↓
Frame / beat validation
        ↓
Video output
```

A recurring design principle is that motion should be derived from time rather than hidden runtime state. This makes rendering reproducible and easier to inspect frame-by-frame.

Examples on Prompt Motion also show:
- HTML + Playwright as a motion-rendering stack.
- closed-form spring motion instead of ad-hoc timers.
- rendering multiple subframes and blending them for motion blur.
- checking frames against a beat grid before full render.
- product / UI launch films created from real components and brand assets.
- reusable skills that interview the Human, plan the film, then render it.

## Notable references

### Cinetic
Prompt Motion includes a skill called **Cinetic**, described as an agent skill that helps a coding agent concept, brand, score, and render short cinematic launch films or motion pieces from code.

Source page:
https://www.prompt-motion.com/lexnlin-6161a6

### Product Film Skill
Prompt Motion also includes a skill for building launch / landing-page videos from a product's real design system, logo, music, and components using Remotion.

Source page:
https://www.prompt-motion.com/anthonyriera-9b1b2a

### HTML + Playwright motion examples
Multiple entries use HTML + Playwright for deterministic motion rendering, including UI-state morphing and launch-film style sequences.

Representative source:
https://www.prompt-motion.com/twoclipping-221cab

## Why it matters for AI-Harness

The most reusable idea is not any single prompt.

It is the separation of:

```
Intent
  ↓
Creative direction
  ↓
Reusable production skill
  ↓
Deterministic renderer
  ↓
Validation
  ↓
Artifact
```

This fits the Harness preference for:
- explicit process,
- reproducible outputs,
- validation before completion,
- Human review at meaningful checkpoints,
- reusable skills instead of one-off prompting.

Potential future candidate:

```
Visual / Motion Skill
        ↓
Brief
        ↓
Storyboard / Beat Map
        ↓
Code-based Render
        ↓
Automated Frame Checks
        ↓
Human Visual Approval
        ↓
Final Video
```

## Preservation rule

Do **not** mirror or copy the full prompts from Prompt Motion into AI-Harness.

The site states that videos and prompts belong to their creators. Keep:
- source URLs,
- workflow observations,
- reusable architectural patterns,
- our own derived notes.

If a specific prompt or skill becomes important, inspect and cite the original source at that time.

## Current decision

KEEP AS A HIGH-VALUE REFERENCE.

Do not integrate a specific video stack yet.

Revisit when:
1. we build a code-driven video / motion workflow,
2. we create reusable visual-generation Skills,
3. we want deterministic rendering instead of opaque one-shot video generation,
4. we need a visual validation loop comparable to executable tests in coding.
