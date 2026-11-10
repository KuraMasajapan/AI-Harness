# development追加情報の照合 — 2026-11-07 JST

## 確認範囲と現状

GitHub connectorでdevelopmentを確認。前回参照版
`7ae57c2a089f82e5e232690d8ecb8c257f51ac51`から
`69ba1ae15221bb240bed40a5d5b55316229881a1`まで13コミット、変更13ファイル。
新規提案8件の差分と索引を確認し、特にhunch・Notion・進捗HTMLを精読した。
既存のJev Context Filter提案（未実装）、Efficiency Telemetry、Context Vaultと比較した。
全履歴・全提案本文の網羅監査や、各OSSの実行・上流仕様の再検証ではない。

試行branchは`codex/environment-upgrade-batch1`、HEAD `2431c09`。
開始時の作業ツリーはclean。developmentのpull/merge、branch変更は行っていない。
今回の判定は新しい情報の調査優先順位であり、製品導入・正式採用の決定ではない。

`begin environment-m2-pilot`で再入場し、sourceはCURRENT、4検証は
Runtime changedによるNOT_CURRENTを確認。過去PASSを現環境のPASSとは報告しない。
今回は資料照合のみで、コード検証の再実行は行っていない。

## 次の3件と重複の扱い

### 1. 分類・判断候補の横断比較 — hunchを単独最優先には確定しない

新規性は、同じ選択式判断について教師から学ぶ小型分類器、未学習時の教師復帰、
卒業・監査・降格を組み合わせる点。単なる新しいオーケストレータではない。
Jev/Ollama/Sokudanや決定的ルールと比較する候補に加え、別サービスを重複新設しない。

最初の対象は派生ログのタグ付け候補に限定し、shadow評価で既存判定を維持する。
重要文脈の破棄、検証省略、権限・採用の決定には使わない。
同一入力と独立した正解で少数派失敗の見逃し、教師呼出し率、CPU/RAM、総所要時間、
初期学習・監査負担を比較する。教師との一致は正解精度と同一ではない。

次工程は小さな評価仕様と利用可能なログ種別の特定。
資料の150〜300件案は研究計画案であり、現在のモデル呼出し予算0を増やす指示ではない。
実機での改善と非劣性は未確認。インストール・モデル取得・API呼出しは未実施。

### 2. You-Are-Here — 既存checkpointの表示層として必要部分を組み合わせる

checkpoint/event/receiptは既設なので作り直さない。同じHTMLへの更新、前回との差、
証拠へのリンク、未確認・古い状態・Human判断待ちの可視化だけを候補とする。
既存データから決定的に生成できれば、新たな要約モデルや常駐Agentは不要。

実装に進む場合の最小範囲はoffline・手動更新・派生表示。
公開、hooks、自動refresh、停止イベントの確実性は仮定しない。
まず既存CLI/Markdownと比較し、再開時の再読込とHumanの確認負担を減らせるか評価する。
表示が増えるだけなら見送る。M2実案件の観測と組み合わせる候補。

### 3. Notion共有メモリ — Context Vault案を更新し、接続実装は保留

資料上の新規性は公式のMemories/Skills用MCPと接続主体・権限の明示。
既存GitHub checkpointの代替ではなく、複数AI間の選別された派生文脈として比較する。
各AIの内部状態や全会話が自動統合されると解釈しない。

由来、時点、project/task、信頼区分、訂正・失効、一次記録への参照を保持する設計を
既存Context Vault案と組み合わせる。GitHubを一次保管として維持する。
接続可能性・効果は未確認。二重管理や外部転送の負担が利益を上回れば採用しない。
アカウント接続、権限付与、実文脈の送信、Skill同期は行っていない。

## 残りの新規情報の扱い

| 情報 | 今回の判断 |
|---|---|
| OpenAI 10月公式まとめ | Windows sandboxなどの適用確認の参照。APIキャッシュと現在のCodex利用枠を混同しない。モデル/料金/設定変更前には現行一次資料と環境を別途確認 |
| Desktop AI横断評価 / Orkas | 既存Codex・TRINITY・Hermesと重複。連携の不足が実証されるまで管理層追加を保留 |
| Mercury | Orkas等との重複が大きく、今回の優先3件から除外。scheduled tasksの権限挙動などは資料上の懸念であり実機未検証 |
| OpenShip | 配備・サーバー運用の候補。今回のCodex文脈保持/検証精度に直接必要な基盤ではなく保留 |
| REA 18-repo研究パッケージ | 実案件の調査対象に応じて参照。逆解析ツール群の一括導入は今回不要 |
| Unslop追記 | UI品質の参考。今回の実行安定性・文脈保持の優先改善からは除外 |

