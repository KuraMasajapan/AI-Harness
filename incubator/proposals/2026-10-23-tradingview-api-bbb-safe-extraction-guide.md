---
document_type: research_evaluation
date: 2026-10-23
title: "TradingView-API — BBB research archive and safe extraction guide"
origin: "Human-shared X post; Human explicitly approved research archive plus usage guide"
source_post: "https://x.com/bkdgiffug/status/2113312677129068746"
source_repository: "https://github.com/Mathieu2301/TradingView-API"
stage_1_rank: A+
stage_2_rank: B
evidence_status: "X POST AND OFFICIAL REPOSITORY VERIFIED; OPERATIONAL BENEFIT UNTESTED"
decision: HOLD
implementation: NOT APPROVED
scope: "AI-Harness cross-project research / BBB reference (not BBB implementation)"
tags: [bbb, tradingview, unofficial-api, backtest, forward-validation, data-provenance, compliance, research-only]
---

# TradingView-API — BBB研究記録と安全な知見抽出ガイド

## 0. この記録の位置づけとHuman承認
2026-10-23、Humanが調査内容全体を将来参照可能な形で保存し、**利用できる部分を抽出するための「使用ガイド」**を付けることを明示承認。本ファイルはResearch/Proposal Incubatorへの**記録のみ**。BBBのソース、設定、戦略、注文、Risk Gate、データ供給元、Core、Trinityを変更しない。TradingView-APIや依存パッケージをインストールせず、TradingViewへの非公式接続も実行しない。HOLDは情報保存を妨げないが、採用・接続・実運用許可を意味しない。

## 1. 発見元：X投稿（独立した性能証拠ではない）
- 投稿者: @bkdgiffug、2026-10-22
- 原文: https://x.com/bkdgiffug/status/2113312677129068746
- 参照先: https://github.com/Mathieu2301/TradingView-API
- 主張: リアルタイム相場と指標、Premium機能、招待制・私有指標、数量制限のない取得、戦略バックテスト、無料アカウントでReplayが使え、Botやアラートに利用できるという宣伝。
- **主張のうち「Premium機能を無料・無制限に使える」「招待制指標を権限なしで読める」という解釈は確認されておらず、採用理由にしない。** 投稿は発見Signalであり、許諾・安定性・有益性の証明ではない。

## 2. 公式Repositoryで確認した仕様（2026-10-23調査）
- 独立コミュニティ製プロジェクトであり、TradingView公式APIではない。
- v4はTypeScriptによるbreaking rewrite。デフォルトnpmはv4、v3のClient APIとは互換でない。
- データAPI: `getCandles` / `watchCandles` / `getQuote` / `getIndicatorData` / `searchMarkets` / Screener等。チャート・指標・Strategy reportのインターフェースあり。
- Backtest API: `@mathieuc/tradingview/backtest`。READMEは凍結したローソク足、先読み拒否、次バー始値エントリー、両方向手数料・スリッページ、保守的な約定判定、IS/OOS分離、seedを固定したランダムエントリー基準等を説明。
- Low-level API: chart/session、studies、replay、raw packet等。
- ログインなしでは短い日中履歴・Pine study利用不可や遅延/代替feedの可能性。アカウントを使う際は`sessionid`と`sessionid_sign`等の認証情報が関わる。README自身がアクセスできる範囲はアカウント権限に従う旨を説明。
- READMEは収益性を保証せず、利用者にプロバイダー規約と市場データ権利の確認を求めている。
- 公式資料: https://github.com/Mathieu2301/TradingView-API/blob/main/README.md 、https://github.com/Mathieu2301/TradingView-API/tree/main/docs
- 上記は**READMEが説明する機能**の確認であり、BBB環境での動作、精度、過負荷耐性、継続稼働、セキュリティ監査を実証していない。

## 3. 最重要：TradingView利用制限
2026-10-23確認のTradingView公式ポリシー:
- 日本語: https://jp.tradingview.com/policies/
- 英語: https://www.tradingview.com/policies/
- アカウント停止ヘルプ: https://jp.tradingview.com/support/solutions/43000674726/

公式規約はTradingViewコンテンツ・市場データの非表示目的利用、アルゴリズムによる意思決定、自動売買、価格参照や注文検証、その他の非表示機械処理を禁止すると明記。公式ヘルプはスクリプト/API/スクレイピング等の自動収集について警告し、違反時の一時・恒久停止を説明。

**研究用にコード設計を読むこと**と、**TradingViewサービスに接続してデータやPremium/私有指標を抽出すること**を厳格に分ける。OSS公開・npmからの入手可能性は、利用規約に対する許諾の証拠ではない。規約回避、Cookieの不適切な利用、権限制限の迂回、TradingViewデータのBBB自動判断への入力は本提案の対象外。将来の正式なライセンス/明示許諾が確認されない限り接続しない。規約は変更され得るため導入判断時は最新版を再照合する。

