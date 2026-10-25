---
document_type: research_note
date: 2026-10-26
status: CANDIDATE
implementation: NOT IMPLEMENTED
topic: local-ai-gpu
evidence_status: CONFIRMED_CORE_CLAIM / LONG_TERM_SAFETY_UNVERIFIED
---

# GPU-Unlock — Efficiency Research Theme

RTXのTensor演算制限を解除し、AI処理性能を高めるOSS。

オーバークロックとは別方式だが、**消費電力・発熱・VRM負荷が増える可能性があり、長期安全性は未検証**。常用は慎重に扱う。

## Research theme

**GPU-Unlock + undervolt + power limit**

性能最大化ではなく、**性能/Wを改善できるか**を検証する。

## OSS

- Ampere（RTX 30系）  
  https://github.com/Zagitta/gpu-unlock
- Ada（RTX 40系）  
  https://github.com/JustAResearcher/gpu-unlock-ada
- Turing（RTX 20系）  
  https://github.com/nlzy/turing-unlock

## Boundary

- 研究候補として保存
- 実機導入は未承認
- 常用安全性は未確認
- GPU世代・個体・ワークロードごとの効果差を前提とする
