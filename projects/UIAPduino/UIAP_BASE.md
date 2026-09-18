# UIAP BASE（仮）

## Purpose

UIAP BASE（仮）は、UIAPduino CH32V003を中心に、初心者・教育用途で扱いやすくしながら、上級者には拡張・改造の余地を残すことを目指す開発ボードである。

現在の最優先目標は、最終仕様の完成ではなく、試作機を完成させて実機評価を始めることである。

---

## Current Development Direction

### Target UIAPduino

最初の製品はUIAPduino CH32V003専用とする。

CH32V003版で製品・設計として成立させた後、UIAPduino CH32V006版への展開を検討する。UIAPduino CH32V006は現在β版であるため、今後のアップデートを待つ意味も含めて、現段階ではCH32V003版を優先する。

### Connection Method

UIAPduino CH32V003側にはピンヘッダーをはんだ付けする。

UIAP BASE側には、左右それぞれに2×12のメスソケットを配置し、ピンヘッダーを実装したUIAPduinoを差し込んで使用する。

したがって、現在の設計は完全な「はんだ付け不要」ではない。子どもが組み立てる場合は、親が作業する、または親の監修下ではんだ付けすることを想定する。

---

## GPIO Visualization

UIAPduinoにUSB経由でプログラムを書き込み、各GPIOのHIGH / LOW状態をUIAP BASE上のLEDで可視化する。

LEDはUIAPduinoのGPIOから直接駆動するのではなく、BASE側MCUがGPIO状態を監視し、その結果に応じてLEDを制御する方向で設計する。

過去案では74HC04を3個使用してLEDを駆動する方式を検討していたが、BASE側にMCUを搭載する方針へ変更したため、74HC04方式は現在不採用とする。

GNDには状態表示LEDを設けない。

---

## Base-side MCU Role

BASE側MCUは単なるLED制御用ではなく、UIAP BASE自体に独自機能を持たせるための中核として利用する。

現時点で想定している役割は以下。

- UIAPduino CH32V003のGPIO状態監視
- GPIO状態に応じたLED制御
- UIAP BASE単独で動作するLEDゲーム
- RESET / MODEボタンの処理
- 完成基板の検品モード
- 上級者によるファームウェア書き換え・カスタマイズ

ゲーム機能の搭載自体は採用方針とするが、ゲーム内容は未定。

UIAPduino側にユーザープログラムがない状態でも、USBから電源が供給されればBASE側MCUが動作し、BASE単独のLEDゲームなどを利用できる構成を目指す。

---

## Buttons / RESET Policy

初期案ではRESET / MODEを1個のスイッチへ集約する方向で検討していたが、Feature Freeze 0.1では操作系を再評価し、A / Bの2ボタン構成を有力案とする。

2ボタンを持たせる主な理由は以下。

- BASE単独ゲームの操作幅を増やす
- 選択 / 決定 / 戻るなどの基本UIを作りやすくする
- 短押し / 長押し / A+B同時押しなどを利用して、少ない部品で複数の操作を実現する
- 検品モードや設定モードへの入口として利用できる

A / Bは日常的に使うアクションボタンとし、通常操作のたびにUIAPduino RESETが発生する構成にはしない。

UIAPduinoのハードRESETをBASE側からどのように提供するかは、A / Bとは切り分けて検討する。候補は、UIAPduino本体RESETへのアクセス確保、専用の小型RESETスイッチ / test pad、BASE MCU + transistorによるRESET制御など。

RESET方式は基本回路freeze前に確定する。

---

## Advanced User / Manufacturing Features

### Base MCU Programming / Debug Access

BASE側MCUには、基板裏面からアクセスできる書き込み・デバッグ用パッドを設ける方向で検討する。

通常ユーザーには意識させず、上級者は自分で端子をはんだ付けしてBASE側MCUのファームウェアを書き換えられる設計を目指す。

### Inspection Mode

