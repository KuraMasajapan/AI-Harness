# AWS Quick（旧Amazon Quick）無料枠と課金条件の調査

- Date: 2026-11-22
- Origin: https://quick.aws.com/sn
- Product: AWS Quick（2026年11月時点）
- Stage 1: A+
- Stage 2 Final Rank: A+（公式料金・利用案内で主要条件を確認、個人Freeの月間AI使用量の数値は不明）
- Evidence: CONFIRMED（AWS公式料金・規約・ユーザーガイド） / UNVERIFIED（実アカウント固有の制限・無料試用キャンペーン適用・実運用能力）
- Decision: CANDIDATE
- Status: KNOWLEDGE / FUTURE VALIDATION CANDIDATE / NOT IMPLEMENTED
- Authorization: Humanの「B以上の研究成果は保存まで作業完了」の継続指示。アカウント登録・接続・実装・有料プラン申込は未承認。

## 何のサービスか

AWS Quickは、AIチャット、Research、Flows、Webアプリ作成、ファイル/外部サービス連携、継続的エージェント業務などを統合するAIワークスペース。2026-11-20公式更新でブラウザを閉じた後もエージェント作業継続、複数エージェント協働、Web上のSkills、追加MCP連携、日本語対応を発表。

## 個人向け（メール・SNSで直接登録、AWSアカウント事前作成不要）

| プラン | 月額 | 人数 | 索引容量 |
|---|---|---|---|
| Free | $0 | 1 | 1GB |
| Plus | $20/人（年払い）または$25/人（月払い） | 最大300人 | 10GB/人 |
| Max | $100/人（年払い）または$125/人（月払い） | 最大300人 | 50GB/人 |

FreeにはAIチャット、Deep Research、Flows、Webアプリ作成、Spaces、コネクターやアクション、デスクトップアプリが掲載されている。ただしチーム共有Spaces等は有料プラン限定。個人向けのインフラ月額固定費は無し。

最重要：**個人FreeのAI処理量の月間具体数値は料金表に明記されていない**。月間制限とローリング・セッション制限が存在し、計算量、モード、モデルで消費が変わる。処理上限を「1時間」等と断定しない（1時間や2027-01-31までの3時間は法人向けEssentialsの枠）。

公式によると追加使用量（overage）は初期状態OFF。自分で有効にしたとき月間支出上限を設定し、上限到達で停止する。Freeのセッション上限到達は回復待ち・アップグレード、月間上限到達は翌月リセット待ち・アップグレード。未使用枠の繰越なし。料金表には索引容量超過$5/GB/月の表示もあり、課金はoverage設定の有無を確認する。

新規登録者へ30日Plus試用の公式User Guide案内があり、2026-11-20公式ブログに3か月無料体験・最大10人招待の新キャンペーン表示もある。どの対象に3か月が適用されるか、30日との関係、試用終了後の移行先・支払設定は登録画面確認が必須。法人向けEnterprise30日無料試用は別プログラムで、期間満了後に課金が始まると公式料金表が明記。

## 法人向け（AWS Management Consoleから登録）

Essentials $3/人/月 + $250/アカウント/月：月1 agent-hour、2027-01-31まで月3時間、索引1GB/人。
Professional $20/人/月 + $250/アカウント/月：月8 agent-hours、25GB/人。
Enterprise $40/人/月 + $250/アカウント/月：月18 agent-hours、50GB/人。
法人の追加agent-hour $3/時間、索引容量超過$5/GB/月など。個人の無料プランと混同しない。

## 個人Freeの注意事項・費用リスク

- 登録はGoogle/Apple/GitHub/Amazon/メール。AWS側で管理用アカウントを背後で作成する仕組み。
- Plus・Maxの支払情報登録・アップグレード・年払いは自動課金条件に注意。年払い契約は途中キャンセル不可（終了時切替）・返金なしと公式案内。
- 個人向けFree/Plus/Maxには組織向けQuick API公開機能（AWS Console登録側に限定と案内）はなく、単体で外部から自由にAPI呼び出しできる無料推論基盤ではない。
- 公開Appsの利用量はアプリ所有者のサブスクリプション枠を消費するため、公開先から大量アクセスされる用途には慎重。
- 外部アプリ連携の権限とデータ取扱い、依存、継続性、日次/定期ジョブの消費は要検証。

## AI-Harnessとの関連

FreeのResearch、Flows、Webアプリ制作、Skills、Web/デスクトップ/モバイル同期、Cloud実行、複数AIのオーケストレーションはAI-Harness・TRINITY・家族のMuse/共有ボード構想との比較候補。ただし無料枠数値が不明で常時運用・無制限実行・自前VPS代替には使えない。既存Codex/ChatGPT/Museの構成を未評価のまま置換しない。

## 最小検証（未実施）

1. 個人Freeへ新規登録する場合、試用表示、期限、支払い方法・overage初期OFFを確認。
2. Plan & Billingで現在の料金状態、支払方法、試用終了日、推定請求、追加利用OFFを確認。
3. Mission Controlで月間/セッションの消費と回復を実測、短いResearch・1回のFlow・小アプリ生成を試す。
4. ブラウザを閉じた後のタスク完了を検証、プランごとの残量を記録。
5. 外部API・MCPとの入出力、権限、データ保存、外部公開アプリの使用量計測をテストして、既存のAI-Harnessと比較する。

## 公式一次資料

- https://aws.amazon.com/quick/pricing/
- https://docs.aws.amazon.com/quick/latest/userguide/standalone-plans.html
- https://docs.aws.amazon.com/quick/latest/userguide/standalone-usage.html
- https://docs.aws.amazon.com/quick/latest/userguide/standalone-billing.html
- https://docs.aws.amazon.com/quick/latest/userguide/standalone-signup.html
- https://docs.aws.amazon.com/quick/latest/userguide/standalone-upgrade.html
- https://aws.amazon.com/blogs/machine-learning/new-in-aws-quick-more-capable-flows-an-updated-web-experience-and-agents-that-work-together/

## Recall triggers

AWS Quick、Amazon Quick、Quick Suite、quick.aws.com、Free、Plus、Max、agent-hours、Flows、Research、Apps、無料利用枠、overage、試用期間、2026年11月
