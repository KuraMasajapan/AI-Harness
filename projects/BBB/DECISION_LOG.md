# BBB Decision Log

## 2026-09-29

### Project start
- 正式名称を **BITBANK-BOT** と決定。
- 略称を **BBB** と決定。
- 取引所を **bitbank** と決定。

### Core philosophy
- 最初はAI取引の検証を目的とする。
- 常時多数のAIエージェントを動かさない。
- 古典的なBotを常時稼働の土台とし、将来AIは必要時のみ利用する省エネ構成を目指す。
- Humanとの常時ホットラインなしでも、将来的に記録・評価・改善を自動化する。

### Development ownership
- 初期構築はSOLで進める。
- Codexはゲーム開発が落ち着いた後、BBB完成版の独立監査役として利用予定。

### Exchange integration
- bitbankとの接続の基本層は **CCXT** を採用。
- 販売所経由ではなく、取引所の現物板取引を前提とする。
- bitbank公式APIドキュメントをAPI仕様のSource of Truthとする。

### Phase 1
- エージェントなしBotから開発開始。
- BTC/JPYを初期対象とする。
- 現物のみ。
- 空売りなし。
- レバレッジなし。
- Paper Tradeを先行。
- EMA + RSI を基準戦略とする。
- 基準戦略は最終戦略ではなく、将来の改善効果を測るBaselineとして扱う。

### Validation
- Backtestを導入。
- Live Paper Tradeを導入。
- Historical Replayを導入。
- 過去相場は未来情報を見せず時系列に再生する。
- Buy & HoldをBaseline比較対象にする。
- 手数料・スリッページ・最大ドローダウン・勝率・Profit Factor等を評価対象にする。

### Improvement loop
- Agentless Learning Loopを導入。
- EMA/RSIパラメータ候補を自動探索する。
- 時系列Fold + unseen Holdoutを使う。
- Research Championの更新は自動化可能とする。
- リスク上限は自動最適化対象にしない。
- 同一データセット再利用による安易な昇格を抑止するためDataset SHA-256を記録する。
- Research Championから実資金Liveへの自動昇格は禁止。

### JPY / FX issue
- BTC/JPYにはUSD/JPYの為替影響が混ざることを重要課題として採用。
- 判断用にBTC/JPY ÷ USD/JPYを利用できるFX-aware構造を実装。
- 実際の損益評価はJPY建てで維持する。
- 異なるSignal Basisで学習したChampionを、同じ参照データ無しにPaperへ流用しない。

### Security
- API Key / SecretをChatGPTへ貼らない。
- API Key / SecretをGitHub / AI-Harnessへ保存しない。
- 将来Live時はPC側の環境変数またはSecret Storeで保持。
- BBB用APIには出金権限を与えない方針。
- 実注文開始前にLive Trading Gateを設ける。

### Logging policy
- BBBの重要決定・仕様変更・検証状態をAI-Harness内にも継続記録する。
- 秘密情報と大量の実取引生ログはHarnessへ直接保存せず、要約・Checkpoint・検証結果を記録する。

### v0.6 immediate-use direction
- 「すぐ使えるものに仕上げて渡し、そこから学習を続ける」方針を採用。
- Windows向けDesktop Research Consoleを追加。
- BBB_START.batから初回環境構築と起動を行う。
- Desktop shortcut installerを追加。
- native shellが使えない場合はlocalhost browser consoleへfallbackする。
- 継続学習をアプリ起動中に定期実行できるようにする。
- 新しいトレード手法を一つずつ手作業で差し替えるのではなく、複数Strategy Familyを同じ検証Gateで競わせるStrategy Labを採用。
- 初期Strategy Family: EMA+RSI / EMA Cross / Breakout / Mean Reversion / Momentum。
- Strategy Lab ChampionはPaperへ自動反映可能。ただしLiveへは自動反映しない。