特定の端子またはテストパッドを短絡するなどの方法で、完成基板の検品モードを起動できる仕組みを設ける方向で検討する。

検品モードでは、例えば以下を自動確認できるようにする。

- LEDの順次点灯
- LED点灯状態の確認
- RESET / MODEボタン入力確認
- その他、BASE側MCUから確認可能な機能

目的は、完成品の検査時間短縮と検査手順の標準化である。

---

## External Connection Design

UIAPduino周辺のソケットから各ピンへアクセスできるほか、ボード右側にも端子台と対応ソケットを配置する方向で設計する。

端子台を設ける主な理由は以下。

- ロボットなど動きのある用途で配線を強固に締結できる
- 抜けやすいジャンパ線によるストレスを減らす
- 実験用だけでなく、実使用時の配線方法も用意する

端子台下のソケットは、マイコン周辺をごちゃごちゃさせずに配線したいユーザー向けの選択肢とする。

右側端子群のピン配置は、単なる番号順ではなく、用途・既存モジュールとの互換性・初心者の使いやすさを理由づけして決定する。

最下段の端子群については、CH9102F系シリアル変換モジュールの利用を意識した並びを検討している。

---

## Design Philosophy

UIAP BASE（仮）は、以下の二層構造を目指す。

- 初心者には簡単に使える
- 上級者には内部まで触れる余地がある

通常使用に必要のない高度な端子や機能は、初心者向けUIを複雑にしない位置・表示方法にする。

特に教育用途では「どこに接続すればよいか」が直感的に分かることを優先する。

一方で、上級者向けには書き込み・デバッグ用パッドや未実装フットプリントなどを残し、カスタマイズ可能な余地を確保する。

低価格を重視するが、単純な最安構成だけを目標にはしない。必要性が確認された場合は、信号線のノイズ対策など、部品追加を伴う改善も許容する。

また、初期製品では削る機能であっても、コストをほぼ増やさず将来利用できるフットプリントやテストパッドとして残せるものは積極的に検討する。

---

## MCU Architecture Options

### A案：CH32V006を継続採用

現在までの基本案。

CH32V006をBASE側MCUとして使用し、LED制御、ゲーム、検品、ボタン処理、上級者向けカスタマイズなどを担当させる。

USBシリアル通信が必要な場合は、外付けモジュールまたは別途USB-UART回路を利用する。

A案は引き続きバックアップ案として残す。

### B案：USB対応WCH MCUへ置換

2026-09-15時点で新たに有力候補として検討を開始した案。

CH32V006に固定せず、USB機能を持つWCH製MCUへ置き換えることで、現在V006に任せる機能を維持しつつ、UIAP BASE自体の将来拡張性を高めることを狙う。

現時点ではCH32V203系などを候補として調査する。

期待する利点は以下。

- GPIO監視とLED制御
- LEDゲーム
- 検品モード
- RESET / MODE処理
- 上級者向けカスタマイズ
- USB機能を利用した将来拡張
- 外付けUSBシリアル変換モジュールを不要にできる可能性
- 部品統合による基板面積・部品点数・総コスト削減の可能性

B案を積極的に進め、技術的・コスト的・製造上の問題で成立しないことが確認された場合はA案へ戻る。

---

## USB Design Policy

UIAP BASEにUSB機能を持たせる場合でも、販売状態ではBASE側USBコネクタを標準実装しない方向で検討する。

理由は、UIAPduino本体とUIAP BASEの両方にUSBコネクタが見えると、初心者や子どもが「どちらへ接続すればよいのか」迷う可能性があるため。

教育用途ではUIAPduino側USBを通常利用の入口として明確にする。

BASE側USBは上級者向け拡張として扱い、以下のような構成を検討する。

- USBコネクタ用フットプリントのみ配置
- 必要なD+ / D-配線を設計
- 必要に応じてCC抵抗、保護回路などのDNP（未実装）フットプリントを配置
- 上級者が自身ではんだ付けして機能を有効化できる

