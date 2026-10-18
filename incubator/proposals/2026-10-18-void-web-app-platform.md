# Void — AI開発向けフルスタックWeb基盤（技術選定メモ）

- Date: 2026-10-18
- Status: CANDIDATE / NOT IMPLEMENTED
- Decision: HOLD（現時点で導入不要）
- Scope: 公開Webアプリ / Hosting / Framework / AI-assisted development
- Recall Triggers: Void, VoidZero, Vite, Cloudflare Workers, Vercel, 公開Webアプリ, AIコーディング

## 概要
VoidはVoidZeroが提供する、ViteベースのフルスタックWebアプリ開発・デプロイ基盤。Cloudflareへの公開を簡素化するが、単なるクラウドサーバーではなく、アプリ開発の枠組みも提供する。

## 参照資料
- 利用体験記事（2026-10-17）: https://ashunar0.dev/posts/try-void/
- 公式サイト: https://void.cloud/
- 記事中のサンプルリポジトリ: https://github.com/ashunar0/void-tutorial

## 記事から確認した特徴
- Viteを用い、Next.jsのApp Routerに似たファイルベースのページ・API構成を提供。
- React / Vue / Svelte / Solidを選択可能。Hono・Drizzle・Better Authを活用。
- Cloudflare Workers等へのデプロイを統合し、D1などのデータベースを扱える。
- PostgreSQL / MySQLも選択可能。Node.js / Bun / Deno向けにビルドする経路も説明されているが、Cloudflare専用機能には制約がある。
- 利用バージョンに対応したドキュメントが `node_modules/void/docs/` に同梱され、AIエージェントが参照できる。
- 型生成、破壊的DBマイグレーションへの明示的ガード等、AIによる開発と検証を意識した設計。
- APIの型チェック性能は記事著者による条件付き計測であり、一般的な優位性を保証するものではない。

## Vercelとの位置づけ
- Vercel: Webアプリのホスティング・デプロイを中心とするサービス。
- Void: 開発フレームワークからデプロイまで統合する仕組み。Cloudflareを主な実行先として活用。
- 完全な一対一の代替とは限らず、採用時は実行基盤・対応フレームワーク・DB・運用条件を比較する。

## AI-Harnessで検討する条件
- 一般公開する新規Webアプリに認証・API・DB・サーバー処理が必要になったとき。
- Codex等によるAI支援開発で、バージョン整合したドキュメントと明示的な型チェックが価値を持つとき。
- 静的HTMLやGitHub Pagesで十分な用途には導入しない。
- 導入前に、料金・無料枠・ロックイン・データ保護・運用負荷・安定性・代替案（Vercel / Cloudflare直利用等）を確認する。

## 評価と境界
- Research status: CANDIDATE（将来の公開Webアプリ技術候補）
- Implementation: HOLD / NOT IMPLEMENTED
- 現在のAI-Harness Core、Trinity、既存プロジェクト構成は変更しない。
- この記録は採用決定や実装許可ではない。具体的な採用・GitHub変更は別途Human承認を得る。