### v0.7 UI / UX Lab
- Human決定: 過剰でもよいので便利機能とUI/UXを積極的に試す。
- Desktop Research ConsoleをTrading Research Cockpitへ拡張。
- 4画面構成: Dashboard / Training Lab / History / Risk & System。
- bitbank Public OHLCVのローソク足表示を追加。
- Paper資産曲線、Return、Max Drawdown、判断回数、Fill、Error等の可視化を追加。
- Strategy Familyカード、Research Jobタイムライン、Operational Readinessを追加。
- Ctrl+Kコマンドパレット、Toast通知、キーボード画面切替を追加。
- 監査Snapshot JSON書き出しを追加。
- UIの便利さを積極的に追求する一方、Live安全境界は別管理し固定する。

### Fundamental Sentinel concept
- GPUなしPCで動く小型Local AIを、BBB専属のファンダメンタルズ文脈整理エージェントとして検討する。
- 情報取得はAPI / deterministic collectorで行い、Local AIへWeb探索そのものを主担当させない。
- Actual / Forecast / Previous等の単純な数値判定はアルゴリズムで処理する。
- Local AIはニュース・声明文の要約、カテゴリ分類、hawkish/dovish、risk-on/risk-off、BTC/JPY関連度、重要度、不確実性等の文脈処理を担当する。
- Local AIはBUY / SELLを直接命令しない。固定Schemaの構造化信号だけを返し、BBB側のFundamental Policy EngineがRisk調整等へ変換する。
- 判断不能時のUNKNOWN / no_overrideを正式な正常系として扱う。
- Local AI停止時もBBB本体を継続可能にし、AIなしFallbackを持たせる。
- 初期はFundamental AI Sandboxとして観測専用運用し、売買へ反映しない。
- Local AI判断とその後のBTC/JPY・USD/JPY等をFundamental Confidence Ledgerへ蓄積し、カテゴリ別にAIの有効性を検証する。
- 将来Cloud AIを利用する場合も常時稼働させず、Local AIで処理困難な案件のみエスカレーションする。
- BBBの利益が確認できた場合、利益の一部を高度なCloud AI利用費へ回すSelf-Funding AI構想を検討する。
- 機能進化と実資金運用信頼性は引き続き別軸で評価する。

## 2026-09-30

### v0.8 Local AI Sandbox implementation
- Sokudan `GeneLab/sokudan-ja-310m` をBBB Local AIの最初の実装候補としてSandbox統合。
- Local AIは別ローカルプロセスで起動し、BBBと同時にauto-start可能とする。
- GPUなしWindows PCを前提にCPU実行。
- Local AI導入は任意。未導入・Loading・Offline・ErrorでもBBB本体は継続。
- Local AI分類結果は現時点でPaper / Live / Riskへ一切接続しない。
- 固定Schema: category / importance / BTC relevance / FX relevance / risk bias。
- 自由生成ではなく、Sokudanのtyped outputを利用する。
- Sandbox結果はローカル `data/local_ai/fundamental_sandbox.jsonl` に保存。
- Risk & SystemへLocal AI状態カードと自己テストを追加。
- 一回限りの `BBB_LOCAL_AI_SETUP.bat` と診断BATを追加。
- v0.8 package local test: 33 pytest PASS / compileall PASS / UI JS syntax PASS。

### v0.8.1 Local AI Python compatibility fix
- Target PCの初回セットアップでSokudanのPython互換性エラーを確認。
- Sokudan v0.3.0の対応範囲はPython >=3.11,<3.14。
- BBB本体とLocal AIを同一venvへ入れる方針を廃止。
- BBBは `.venv`、Sokudanは `.venv_local_ai` へ分離。
- Local AI setupはPython 3.13 -> 3.12 -> 3.11の順で探索する。
- 対応Pythonが無くwingetが利用可能な場合、Human確認後にPython 3.13導入を提案する。
- BBB本体の既存環境は変更しない。
- Local AI Managerは専用PythonからSokudan serverを起動する。
- Sandbox / trade influence OFF / Live Lockedの境界は変更なし。

### v0.8.2 Local AI setup robustness
- Target PCで `py -3.13` が見つかりvenv作成まで成功した後、v0.8.1のPython判定が停止する事象を確認。
- v0.8.1セットアップ判定を堅牢化するため、Launcher名ではなく対応Pythonの `sys.executable` 実体パスを解決してvenv作成する方式へ変更。
- 作成後にLocal AI Python実バージョンを画面・ログへ表示。
- 既存 `.venv_local_ai` はセットアップ時に再作成する。
- 初回Local AI導入の正式順序を `BBB終了 -> Setup -> BBB起動` と明記。
- v0.8.2 package validation: 33 pytest PASS / compileall PASS / UI JS syntax PASS / BAT static check PASS。

