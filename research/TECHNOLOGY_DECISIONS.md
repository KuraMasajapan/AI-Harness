# Technology Decisions — AI-Harness

AI-Harness環境における外部技術の評価履歴。**REJECTは当環境での不採用**を意味し、技術・サービス全般の否定ではない。詳細な不採用レポートは残さず、再調査時の重複検知に必要な最小限の根拠のみ記録する。

| 評価日 (JST) | 技術・一次資料 | 判断 | 不採用の決定的根拠 |
| --- | --- | --- | --- |
| 2026-11-10 | **Freebuff** — [公式](https://freebuff.com/) / [投稿](https://x.com/jahooma/status/2119982082227343592) | **REJECT（現行AI-Harnessへの導入）** | [公式の無料枠説明](https://freebuff.com/blog/how-is-freebuff-free)では日本は原則1日5時間分で無制限ではない。[公開利用規約（2026-11-12発効予定）](https://freebuff.com/terms-of-service)は無料推論の外部自動操作・中継を制限。[公開プライバシー文書（同日発効予定）](https://freebuff.com/privacy-policy)にはプロンプト／プロジェクト情報の広告個別化利用、接続リポジトリの評価を記載。Codex等に対する実測上の優位性も未確認。 |
| 2026-11-11 | **LocalHarness** — [公式](https://pypi.org/project/localharness/) | **REJECT（今回暫定・現行導入のみ）** | TRINITYと機能重複。移行・権限検証コストに見合う優位の実測なし。 |
| 2026-11-11 | **FlashProve** — [公式](https://github.com/anthropics/FlashProve) | **REJECT（今回暫定・現行導入のみ）** | モデル生成元の証明は研究段階で、現行家庭用環境と導入費用が不釣合い。 |
| 2026-11-11 | **Murmury** — [公式](https://github.com/GianlucaBave/murmury) | **REJECT（今回暫定・現行導入のみ）** | Mac会議補助の用途に偏り、現行AI-Harnessの開発要件と直結しない。 |

再評価は、規約・データ処理条件の変更や、隔離環境での明確な性能優位が確認された場合に限る。