## M2との関係

M1実装済み、M2効果未確認、M3未判断という区分は維持する。
新資料の追加だけを理由に設計レビューを再帰的に増やさない。
研究上はhunchを重点候補とするが、短期の実作業評価には既存checkpointの復元と
表示・再読込負担の観測を優先し得る。順番は必要なデータと実証された不足で決める。
元M2の8回は再試行・再採点しない。モデル呼出し予算0 / ready=falseを維持する。

今回変更したのはこの比較記録のみ。実装・性能向上・正式採用を完了とはしない。

## ユーザー訂正を受けた比較対象の補充

2026-11-07: Jevは現行実装ではなく未実装候補。新規追加情報中心の前回比較では、
既存登録の分類・検索候補を十分に含めていなかったため、hunch単独の順位は暫定とする。

| 役割 | 比較候補 | 確認できた範囲 |
|---|---|---|
| 型付き分類・判断 | OpenAI Decisions API / gpt-6-luna、Sokudan、Jev、hunch、決定的ルール | OpenAI公式ガイドを今回閲覧しgpt-6-luna対応を確認。他は保存研究。実環境の比較精度・速度・費用は未確認 |
| 日本語文書の意味検索 | PLaMo-Embedding-1B | agents/Local-AIにCANDIDATE / NOT YET APPROVEDとして登録。埋め込みモデルであり完成したファイル検索サービスではない |
| コード検索・構造探索 | Codebase Memory MCP、CodeGraphContext、Serena、既存rg/AST取得 | 保存研究で比較候補あり。前3者は検索・索引/言語解析ツールであり同種のLLMとは限らない |
| 検索後の絞り込み | Sokudan共通ファイル探索案 | 提案自体がNOT IMPLEMENTED。分類機能が存在することから索引・検索API実装済みとは推論しない |

追加で読んだ保存資料:
`agents/Local-AI/sokudan-ja-310m.md`、`agents/Local-AI/PLaMo-Embedding-1B.md`、
`incubator/proposals/2026-10-25-sokudan-shared-file-discovery-for-hermes.md`、
`incubator/proposals/2026-10-31-codebase-memory-mcp-evaluation.md`、
`incubator/proposals/2026-10-11-coding-context-tool-candidates.md`（Serena部分）。

公式確認: https://developers.openai.com/api/docs/guides/decisions
分類・採点用の型付き判断API。現在の対応model欄はgpt-6-luna。
今回API呼出し・接続・支払い・実装はしていない。

次の比較は製品名単位ではなく、(1)必要箇所の検索・原文取得、(2)限定分類、
(3)復元・表示の3機能で設計する。検索は候補発見、分類は順位づけ、最終判断と
必須検証はCodex/既存機械検証に残す。既存rg等で十分なら追加依存は見送る。
PLaMo等がユーザーの記憶している対象と同一かは未確定。

## 固定参照

以下のdevelopment版に固定。試行branchに未取り込みのためremoteを参照する。

- [追加13コミットの比較](https://github.com/KuraMasajapan/AI-Harness/compare/7ae57c2a089f82e5e232690d8ecb8c257f51ac51...69ba1ae15221bb240bed40a5d5b55316229881a1)
- [hunch](https://github.com/KuraMasajapan/AI-Harness/blob/69ba1ae15221bb240bed40a5d5b55316229881a1/incubator/proposals/2026-11-06-hunch-adaptive-cpu-semantic-decision-candidate.md)
- [進捗HTML](https://github.com/KuraMasajapan/AI-Harness/blob/69ba1ae15221bb240bed40a5d5b55316229881a1/incubator/proposals/2026-11-04-you-are-here-project-map-dashboard-candidate.md)
- [Notion](https://github.com/KuraMasajapan/AI-Harness/blob/69ba1ae15221bb240bed40a5d5b55316229881a1/incubator/proposals/2026-11-06-notion-shared-agent-memory-skills-official-update.md)

既存比較元:
`incubator/proposals/2026-09-21-jev-context-filter-adoption-model.md`、
`incubator/proposals/2026-09-20-efficiency-telemetry-public-metrics.md`、
`research/2026-10-27-context-vault-startup-injection-reference.md`。