### v0.8.2 target PC install success
- Target Windows PCでLocal AI専用環境の作成に成功。
- Compatible Python: `C:\Users\Owner\AppData\Local\Programs\Python\Python313\python.exe`
- Local AI Python: `3.13.15`
- `.venv_local_ai` 作成成功。
- Sokudan Local AI installation verification PASS。
- BBB本体とSokudanは分離Python環境で運用。
- 次工程: `BBB_START.bat` 起動後、初回モデル重み取得とLocal AI READY / self-test確認。

### Local AI target runtime READY
- Target Windows PCでBBB v0.8.2起動後、Sokudan Local AIが `READY` へ到達。
- Model: `GeneLab/sokudan-ja-310m`
- Sokudan package: `0.3.0`
- Device: CPU
- Local AI自己テスト実行成功。
- UIで観測したLast Inference: 1689 ms。
- Sandbox / Trade influence OFFを維持。
- 次工程は外部Fundamental Data Collector / RSS・API取り込み。現v0.8.2のLocal AI self-testは固定サンプル文章を直接Sokudanへ渡すだけで、汎用外部API collectorは未実装。

## 2026-10-01

### v0.8.3 Fundamental Data Collector
- Local AI実機READY / Self-Test成功後、実データ入力経路を実装。
- BOJ News RSS と BOJ Statistics RSS を公開Feedとして追加し、日本語項目をSokudanへ自動分類。
- Federal Reserve Press RSS を追加。Sokudanは日本語向けとして扱うため、現段階ではCollect Only。
- 既定15分poll。UIのData Sources Hubから手動取得も可能。
- Feed項目はSHA-256 IDで重複排除。
- 初回Feed大量投入を避けるため、各Sourceの最新2件のみ処理対象とする。
- Local AIがLOADING / OFFLINEの場合、分類待ちを保存しREADY後に再試行。
- Data Sources Hub / Fundamental FeedをRisk & Systemへ追加。
- FREDはData Sources Hub上でNOT_CONFIGURED / PLANNEDとして明示。構造化Macro APIは次工程。
- Fundamental情報はSandbox観測専用。Paper / Live / Riskへの影響OFF。
- v0.8.3 package validation: 38 pytest PASS / compileall PASS / UI JS syntax PASS / BAT static check PASS。

### v0.8.3 target collector verification
- Target Windows PCでFundamental Feedの実データ取得を確認。
- BOJ Statistics RSS / BOJ News RSSの項目がSokudanで分類され、category / importance / BTC relevance / biasがUIへ表示された。
- Federal Reserve Press RSSは設計通り `collect_only` で保存された。
- Local AI未READY時に取得されたBOJ項目が `local_ai_not_ready` として残り、後続のREADY後分類結果と同一項目が別行で表示される重複を確認。
- 次修正候補: pending classification完了時に既存Feed行を更新/統合し、同一event_idの重複表示を防止。
- 次修正候補: BBB終了時にSokudan child processを確実に終了するLifecycle cleanup。


### v0.8.4 Cleanup + Fundamental Replay Lab α
- v0.8.3実機確認で見つかったFundamental Feed重複表示を修正。監査用feed_events.jsonlはappend-onlyを維持し、UI Current Viewだけevent_id単位でmergeする。
- Local AI未READYで取得したイベントが後から分類成功した場合、別ニュースではなく同一イベントの状態更新として扱う。
- BBB終了時に、自分で起動したSokudan processを明示停止する。Windowsではprocess tree停止をfallbackではなくowned processの標準shutdown pathへ組み込む。
- 緊急停止補助として BBB_STOP.bat を追加する。
- Fundamental分類Schemaを bbb-fundamental-v2 とし、financial_markets を追加。為替・国債・決済・流動性等をcrypto_marketから分離する。
- 分類記録へSchema version / SHA-256を保存し、将来のCase Studyでschema差分を比較可能にする。
- Fundamental Replay Lab αを追加。BBBが実際に観測した recorded_at をknowledge timeとして、その後のBTC/JPYを5m / 30m / 1h / 4h / 24hで照合する。
- 未来horizonがまだ存在しない場合はnullとして保持し、未来情報を補完しない。
- Replay結果は data/fundamental_replay 配下のmarket dataset / confidence ledger / reportへ保存する。
- Replay / Local AI結果は引き続きSandbox only。Paper / Live / Risk / Championへの自動影響はOFF。
- v0.8.4 package validation: 43 pytest PASS / compileall PASS / UI JavaScript syntax PASS / BAT label check PASS。