この方針により、標準品の部品コストと初心者向けUIの単純さを維持しつつ、玄人向け拡張性を残す。

なお、USBシリアル通信が可能であることと、UIAPduino CH32V003への書き込み・デバッグが可能であることは別機能として扱う。B案では将来的にどこまで統合可能かを継続調査する。

---

## Cost / Manufacturing Policy

コストは10円単位でも削減対象として検討する。

ただし、開発初期は機能候補を広い角度から検討し、その後に以下の観点で「残すもの」「削るもの」を選別する。

- ユーザー価値
- 部品単価
- PCB面積
- 実装費
- JLCPCBでのPCBA可否
- LCSC / JLCPCBでの在庫・安定調達性
- 初心者の使いやすさ
- 将来拡張性

特にJLCPCB / LCSCで安定して調達・実装できることを重要な選定条件とする。在庫・PCBA対応状況は、部品選定におけるボトルネックになり得る。

最終的に削除する機能でも、部品を実装せずフットプリントやテストパッドのみ残すことで低コストに将来拡張性を確保できる場合は、その方法を優先的に検討する。

---

## Firmware Policy

BASE側MCUのファームウェアはAIを利用して設計・実装する予定。

ただし、AI生成コードをそのまま正式採用するのではなく、実機テストを前提とする。

基本フロー：

1. 機能仕様を定義
2. AIがファームウェア設計・コード生成
3. 実機で検証
4. 不具合を修正
5. 再テスト
6. 安定したものを正式版とする

---

## Current Decision

2026-09-15時点では、A案をバックアップとして残しつつ、B案を積極的に検討・開発する。

B案に重大な破綻要因が見つかった場合はA案へ戻る。

現在はMCUをまだ最終決定しない。

次の評価では、CH32V006とUSB対応WCH MCU候補を、以下の観点で比較する。

- MCU単価
- JLCPCB / LCSC在庫・PCBA対応
- GPIO数
- USB機能
- 必要周辺部品
- パッケージサイズ
- LED制御能力
- ゲーム・検品機能への適性
- 書き込み・デバッグ方法
- 将来のUIAPduino CH32V003書き込み支援への発展可能性
- 実装済みUIAP BASE全体としての総コスト

---

## Current Priority

最優先事項はUIAP BASE試作機を完成させることである。

ただし、MCU選定はPCBレイアウト・USB拡張・書き込み端子構成へ影響するため、本格的なレイアウト確定前にA案 / B案の評価を進める。


---

## Feature Freeze 0.1 — 2026-09-18

V0.1の最小構成を保存したまま、その骨格を大きく変えずにUIAP BASEの付加価値を一段上げるための機能範囲を仮固定する。

このFeature Freezeは最終仕様ではない。PCB粗配置へ進む前に「何を本体へ載せ、何を外部エコシステムへ逃がし、何を将来用として残すか」を整理するための基準である。

### Core Architecture

現時点では以下の基本構成を維持する。

- BASE MCU：CH32V203C8T6を第一候補として継続
- LED driver：SM16206Sを第一候補として継続
- UIAPduino 15信号の状態監視 / LED可視化
- BASE logic：3.3V
- LED rail：5V
- UIAPduino USB-Cを通常の給電・書込み入口とする

ESP32-C3 / C6 / S3も比較対象として確認したが、現行BASEではGPIO数、価格、電源、RF設計、基板面積などを含めてCH32V203構成を変更する決定要因は確認されていない。

無線が製品価値の中心になる将来版では、ESP32-S3等を別系統として再評価する余地を残す。

### A / B Buttons

操作系は1ボタン案からA / Bの2ボタン案へ拡張する。

A / Bはゲーム専用ではなく、BASE全体の汎用操作入力として利用する。

想定用途：