## 4. BBBへの関連性（Stage 2）
| 領域 | 研究価値 | 扱い |
|---|---|---|
| bitbank BTC/JPYの一次データ | B | bitbank Public APIが既存。置換不要 |
| RSI等の指標計算 | A | 算式やデータ条件の**設計比較**のみ。TradingView値の自動取得なし |
| 取引所間データ品質 | A+（課題として） | 比較するなら権限の明確な別取引所APIを使用。BTC/USDTとBTC/JPY、時刻、為替、出来高は直接同一視しない |
| Backtest設計 | A+ | 先読み、約定、コスト、IS/OOS、再現性の**実装原則**を抽出可能 |
| Replay/Forward | A | 既存BBBのReplay Lab / Training Lab / Forward Gateと検証観点を比較 |
| 注文執行/自動売買 | C | 不要。接続・移植禁止（別途Humanと適法なデータ利用確認が必要） |

現時点のBBB既存機能として、bitbank Public API、Training Lab、Replay Lab、Forward Gate、Research Champion、Paper運用などがある。**最新のBBB Source of Truthを開発時に再取得**し、下記の項目が実際に不足しているか判定すること。既存機能があれば重複導入しない。

## 5. 使用ガイド — 「全体を残し、使える部分だけを抜き出す」
### A. 可：外部データを取り込まず、アイデアだけを抽出
1. 公式README、`docs/backtest.md`、tests等の**公開ソース**を読み、バックテスト上の設計意図と失敗条件をメモする。
2. BBBの既存Replay / Training / Forward仕様と横並びにして、「Already present / Partial / Missing / Unverified」に分類する。
3. 特に以下の候補を監査する。
   - 将来データ混入・look-ahead rejection
   - 信号確定時点と**次の取引可能足**の約定時点
   - 手数料、bid/ask spread、slippage、最小注文量、丸め
   - 保守的な同一バー利確/損切り判定
   - Train/Validation/Forwardの時間境界、データ漏洩
   - 比較用のseed固定ランダムエントリー・Buy & Hold
   - データ欠損、時刻粒度、タイムゾーン、出来高、価格通貨の一致
   - 同一データでの独立再計算と一致許容差
4. **TradingViewから市場データや指標データを取得せず**、bitbank等の許諾されたデータと独立実装のテストコードで小さく再現する。
5. 差分が本当にある場合のみ、BBB開発チャットに「改善候補」として引き渡す。Research Championや設定への反映は別途Human承認。

### B. 条件付き：コードの再利用
- コード再利用にはRepository/個別ファイル/依存パッケージのライセンスと第三者権利を**別途確認**する。2026-10-23のGitHubリポジトリmetadataではlicense=nullであり、この調査では包括的な再利用許諾を確定していない。
- ライセンス未確認でコードをコピー・改変・配布・BBBへ組み込まない。
- READMEのAPI/Backtest説明は機能の発見源であり、BBB実装への無条件コピー指示ではない。
- 公開された一般的な設計パターンを独立実装して検証する場合も、元コードの複製と混同しない。

### C. 不可（現在）
- 非公式TradingView接続の試行、Cookie/session情報の投入、Premium/招待制データの取得、TradingView指標をBBBの売買・リスク判断へ送信すること。
- 投稿の「無制限」「無料」を根拠にした非表示自動収集。
- BBBの実資金注文、戦略・閾値、現行Core/Trinityの無断変更。

## 6. 最小検証案（まだ実行しない）
- 入力: 同一期間・同一タイムフレームの、既存の正当に利用できるbitbank BTC/JPY足を凍結。
- A: 現在のBBB Backtest / Replay計算。
- B: 上記の一般的な仕様から**独立して作成した簡易検証器**（権利確認のないOSSコードは流用しない）。
- ケース: 正常系、欠損足、極端なspread、手数料変更、同バー両側到達、future leak、タイムゾーン差、足境界、無取引。
- 比較: trades、entry/exit時刻、fee、PnL、Max DD、PF、Buy & Hold、IS/OOSとForwardの分離、ログ根拠。
- 合否: 差異を理由付きで説明できること、未来参照がないこと、正当に入手したデータだけを使うこと、実資金へ一切影響しないこと。
- 負担見積り・作業開始・BBB実装は後続の開発判断に委ねる。

## 7. 既存Proposal照合・保存判断
2026-10-23、`development/incubator/proposals/` の既存候補ファイル名を確認。「TradingView-API」を主題とする独立ファイルは見当たらなかった。関連する候補群とは目的を分離し、本稿はBBB研究に使う「外部OSS・規約・安全な知見抽出」の参照記録とする。

- Stage 1: **A+**（BBBに関係する強い探索Signal）
- Stage 2: **B**（機能の存在を確認したが利用制限が厳しく、BBBへ直接採用不可。方法論は参考になる）
- Evidence: **公式README確認済 / 効果未実証 / 権利許諾未確認**
- Decision: **HOLD — Research reference only**
- 保存価値: X投稿の強い宣伝文句に惑わされず、**有用な方法論と不可なデータ取得を切り離す**判断を将来再利用できる。
- Human承認: 研究内容全体の保存および使える部分の抽出ガイドの併記のみ。実装には拡張しない。

## 8. Recall triggers
TradingView-API, Mathieu2301, TradingView unofficial API, BBB, backtest independent verification, look-ahead bias, execution reality gap, Replay Lab, Training Lab, Forward Gate, source license, non-display data, market data compliance, backtest safe extraction.