### v0.8.4 target Local AI recovery
- v0.8.4展開後、一時的にLocal AIが `NOT_INSTALLED` 表示となった。
- `.venv_local_ai` フォルダ自体は存在していたが、BBB側から有効なLocal AI環境として認識されなかった。
- `BBB_LOCAL_AI_SETUP.bat` でLocal AI専用環境を再構築。
- 再構築後、Target Windows PCでLocal AIが `READY` へ復帰した。
- data保持のまま再セットアップで復旧可能であることを確認。

### v0.8.4 first Fundamental Replay target run
- Target Windows PCでFundamental Replay Lab αの初回試運転に成功。
- UI表示: Observed Events 16 / Classified 14。
- 1h bias alignment: 84.6% (n=13, risk_on / risk_offのみ)。
- Replay結果ファイルが `data/fundamental_replay/run_*/confidence_ledger.jsonl` に生成されたことをUI上で確認。
- この84.6%は標本13件の初期観測であり、性能証明として扱わない。過去イベント大量投入によるCase Study拡張が次工程。

### v0.8.5 Historical Fundamental Import + Skin System
- Human要望により、Fundamental Replay Case Studyを過去データへ拡張。
- 最初のHistorical SourceはBOJ公式年別アーカイブとする。
- 対象: 金融政策に関する決定事項等 / 金融政策決定会合における主な意見 / 講演・挨拶等 / 記者会見。
- UI初期値は2025年、最大100件。Source間で偏りすぎないようround-robinで候補を選ぶ。
- 過去EventはLive Feedと別ファイルへ保存し、SokudanでSandbox分類する。
- Archiveで保証されるのが日付のみの場合、正確な公表時刻を捏造しない。knowledge_atは当日23:59:59 JSTへ保守的に置き、date-only Eventは5m/30m/1h/4hを未評価とする。
- 初期Historical ReplayはBTC/JPY 24h reactionを評価する。
- UI Skinは4種すべて採用: Aurora Light / Sunrise Gold / Midnight / Sakura Tech。
- Skinは画面右上で切替、localStorageへ保存。初回既定はAurora Light。
- 主要UIをEnglish / 日本語併記へ移行。和訳はHuman Reviewで随時修正可能。
- Safety boundaryは変更なし。Historical Import / Replay / Local AIはPaper / Risk / Liveへ影響しない。
- v0.8.5 package validation: 48 pytest PASS / compileall PASS / UI JavaScript syntax PASS / BAT label check PASS / packaged ZIP再展開後48 tests PASS。
- package SHA-256: 8d9a946c5ca8084a169bdb743801f563c1a6464358bdbcc8b5ad7ded5f4aefbf。

### v0.8.6 Run Timing + Calm Skin refinement
- Human要望: Historical Import / Replay等の実行開始から完了までの経過時間を計測したい。
- 全background jobにelapsed_secondsを追加。running中は現在時刻との差分で動的更新し、完了後は固定所要時間を保持する。
- Historical Fundamental ImportカードへElapsed / 経過時間を追加。
- Historical Replay reportへelapsed_secondsを保存し、24H Bias Alignment欄にもReplay所要時間を表示する。
- v0.8.5 Light Skinは眩しすぎるとのHuman評価を受け、4 Skinを低彩度・落ち着いたsurfaceへ再調整。
- Skin名: Aurora Mist / Sand Gold / Slate Midnight / Dusty Sakura。
- pure white面積、高彩度accent、radial glow、強いgradient、強いshadowを削減。
- 参考方向としてMobbin / SaaSFrame等の実製品UIギャラリーを確認。個別製品の複製ではなく、低彩度surface・限定accent・情報階層優先の原則だけを採用。
- v0.8.6 package validation: 52 pytest PASS / compileall PASS / UI JavaScript syntax PASS / packaged ZIP再展開後50 tests PASS。
- package SHA-256: f784a7dc30199b254a60b552e17d5f308583f54970f59ccf76de8e2bb538598b。