- ゲーム操作
- 選択 / 決定 / 戻る
- 短押し / 長押し
- A+B同時押し
- MODE切替
- 検品モードへの入口
- 将来追加する機能の操作

UIAPduino hard RESETはA / Bの日常操作から分離し、別方式で確保する。

### Secret LED

SM16206Sの16chのうち、UIAPduino 15信号表示で使用しない1chを付加価値へ利用する案を有力候補とする。

通常のSTATUS LEDとして固定せず、以下のような遊びを含めて検討する。

- BASE logo / iconの隠し発光
- GAME / MODEの演出
- 課題達成時の表示
- inspection / special state表示
- 基板裏面やFR-4透過を利用したSecret LED表現

最終的な発光方法とシルク / 銅箔デザインはPCBレイアウト時に検討する。

### Grove / M5Stack Unit Expansion

UIAP BASEにGrove / M5Stack Unit系の既製モジュールを接続できる入口を持たせる案を、V0.2の有力機能とする。

目的はBASE本体へ多数のセンサーを搭載することではなく、コネクタ1個の追加によって、既に市場に存在する安価なモジュール群を利用できるようにすることである。

期待する利用例：

- Button
- Buzzer
- Light sensor
- PIR / distance sensor
- OLED
- environmental sensor
- motor / actuator関連Unit
- M5Stack UnitおよびSeeed Grove系モジュール

「部品をBASEへ盛る」より「既存エコシステムへの入口を用意する」ことを優先する。

Grove系は同じ4pinコネクタでもGPIO / I2C / UART / analogなど信号方式が異なるため、V0.2でどこまで対応するか、電源電圧、信号保護、pin assignmentは回路設計段階で確定する。

### Qwiic Policy

Qwiic / STEMMA QTは有用なI2Cエコシステムだが、UIAPduino CH32V003自体にQwiic用の拡張経路 / footprintが存在する。

そのためBASE側へ同じ機能を重複実装する優先度は低い。

BASE装着中でもUIAPduino側Qwiic機能を利用しやすいよう、コネクタ位置、周囲のclearance、外装との干渉を考慮する。

### SAO Policy

SAO (Simple Add-On) は海外Maker / Badgelife文化との相性が良く、PCB art、meme board、small OLED、LED accessoryなど遊び心のある拡張を作りやすい。

一方で、現段階ではUIAP BASEの初心者向けという本質に直接必要な機能ではなく、主要機能として前面へ出すと目的が散る可能性がある。

したがってFeature Freeze 0.1では以下とする。

- 標準機能としての採用は保留
- PCB面積やUIを汚さず残せる場合のみ、裏面DNP footprint等を検討
- 汎用拡張端子からSAO adapterを後付けする方式も候補
- SAO文化そのものをBASE開発の主目的にはしない

### Future / DNP Expansion

以下はV0.2標準搭載を必須とせず、低コストで逃げ道を残せる場合にDNP footprint / pad / routingとして検討する。

- BASE側USB
- generic 3.3V / 5V / GND / UART / I2C等の拡張pad
- wireless module接続
- advanced debug / inspection access
- SAO adapter接続
- future accessory identification

無線機能そのものをV0.2標準品へ搭載する方針ではない。

### Mechanical / Community Expansion

UIAP BASEは専用ケースを必須としない。

裸基板のままブレッドボード横へ置きやすく、デスク上でも完成品として見えることを重視する。

また、第三者がcase / tray / stand / decoration / accessoryを設計しやすいようにする。

検討項目：

- mounting hole位置と穴径の標準化
- board outlineの安定化
- UIAPduino、terminal block、USB等の高さとkeepout公開
- STEP等の3D model公開
- 寸法図公開
- 3D printerで外装やアクセサリを作りやすい構成

「完成ケースをすべて用意する」のではなく、「他のMakerが続きを作りやすいmechanical interfaceを提供する」ことを目指す。

### Visual Design Direction

