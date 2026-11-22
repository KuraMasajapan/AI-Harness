# Sign in with ChatGPT (SIWC) — オープンソース向けChatGPTプラン利用

- Date: 2026-11-22
- Source: https://developers.openai.com/siwc/token-sharing-open-source
- Source type: OpenAI公式Developer Docs（Overviewの原文を直接取得）
- Stage 1 Rank: A++
- Stage 2 Final Rank: A+（公式仕様は確認、AI-Harnessへの実装適合性は未検証）
- Evidence: CONFIRMED（公式仕様の存在・概要） / UNVERIFIED（対象アカウントの資格、実機での使用可否・効果）
- Decision: CANDIDATE
- Status: KNOWLEDGE / FUTURE VALIDATION CANDIDATE / NOT IMPLEMENTED
- Authorization: Humanの「B以上を保存まで評価作業完了」の継続指示による研究候補保存。実装・接続・認証情報取得・本番導入は承認されていない。

## 原文の主旨（Overview）

Sign in with ChatGPT (SIWC) における「ChatGPT plan usage」は、本人が同意したオープンソース・ローカルホスト型アプリが、対象のResponses API呼び出しで本人のChatGPT契約の利用枠を使う機能。通常のAPIキー・別課金方式と異なる選択肢。ただし対象モデル/上限/権限の制約があり、無制限使用ではない。これによってChatGPTの会話履歴やその他アカウント文脈へのアクセス権が付与されることはない。

公式ドキュメントの対象はOSS・ローカルホスト型アプリ。課金アプリやリモートホスト型製品は別途interest formで申請するよう案内。

### ClientとHostの区別

- Client: OAuth登録を表す発行済みclient_id。ユーザー・登録時のワークスペースと紐付き、権限やプラン利用設定に関係。
- Agent host: ノートPC、デスクトップ、セルフホストVMなど個別の実行環境。アプリが定義するライフサイクルにわたり安定したext_agent_host_idを保持。
- 同一ユーザー・同一ワークスペースの単一client_idを複数ホストで再利用可能。ただし各hostは一意のhost IDが必要。
- host IDの推奨はRFC 9278によるJWK thumbprint URI。UUIDv4からのurn:uuid:形式、did:keyも対応。個人を直接識別するメール/ユーザーIDを埋めない。公開鍵由来のIDでも、現時点では秘密鍵の所有証明を検証する仕組みではない。

### 最初の推論まで

ホストIDを作成・永続保存 → ブラウザによるサインイン、client登録、ChatGPTプラン使用への同意 → authorization codeをOAuth tokenへ交換 → ID tokenと許可されたscopeの検証 → 必要情報・credentialを安全に保存 → access tokenでResponses API request、ストリームを完了まで処理。再ログイン時は保存されたclient IDを再利用。

公式ドキュメントにはUI/UX、sign-in、accounts/sessions、models/inference、Codex app-server、self-hosted VMs、token reference、error recovery、preview limitationsの詳細ページあり。

## AI-Harnessとの関連性

- AI-HarnessのローカルOSSエージェントとChatGPT Plus利用権の統合研究に直接関係。
- Codex CLI/app-serverや複数ホスト間の認証管理と、既存のACCESS/WORKFLOW/Trinityのusage計測を比較する価値が高い。
- 単一のアカウント契約を複数ホストで使用できる可能性と、ホストごとの追跡・制御の限界を分けて評価する。
- サービスや接続を常時稼働させるだけで無料無制限APIに変化するわけではない。

## 安全性・制約

- OAuth access/refresh tokenは秘密情報。ChatGPTパスワード・セッションCookieをアプリへ入力しない。
- 認証情報・永続トークンの格納場所は規約と公式ガイドに従って慎重に扱う。GitHub・公開ログ・会話に記録しない。
- OpenAI公式Terms：https://openai.com/ja-JP/policies/sign-in-with-chatgpt-terms/
- SIWCのPreview limitationsやResponses API必須パラメータについては個別文書を確認。汎用APIのすべてのモデル・ツール・機能に適用可能と見なさない。
- 現在のユーザーPlusアカウントに実際に権限があるか、外部から残量を取得できるかは本資料からは断定できない。
- ローカルOSS向けの規定と、クラウドVMへの資格情報転送ガイドは存在するが、任意のクラウドサービスの商用・リモート運用を包括許可するものではない。

## 最小検証（研究案・未実施）

1. Sign in/Preview limitations/Termsで対象アプリ、利用許可、対応モデル、上限、資格情報の保存要件を確認。
2. テスト用ローカルOSSで正規OAuthフローから接続し、一度だけ低負荷のResponses API streamingを実行。
3. モデル一覧、usage、上限到達、更新/失効、再ログインを確認。
4. 複数ホスト識別とトークン管理を検証する場合は個別のセキュリティレビューを先に行う。
5. 既存のAPIキー方式、Codex CLI既存ログイン、クラウドAPI従量課金と比較し、採用前にHuman承認を求める。

## Recall triggers
SIWC、Sign in with ChatGPT、Token Sharing、ChatGPT plan usage、OAuth、ext_agent_host_id、client_id、Codex app-server、Responses API、OSS、ローカルエージェント、API料金
