# AWS Quickの得意分野とAmazon・AWSサービス連携

- Date: 2026-11-22
- Source: AWS公式Quick機能・統合ガイド・AWSサービスコネクター・Amazon Selling Partner発表
- Stage 1: A+
- Stage 2 Final Rank: A（一次資料に基づく機能比較、Freeでの実動作は未検証）
- Evidence: CONFIRMED（公式掲載機能と対象条件）/ UNVERIFIED（個人Free実際の権限・課金・運用効果）
- Decision: CANDIDATE
- Status: KNOWLEDGE / FUTURE VALIDATION CANDIDATE / NOT IMPLEMENTED
- Related proposal: incubator/proposals/2026-11-22-aws-quick-free-plan-pricing.md
- Authorization: B以上の研究候補をGitHubへ保存する継続承認。外部サービス登録、権限付与、実装は未承認。

## 強み

1. 業務データ分析とBI：Quick Sightによる可視化、Athena、Redshift、PostgreSQL、MySQLなど30以上の構造化データ接続が案内される（プラン制約あり）。
2. Quick Flowsによる反復業務、ResearchによるWebと企業知識横断、AppsによるWebアプリ制作、複数Agent協働。
3. Amazon Selling Partner連携：出品者向け在庫、売上、補充発注、Seller Assistant連携。通常のAmazon購入者アカウントで買い物や注文履歴を自由に操作する機能とは別。
4. AWSデータ連携：S3を知識ベースとして検索可能。S3、Bedrock、Textract、Comprehend、Bedrock Data Automation等の直接操作用AWS service action connectorsはQuick Automate限定で、IAMと管理者設定が必要。
5. Amazon Business/Prime Business向けQuick特典の案内あり。ただし一般のAmazon Prime会員特典や日本向け条件と混同しない。

## 無料枠との重要な境界

- 個人向けQuick FreeではChat、Research、Flows、Apps、一般コネクター機能が案内されるが処理量上限あり、具体的月間AI量は未公表/未確認。
- AWSサービスaction connectorsはQuick Automate限定（法人Enterprise相当）。個人FreeからBedrock/Textractを自在に呼べるという意味ではない。
- Quick Sightの高度BIや組織内サービス連携は上位法人プラン中心。
- AWSサービスを別途使うならS3/Bedrock等そのものの従量料金・IAM権限・データ保存条件が独立して発生し得る。
- Amazonの普通の買い物（検索・カート・購入）へQuick Freeが特別な公式アクセスを持つことは確認できていない。

## Harness適合

研究・文書作成・業務データ分析には相性がよい。AWS上に業務データがある場合に特有の価値があるが、現在のHarnessのGitHub、Muse、Codex、家族共有ボードをそのまま代替するものではない。最小試験として個人FreeでResearch、Flows、Appsの実行を行い、Mission Controlで消費量を見る。AWS接続試験は無料・読み取り専用・IAM最小権限を検証後、別途Human承認を得る。

## 一次資料

- https://docs.aws.amazon.com/quick/latest/userguide/what-is.html
- https://aws.amazon.com/quick/integrations/
- https://docs.aws.amazon.com/quick/latest/userguide/working-with-integrations.html
- https://docs.aws.amazon.com/quick/latest/userguide/builtin-services-integration.html
- https://docs.aws.amazon.com/quick/latest/userguide/supported-integrations.html
- https://www.aboutamazon.com/news/innovation-at-amazon/seller-assistant-plugin-amazon-quick-claude
- https://business.amazon.com/en/prime-business/member-exclusives/amazon-quick
- https://aws.amazon.com/quick/pricing/

## Recall triggers
AWS Quick、Amazon Selling Partner、Amazon Business、S3、Bedrock、Textract、Quick Sight、Quick Flows、Quick Automate、AWS service connectors、Free