PCB単体でも大人が机に置きやすく、同時に子どもが触りたくなる遊び心を持たせる。

基本イメージ：

- 白いUIAPduinoを視覚的な主役にする
- BASEは青〜青緑系を中心とした落ち着いた色調を候補とする
- 黄 / orange等を必要箇所のaccentとして使う
- 子ども向けのrobot / planet表現だけに寄せず、waveform、circuit symbol、grid、coordinate、typography等も利用する
- 空きPCB面積を単なる余白ではなく、説明 / icon / hidden message / artとして活用する

目標は「Educational instrument × playful object」とする。

### Deferred Idea: BOTchan

OLED等を顔として使う小型character gadget / BOTchan案は、UIAPduino入門体験や将来のsoftware体験として発展可能性がある。

ただし現段階ではBASEの回路・PCBを完成させる優先度が高いため、BOTchanはV0.2の必須要件へ入れず別アイデアとして保留する。

### Feature Selection Rule

今後の追加機能は、単純に「面白いか」だけでは採用しない。

優先するのは以下。

- 追加BOM / PCB面積が小さい
- 初心者の配線・理解の負担を下げる
- 1つのconnector / footprintで多くの既製品や用途を開放できる
- BASEの本来目的である学習・可視化・拡張へ直接つながる
- 不要なユーザーへコストを強制しない
- 将来のMaker / community拡張へ逃げ道を残せる

特定センサーを多数オンボード搭載するより、Groveのように外部エコシステムへ接続できる入口を優先する。

### Next Step after Feature Freeze 0.1

PCB粗配置へ進む前に、以下を基本回路へ反映して確定する。

1. A / B button回路とUIAPduino hard RESET方式
2. Grove / M5Stack Unit portの電源・信号方式・connector footprint・向き
3. Secret LEDの実装方法
4. UIAPduino側Qwiicへのclearance
5. SAOをDNPで残すか、adapter方式へ完全に逃がすか
6. mounting hole / board outline / external connector keepout
7. USB DNP / debug pad / generic expansion padの物理領域

これらを反映した後に、PCB粗配置 → 配線性評価 → A4 1:1実寸確認へ進む。

---

## Prototype Basic Circuit Baseline — 2026-09-18

CH32V203C8T6 + SM16206S の1-MCU構成について、基本回路図へ進めるための暫定ベースラインを定める。

これは最終仕様ではなく、試作・PCB粗配置・実測のための基準点とする。配線性や実機評価によって一般GPIO割当や定数は変更してよい。

### Power

V0.1ではUIAPduinoを電源の親、UIAP BASEを子とする。

- 通常はUIAPduino USB-Cから給電する。
- UIAPduino 3.3V → BASE_3V3 → CH32V203C8T6 / SM16206S logic
- UIAPduino 5V → LED_5V → 15個の状態表示LED
- GNDは共通とする。
- USB給電と外部給電を同時に使用しない。
- BASE側USBを将来実装する場合、VBUSを既存5V railへ直接接続せず二重給電を避ける。

試作時の電流測定・切り離しができるよう、3.3V / 5V railには閉じたソルダージャンパを置く案を採用する。

### CH32V203 Minimum Circuit

- VDD / VIO / VDDA / VBAT：3.3V
- VSS / VSSA：GND
- 各電源ピン近傍に0.1uF
- BASE_3V3へ4.7uF程度のbulk capacitor
- NRST：0.1uF to GND。内部弱pull-upを利用し、裏面test padへ引き出す。
- BOOT0：10k pull-down + 3.3Vへ一時接続できるtest pad
- PB2 / BOOT1：10k pull-down
- PA13 / SWDIO、PA14 / SWCLK、NRST、3.3V、GNDを裏面debug/program padへ出す。

V0.1はUSB検証時の不確定要素を減らすため8MHz外付け水晶を実装する方向とする。量産最適化時に内部HSIのみで十分か再評価する。

