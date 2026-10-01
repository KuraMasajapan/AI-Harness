# BBB v0.8.7 Cool Contrast UI — Checkpoint
Date: 2026-10-02

## Human feedback
- Light skins were initially too bright.
- Calm v0.8.6 reduced glare but also reduced page contrast.
- Use two main colors and make the app look cooler / more product-like.

## Design decision
Main colors:
- Deep Navy: #0B1622
- Electric Blue: #2F9EE5

Semantic green / yellow / red are status-only.

## Visual hierarchy
- Sidebar: darkest surface
- Workspace: dark navy surface
- Cards: one step lighter
- Metrics/fields: inset darker surface
- Borders stronger than v0.8.6
- Active nav: Electric Blue left rail
- Primary action: flat Electric Blue
- No large bright gradients or pastel surfaces

## Skin set
- Graphite Blue / グラファイトブルー
- Deep Navy / ディープネイビー
- Steel Slate / スチールスレート
- Black Ice / ブラックアイス

All skins remain within the same cool UI family.

## Design research
Reference direction: real-product UI galleries such as Mobbin and SaaSFrame.
Applied only general hierarchy, limited-accent, and analytics-dashboard principles; no specific product screen copied.

## Validation
- pytest: 54 passed
- compileall: PASS
- UI JavaScript syntax: PASS
- flat ZIP root: PASS
- package extraction + pytest: 54 passed
- package: BBB_v0.8.7_Cool_Contrast_UI.zip
- SHA-256: d1a60f524b1b56922820feaefe81fa5f321b6717056bb2e8b8f4b1056eeed64a

## Safety
No change to trading boundary. UI-only change plus version update.