### v0.8.6 packaging label correction
- Human確認でv0.8.6 ZIP内の一部runtime/UI表記がv0.8.5のまま残っていることを発見。
- `BBB_START.bat` / `BBB_LOCAL_AI_SETUP.bat` / runtime `__version__` / Desktop API version / UI header / first-read docsをv0.8.6へ統一。
- Calm Skin名もcurrent docsで Aurora Mist / Sand Gold / Slate Midnight / Dusty Sakuraへ統一。
- 回帰防止testを追加し、corrected package validationは52 pytest PASS。
- corrected package SHA-256: f784a7dc30199b254a60b552e17d5f308583f54970f59ccf76de8e2bb538598b。

### v0.8.6 ZIP root layout correction
- Human実機確認で、修正版v0.8.6 ZIPを上書きした後もLauncher/UIがv0.8.5のまま起動する事象を確認。
- 原因: ZIP内部が `BBB_v086_work/` の1段ラッパーフォルダ構造で、既存BBBルートへの上書き時にv0.8.6ファイルがサブフォルダへ入り、ルートのv0.8.5が残った。
- 対応: ZIP rootをフラット化し、`BBB_START.bat` / `src/` / `config/` 等がZIP直下に来るFIXED packageを作成。
- FIXED packageで `BBB_START.bat` / runtime version / UI versionがv0.8.6であることを検証。
- pytest 52/52 PASS。
- FIXED package SHA-256: 3777b045f66da59ee58e0480eeffd6ae44f3e69221f06366401f8144a67b85d4。

### v0.8.6 Run Timing UI hotfix
- Human実機確認でHistorical Fundamental Import画面に `ReferenceError: clockDuration is not defined` が表示された。
- Stored 100 / Classified 100 / Replayable 100は正常で、Historical Import data自体は破損していない。
- 原因: v0.8.6 UIでRun Timing表示用 `clockDuration()` を呼び出していたが、helper定義が欠落していた。
- `clockDuration()` を追加し、1時間未満はMM:SS、1時間以上はHH:MM:SSで表示。
- 既存testは文字列参照だけを見ており定義欠落を検出できなかったため、helper definitionを直接確認する回帰testへ修正。
- HOTFIX packageはflat ZIP rootを維持。
- validation: pytest 52 PASS / compileall PASS / UI JavaScript syntax PASS / packaged ZIP再展開test PASS。
- HOTFIX SHA-256: 14b26a9def1b27f897da943bc48990a5a050eb339933804600f19fdf2029959f。

### v0.8.7 Cool Contrast UI
- Human feedback: v0.8.6は眩しさは減ったが、ページ全体のコントラストが弱く、よりはっきりしたCoolな見た目を希望。
- Main colorをDeep Navy #0B1622 + Electric Blue #2F9EE5の2色に固定。
- Sidebarを最暗部、workspaceを中間、card / metricを段階surfaceとして分離。
- active navigationはblue left rail、primary actionはflat blue。
- Green / Yellow / Redは成功・警告・エラー等のsemantic status専用とし、通常装飾には使わない。
- 4 SkinはGraphite Blue / Deep Navy / Steel Slate / Black Iceへ再編。すべてCool product UIの範囲内に統一。
- Mobbin / SaaSFrame等の実製品UI galleryで見られる、clear hierarchy / limited accent / dark analytics surfaceの方向を参考にした。特定製品の複製はしない。
- v0.8.7 validation: 54 pytest PASS / compileall PASS / UI JavaScript syntax PASS / flat ZIP root確認 / packaged ZIP再展開後54 tests PASS。
- package SHA-256: d1a60f524b1b56922820feaefe81fa5f321b6717056bb2e8b8f4b1056eeed64a。