### SM16206S LED Driver

SM16206Sは3.3Vで動作させる。

- SDI → PA0
- CLK → PA1
- LE → PA2
- OE → PA3
- OEには外部10k pull-upを追加して起動時消灯を強化する。
- R-EXTは10kΩ前後を初期値とし、約1.65mA/chで視認性を実測する。
- OUT0～OUT14 → 15個のLED cathode
- LED anode → LED_5V
- OUT15は予備とする。
- 0.1uF decouplingをVDD直近へ配置する。

SM16206S内部にはOE約250kΩ pull-up、LE約250kΩ pull-downがあるが、起動時の不用意な点灯を避けるためOEは外部pull-upを追加する。

### UIAPduino Signal Monitoring

UIAPduinoの信号本線を切らず、各信号から1kΩ程度を介してBASE MCU入力へ枝分かれする。

監視先は5V tolerant (FT) pinを使用する。

暫定割当：

| UIAPduino | CH32V203 |
|---|---|
| D0 | PB10 |
| D1 | PB11 |
| D2 | PB12 |
| D3 / SDA | PB13 |
| D4 / SCL | PB14 |
| D5 | PB15 |
| D6 | PA8 |
| D7 / SCK | PA15 |
| D8 / MOSI | PB3 |
| D9 / MISO | PB4 |
| D10 | PB5 |
| D11 / SWIO | PB8 |
| D12 | PB9 |
| D15 / TX | PA10 / USART1_RX |
| D16 / RX | PA9 / USART1_TX |

D15/D16は通常GPIO監視として入力し、USB CDC-UART bridgeモード時のみUSARTへ切り替える。

CH32V003は5V動作時でも3.3V出力をHIGHとして認識できる入力仕様のため、V203 TX → UIAPduino RXにはV0.1で追加level shifterを置かない。

### RESET / MODE Button — Previous V0.1 Candidate

基本回路V0.1では、1個のpush switchをUIAPduino RESETとBASE MODE入力へ兼用する案を検討した。

- push switch：3.3V → BTN_NODE
- BTN_NODE：100k pull-down → GND
- BTN_NODE → CH32V203 PA4 input
- BTN_NODE → N-MOSFET gate
- N-MOSFET source → GND
- N-MOSFET drain → UIAPduino RESET

この案は、BASE MCU firmwareが停止していても物理操作でUIAPduino RESETをLowにできる利点がある。

ただし、Feature Freeze 0.1でA / Bの2アクションボタンを優先する方向へ変更したため、この1ボタン兼用案は現在の最終候補ではない。

A / Bの日常操作とUIAPduino hard RESETを分離する方向で、基本回路freeze前に再設計する。

### USB / Future Expansion

- UIAPduino USB-Cを通常の電源・書込み入口とする。
- PA11 / PA12はV203 USB Device用として予約する。
- BASE USB-CはV0.1標準実装せず、DNP footprint / routingを検討する。
- 将来BASE USBを実装する場合、USB VBUSはシステム5Vへ直結しない。
- PB6 / PB7のもう一方のUSB FS機能は将来用として予約する。
- D11 / SWIOはV0.1では監視のみ。BASEから能動的にSWIO書込みする機能は別途電圧・双方向駆動を検証してから設計する。

### Current Assessment

現時点ではCH32V203C8T6 + SM16206Sの1-MCU構成を崩す重大な電気的矛盾は確認されていない。

MCU選定そのものを主要ボトルネックから外し、次工程を以下へ進める。

```text
基本回路V0.1
  ↓
PCB粗配置
  ↓
配線性を見て一般GPIOを入れ替え
  ↓
A4 1:1実寸確認
  ↓
回路・配置修正
  ↓
PCB freeze
```

次工程では、UIAPduino socket、15 LEDs、CH32V203、SM16206S、terminal blocks、RESET/MODE、USB DNP、裏面debug padsの物理配置を検討する。
