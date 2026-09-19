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

状態表示LEDは、単独の15連LEDバーとしてまとめるのではなく、UIAPduinoの各GPIOピンとの対応が直感的に分かるよう、UIAPduino周囲のピン配列に沿って配置することを基本とする。

したがって、ゲームや演出へ流用する場合も、論理上の「15ch」を物理的な一列配置とみなさず、実際のLED配置を前提にUIを設計する。

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

## Prototype Basic Circuit Baseline V0.1 — 2026-09-18 (partially superseded)

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

---

## Basic Circuit V0.2 Candidate — 2026-09-18

Feature Freeze 0.1を基本回路へ反映した最新版候補。

このセクションは、上記Prototype Basic Circuit Baseline V0.1のうち、button / RESET、Grove、Secret LED、USB resource allocationに関する内容を更新する。CH32V203C8T6 + SM16206Sという基本骨格、3.3V logic / 5V LED rail、15信号監視の方針は維持する。

### 1. A / B Action Buttons

A / BはBASEの日常操作用buttonとし、UIAPduino RESETとは分離する。

暫定回路：

- BTN_A：PA4 input
- BTN_B：PA5 input
- 各pinは10kΩで3.3Vへpull-up
- 各buttonは押下時にGNDへ接続
- debounceは原則firmwareで行う
- V0.2ではbuttonごとのRC debounce capacitorは必須としない
- A+B同時押し、長押し、boot時押下をfirmwareで識別可能にする

A / Bはgameだけでなく、MODE、selection、inspection、future functionにも使う。

### 2. Dedicated UIAPduino RESET

UIAPduino V1.4にはRESET / D17信号が外部端子へ出ているため、BASE側に小型の専用RESET buttonを設ける。

physical RESETはBASE MCUが停止していても動作するよう、RESET / D17をbuttonで直接GNDへ落とす。

加えて、BASE MCUからもUIAPduinoをresetできるようにする候補として以下を採用する。

- UIAPduino RESET / D17 → N-MOSFET drain
- N-MOSFET source → GND
- N-MOSFET gate → PA6
- gate → 100kΩ pull-down → GND
- device candidate：2N7002 class

これにより以下を分離する。

- A / B：ユーザー操作
- RESET：物理的なUIAPduino hard reset
- PA6 + MOSFET：BASE MCUからのprogrammatic reset

専用RESET buttonはA / Bより小さくする、または配置を離して誤操作を防ぐ。

### 3. Secret LED

SM16206SのOUT15を予備のまま残さず、Secret LED用channelとして使用する候補とする。

暫定回路：

- LED16 anode → LED_5V
- LED16 cathode → SM16206S OUT15
- currentは他の状態表示LEDと同じREXT設定で制御
- LED package / color / mounting sideはPCB layoutで確定

用途：

- UIAP BASE logo / icon illumination
- GAME / MODE special effect
- inspection state
- hidden message / achievement
- board artとの連携

FR-4透過方式はPCB厚、solder mask色、LED brightnessに強く依存するため、V0.2では方式を固定しない。表面icon、裏面LED、cutout等をlayout時に比較する。

### 4. Grove / M5Stack Unit Port — V0.2 Scope

V0.2ではGroveを「万能port」にせず、M5Stack Port.A系のI2Cと一般GPIOを主軸にする。

M5Stack HY2.0-4Pの一般的な物理配列：

- Black：GND
- Red：5V
- Yellow：signal
- White：signal

M5Stack Port.AではYellow = SDA、White = SCLとして使用される。

#### Signal Assignment

CH32V203のPB6 / PB7をGroveへ割り当てる。

- Yellow → PB7 / I2C1_SDA
- White → PB6 / I2C1_SCL
- PB6 / PB7は通常GPIOとしても利用可能
- PB6 / PB7は5V tolerant (FT) pin

これにより、I2C Unitだけでなく、Button / Buzzer / LED系など単純GPIOを使うUnitの多くにもfirmware対応できる。

V0.2では以下を標準対応範囲とする。

- I2C
- Digital Input / Output
- PWM等、通常GPIOで実現できる機能

以下はV0.2で「完全互換」を保証しない。

- Analog inputを必要とするUnit
- Grove UART pin orderを前提とするUnit
- 大電流Unit
- 5V output logicを必須とする特殊Unit

UARTやAnalogまで完全対応するためにMUX / level conversion / additional ADC等を標準搭載することは、現段階では行わない。

#### Grove Power

M5Stack Unitとの互換性を優先し、GROVE_VCCは5Vをdefaultとする。

ただしSeeed Grove系には3.3V動作を前提とするmoduleも存在するため、PCB上に5V / 3.3V選択用solder jumperを設ける案を採用する。

- default：5V
- optional：3.3V
- 初心者が通常操作するjumperにはしない
- silkscreenでdefault 5Vを明示する

3.3V railはUIAPduino上のXC6206 regulatorを経由するため、外部moduleへ大電流を供給する用途には使用しない。

#### Signal Protection

Grove signal 2本には100～330Ω程度のseries resistorを入れる候補とする。

I2C pull-upはmodule側との重複を考慮し、4.7kΩ程度のDNP pull-up footprintを3.3V側へ用意する案を採用する。

最終抵抗値は実機でI2C rise time、GPIO operation、誤接続時挙動を確認して決定する。

#### Power Budget

UIAP BASEのGrove portは、V0.2ではsensor / display / button / buzzer等のlow-power Unitを主対象とする。

motor / vibrator / high-power actuatorなど、USB power budgetへ大きな負荷を与えるUnitは標準用途に含めない。

GROVE_5V branchには、0Ω linkまたはresettable fuseを選択できるfootprintを入れ、prototypeで実電流を測定して保護値を決定する。

### 5. Grove Connector Candidate

PCB edgeへ横向きに挿せるHY2.0-4P、2.0mm pitch、right-angle SMDを第一候補とする。

2026-09-18時点の候補：

- CAX HY2.0-4P-WT / JLCPCB C722729
  - SMD right-angle
  - 2.0mm pitch
  - JLCPCB SMT assembly対応
  - low-cost candidate
- XUNPU WAFER-HY2.0-4PWB / JLCPCB C3029460
  - SMD right-angle
  - 2.0mm pitch
  - auxiliary solder supportあり
  - stock / mechanical robustnessの比較候補

final BOMでは最新stock、単価、connector retention、cable compatibilityを再確認して決定する。

### 6. USB Resource Allocation

PB6 / PB7はV0.2でGroveへ使用するため、CH32V203のUSBFS host/device interfaceとしては使用しない。

将来のBASE側USBはPA11 / PA12のUSB Device interfaceを使用する方向とする。

これによりV0.2で残せる将来機能：

- USB CDC
- USB HID
- BASE firmware update / PC communication

一方、CH32V203によるUSB Host機能はV0.2標準基板では優先しない。

USB Hostが必要になる将来版では、Groveとのpin sharing、MUX、別MCU、別board revisionのいずれかで再設計する。

このtrade-offは、現時点ではGrove / M5Stack ecosystemへの接続価値を優先する判断とする。

### 7. Qwiic

UIAPduino CH32V003 V1.4にはQwiic用CN2 (SM04B-SR) footprintがあり、標準出荷時は未実装である。

BASE側にはQwiic connectorを重複搭載しない。

代わりにPCB rough placementで以下を確認する。

- UIAPduino CN2を後付けした場合にBASE部品と干渉しない
- cableを抜き差しできるclearanceがある
- case / trayを後から作ってもQwiic accessを塞がない

### 8. SAO

V0.2基本回路にはSAO専用active circuitを追加しない。

PCB rough placementで十分な空き面積が残った場合のみ、以下のどちらかを比較する。

- backside DNP 2x3 footprint
- Grove / generic expansionからのSAO adapter

初心者向け表面UIにはSAOを前面表示しない。

### 9. Updated Pin Resource Plan

V0.2暫定割当：

| Function | CH32V203 |
|---|---|
| SM16206 SDI | PA0 |
| SM16206 CLK | PA1 |
| SM16206 LE | PA2 |
| SM16206 OE | PA3 |
| BTN_A | PA4 |
| BTN_B | PA5 |
| UIAP RESET control | PA6 |
| Reserved / sense candidate | PA7 |
| Monitor D6 | PA8 |
| Monitor D16 / RX | PA9 |
| Monitor D15 / TX | PA10 |
| BASE USB Device D- | PA11 |
| BASE USB Device D+ | PA12 |
| SWDIO | PA13 |
| SWCLK | PA14 |
| Monitor D7 | PA15 |
| Monitor D8 | PB3 |
| Monitor D9 | PB4 |
| Monitor D10 | PB5 |
| Grove SCL / GPIO | PB6 |
| Grove SDA / GPIO | PB7 |
| Monitor D11 | PB8 |
| Monitor D12 | PB9 |
| Monitor D0 | PB10 |
| Monitor D1 | PB11 |
| Monitor D2 | PB12 |
| Monitor D3 | PB13 |
| Monitor D4 | PB14 |
| Monitor D5 | PB15 |
| BOOT1 | PB2 |
| HSE | PD0 / PD1 |

PB10 / PB11は現時点ではUIAPduino D0 / D1 monitorを維持する。

GroveをPB6 / PB7へ割り当てることで15本monitorの5V tolerant input構成を崩さず、追加level shifter / dividerを避ける。

### 10. V0.2 Circuit Assessment

Feature Freeze 0.1を回路へ反映した結果、主要な追加部品は概ね以下へ収まる。

- action button ×2
- button pull-up resistor ×2
- dedicated UIAP RESET button ×1
- RESET control用N-MOSFET + gate pull-down
- Secret LED ×1
- Grove connector ×1
- Grove power-select solder jumper
- Grove signal series resistor ×2
- optional I2C pull-up footprint ×2
- optional Grove power protection footprint

大きなICを追加せずに、操作性、遊び、M5Stack / Grove ecosystemへの接続性を追加できる。

次工程はPCB rough placementとし、特に以下を物理的に確認する。

1. A / B / RESETを押し間違えにくい位置関係
2. Grove cableをboard edgeから自然に引き出せる向き
3. UIAPduino Qwiic CN2のclearance
4. Secret LEDの見え方
5. terminal block / 5-pin socketとの干渉
6. BASE USB DNP area
7. mounting holes / future 3D printed trayのkeepout




---

## Button Mode Switching Decision — 2026-09-19

A / Bボタンのモード切替方式について、教育性と実使用時の操作性の両面から比較を進めた。

### Switching Method Candidates

最終候補は以下の2方式まで絞った。

1. **3ピン・中央共通ジャンパー ×2**
   - 物理的に回路を切ってつなぎ替えるため、信号経路を理解しやすく教育用途との相性が良い。
   - 構造が単純で誤接続しにくく、低コスト。
   - 一方でA / Bの2回路を切り替えるにはジャンパーキャップを2個操作する必要があり、片側だけ切り替わった中間状態も作れてしまう。

2. **DPDT（2回路2接点）スライドスイッチ ×1**
   - 6端子の2回路を機械的に連動させ、A / Bの2系統を1回の操作で同時に切り替えられる。
   - NORMAL / GAMEなどのモード切替を1操作で行えるため、実使用時の分かりやすさと誤操作防止に優れる。
   - 教育上の「回路を自分でつなぎ替える」体験はジャンパー方式より弱くなる。

教育的価値ではジャンパー方式が優れるが、A / Bを確実に同時切替できる操作性を重視し、現時点ではDPDTスライドスイッチ方式を優先する。

### Current DPDT Selection

複数のJLCPCB / LCSC実装候補を比較した結果、**C22435667を現時点の採用候補とする。**

比較時には以下を重視した。

- DPDT / 2-position
- SMD実装
- JLCPCB / LCSCでの調達・実装性
- 部品単価
- PCB占有面積
- 操作しやすさ
- 外観
- 在庫・量産時の入手性

ALPS、G-Switch、SHOU HAN、NIDECなども比較対象としたが、UIAP BASEの価格目標とのバランスから、まずC22435667で試作・設計を進める。

スイッチの切換タイミング（Break-Before-Make等）は部品選定の必須条件に固定せず、切替途中に一時的な接続状態が発生しても危険にならない回路側設計を優先する。

### NIDEC Switch Policy

NIDEC製スイッチは品質、操作感、外観の面で魅力があり、将来の量産品や品質向上版では有力候補と考える。

現段階では単価がUIAP BASEのコスト目標に対して負担になりやすいため標準採用を見送るが、**今後の部品選定でもNIDEC製品を積極的に候補へ含める。**

特に量産数量、調達条件、価格差が改善した場合は、C22435667からNIDEC製DPDTスイッチへ置き換える可能性を残す。

PCB設計では、可能な範囲で将来の代替スイッチへ変更しやすいよう、スイッチ周辺の機械的余裕とフットプリント互換性を意識する。


---

## A / B NORMAL Mode Pin Assignment Decision — 2026-09-19

DPDTスライドスイッチによるA / BボタンのNORMAL / GAME切替について、NORMAL側の役割を以下の方針で決定する。

### A Button — RESET

AボタンのNORMAL側は、UIAPduino CH32V003 V1.4の **D17 / RESET (NRST)** へ固定接続する。

目的：

- UIAPduinoの物理RESETとして利用する
- BASE MCUが停止していてもRESET操作を成立させる
- RESET機能をユーザーが迷わず利用できるよう、専用機能として固定する

D11はSWIO兼用ピンであり、RESET用途には使用しない。

### B Button — Fixed General GPIO

BボタンのNORMAL側は、ユーザーが任意のGPIOへ配線する方式にはしない。

UIAP BASE側であらかじめ **一般用途GPIOを1本に固定**し、USERボタンとして扱う。

理由：

- 初心者が「どのGPIOへ接続するか」で迷わない
- 教材やサンプルコードを統一できる
- 誤配線や説明の複雑化を減らす
- UIAP BASEの「まず成功しやすい」設計思想に合う

固定GPIOは、UART / I2C / SPI / SWIO / RESET / オンボード機能などとの競合をできるだけ避けた、一般的で扱いやすいデジタルGPIOから選ぶ。

**現時点の第一候補は D5 (PC3)。**

ただしD5をこの時点で絶対固定とはせず、PCB粗配置・配線性を確認した上で、同等に扱いやすい一般GPIOの中から最も合理的なピンを最終確定する。

### GAME Mode Side

GAME側では、A / BボタンをBASE MCUの入力へ切り替える。

現行V0.2案：

- Button A → CH32V203 PA4
- Button B → CH32V203 PA5

DPDTスライドスイッチ1個で、A / Bの2回路をNORMAL / GAME間で同時切替する。

### Design Principle

A / BボタンのNORMAL側では自由配線を機能として提供しない。

- A = UIAPduino RESET
- B = UIAPduino fixed USER GPIO

という固定された役割にし、初心者が機能を理解しやすく、教材・サンプル・シルク表示を統一できる構成を優先する。

最終的なB側GPIO番号はPCB粗配置・配線性確認時に確定する。


---

## Grove / M5Stack Unit Compatibility Policy — 2026-09-19

UIAP BASEのGrove / M5Stack Unit対応は、コネクタの物理互換だけを広く保証する方針にはしない。

重要な前提：

> **ハードウェアとしてGrove / M5Stack Unitを接続できること**
>
> と
>
> **M5Stack向けArduinoライブラリや公式サンプルをUIAPduino CH32V003でそのまま利用できること**
>
> は別問題として扱う。

UIAPduino CH32V003はFlash / SRAMに余裕が大きくないため、ESP32級を前提とするM5Stack公式ライブラリ群や大型依存関係をそのまま持ち込む設計は避ける。

### V003で優先するUnit / Module

CH32V003でも比較的扱いやすく、学習用途との相性が良い以下のようなモジュールを優先する。

- Button / Switch
- Buzzer
- LED
- PIR
- Light sensor
- 単純なI2C温湿度センサー
- ToF距離センサー
- その他、軽量なGPIO / I2C制御で利用できるUnit

これらについては、必要に応じてUIAP BASE / UIAPduino向けの小さな専用ドライバ、軽量サンプルコード、教材を用意する。

### V003で慎重に扱うもの

以下は物理的に接続できても、V003で初心者向け標準対応として保証しない。

- 高度な画面描画
- 大きなフレームバッファを必要とする表示
- 画像処理
- 複雑な暗号処理
- センサーフュージョン
- 大型ライブラリ依存のUnit
- ESP32 / M5Unified / M5GFX等を前提とするコードをそのまま使う構成

OLED等の表示器は使用可能性があっても、RAM使用量やライブラリサイズを個別に確認して扱う。

表示器側にMCUを持ち、ホスト側がI2C等でコマンドを送るだけのUnitは、ホスト側のメモリ負担を抑えられる可能性があるため別途評価する。

### Compatibility Promise

UIAP BASEでは「Groveなら何でも使える」「M5Stack Unit完全互換」と広く表現しない。

ユーザーへの約束は、以下のように限定する。

> **UIAPduino CH32V003で実際に使いやすいGrove / M5Stack Unitを簡単につなげる。**

物理的に接続可能であることと、V003で快適に利用できることを区別する。

### Recommended Compatibility Levels

将来的に公式サイト、教材、対応表では、Unitごとに実機確認とソフトウェア負荷を基準として対応レベルを示す案を採用する。

- 🟢 **UIAP Ready**
  - 公式サンプルあり
  - V003で動作確認済み
  - 初心者向けに推奨

- 🟡 **Advanced**
  - 軽量ライブラリ、独自コード、RAM / Flash節約等の工夫が必要
  - 上級者向け

- 🔴 **V003非推奨**
  - メモリ不足、依存関係、機能過多等によりV003では推奨しない

対応表は「コネクタが刺さるか」ではなく、**V003実機で現実的に使えるか**を基準にする。

### V003 / V006 Educational Progression

将来UIAPduino CH32V006版へ展開する場合、同じGrove / M5Stack Unit ecosystemを使いながら、教材上の段階分けに利用できる可能性を残す。

- V003：基礎、軽量なUnit、GPIO / I2C中心
- V006：より高度なUnitや機能へ拡張

これにより、V003の制約を単なる弱点として扱うのではなく、限られたリソースで動かす学習要素として活用する。

### Design Principle

UIAP BASEのGrove / M5Stack対応は、対応数を誇ることよりも、初心者が迷わず実際に動かせることを優先する。

「つながる」ではなく「使える」を公式対応の判断基準とする。


---

## Grove / Qwiic Final Direction Summary — 2026-09-19

Grove / M5Stack Unit / Qwiic / STEMMA QT / Arduino Modulino周辺について検討した結果、UIAP BASE V003では「最大互換」を狙うのではなく、初心者が安全に使いやすい範囲へ意図的に絞る方針とする。

### 1. Basic Policy

UIAP BASE V003では、汎用性を無制限に広げない。

判断基準は、

> 対応できるかどうかではなく、初心者にとって対応する価値があるか

とする。

追加回路、切替操作、説明負荷、誤接続リスクが増える場合は、対応範囲を絞ることを優先する。

### 2. Qwiic

Qwiicは3.3V I2C ecosystemとして扱う。

- 3.3V
- SDA / SCL
- GND
- UIAPduino D3 / D4を使用
- SparkFun Qwiic
- Adafruit STEMMA QT
- Arduino Modulino等のI2C系への入口として利用可能

UIAPduino本体のCN2 footprintを必須とはせず、UIAP BASE側にもQwiic connectorを設ける方向で検討する。

理由：

- BASE基板端へ使いやすい位置に配置できる
- 初号機では基板面積を強く制限しない
- 実物で使用頻度・操作性を評価した後、量産版で削減判断できる

### 3. Grove

UIAP BASE V003のGrove portは **3.3V固定を基本方針** とする。

Grove ecosystem全体は3.3V / 5Vが混在しており、すべてのGrove製品を共通条件で保証することはしない。

教育用途で優先したい以下のような製品群には3.3V対応品が多く、V003用途では十分な選択肢がある。

- Button / Switch
- LED / Buzzer
- Light sensor
- Temperature / Humidity sensor
- PIR
- Distance / ToF
- 小型表示
- 各種軽量I2C sensor

5V必須になりやすい例：

- Motor / Motor Driver
- Electromagnet
- Water Atomization
- 一部のGas sensor
- 一部の旧型Relay
- その他、高消費電力・駆動系・旧設計module

これらはV003初期版で無理に標準対応しない。

### 4. No User Voltage Switching

ユーザーにGrove機器ごとの3.3V / 5V判断を要求しない。

したがって、現時点では以下をV003標準仕様から外す方向とする。

- 3.3V / 5V手動切替switch
- Grove voltage selection jumper
- 通常利用時にユーザーが電圧を選択する仕組み
- 5V Groveを広く保証するためだけの複雑なlevel conversion

「挿す前に電圧を調べて切り替える」操作は、UIAP BASEの初心者向け設計思想と相性が悪い。

### 5. Shared D3 / D4 I2C Bus

Grove I2CとQwiicはUIAPduinoのD3 / D4を共有する。

これはI2Cとして正常な構成であり、異なるI2C addressを持つdeviceは原理上同じbusで同時使用できる。

ただし以下は注意事項として扱う。

- I2C address重複
- module側pull-up resistorの重複
- 3.3V以外へpull-upされる製品
- V003のFlash / SRAM制約
- 大型library依存

基板上では必要以上に長い説明をせず、例えば以下のような簡潔なsilkscreenを検討する。

`I2C SHARED D3/D4`

Qwiic側には `3V3` を明示する。

Grove側についても3.3V運用が明確になる表示を行う。

### 6. Compatibility Promise

UIAP BASEでは「Grove完全互換」「M5Stack Unit完全互換」「何でも使える」とは表現しない。

公式な約束は以下とする。

> **UIAPduino CH32V003で実際に使いやすいGrove / Qwiic系moduleを簡単につなげる。**

対応可否はconnector形状だけでは判断しない。

実際の動作、電圧、memory負荷、library依存を確認して対応levelを決める。

### 7. Compatibility Levels

対応moduleは将来的に以下のlevelで管理する。

- 🟢 UIAP Ready
  - V003で動作確認済み
  - 初心者向け
  - 公式sampleあり

- 🟡 Advanced
  - 軽量化、専用driver、memory節約等の工夫が必要

- 🔴 V003非推奨
  - 5V必須
  - memory不足
  - 大型library依存
  - 機能過多
  - その他V003用途に不適

### 8. M5Stack Unit Positioning

M5Stack UnitはGroveと同じHY2.0-4P系connectorを使う製品が多いが、電源・signal条件を一括して同一視しない。

M5Stack Unit対応は「connectorが挿さること」ではなく、各Unitの電気条件とV003での実用性を確認してUIAP Ready判定する。

M5Stack Port.A互換を理由にBASE全体を5V設計へ寄せない。

### 9. Prototype Philosophy

初号試作では基板面積を強く削らない。

まずGroveとQwiicを実装して、

- 実際の使いやすさ
- connector配置
- cable取り回し
- 使用頻度
- 3.3V固定Groveで困るか
- QwiicをBASE側に持つ価値
- 対応moduleの広がり

を実機で評価する。

基板サイズ・connector数・不要回路の削減は、その後の量産版で判断する。

### 10. Superseded Ideas

以下は検討過程で出た案だが、現時点の基本方針としては採用しない。

- Grove VCCを5V defaultにして3.3Vへ切替
- ユーザーが機器ごとに3.3V / 5Vを切り替える
- 5V I2C対応のためのlevel shifterを標準必須にする
- Groveを万能portとして全製品対応させる
- M5Stack Port.AをGrove全体の基準として扱う

これらは将来の上位版・別版で必要性が出た場合に再検討する。

### Current V0.2 Direction

現時点のV0.2方向は以下。

- Qwiic：3.3V固定、D3 / D4
- Grove：3.3V固定、D3 / D4
- 両者は同じI2C busを共有
- 3.3Vで安全に使える製品をUIAP Ready候補とする
- 5V必須Groveは標準対象外
- ユーザー電圧切替は設けない
- 初号機ではGrove + BASE側Qwiicの両方を実装候補として維持
- 実機評価後に量産版で削る


---

## Physical Component Dimension Baseline V0.1 — 2026-09-20

PCB粗配置や実物に近い外観イメージを作る前段として、現時点で採用済みまたは有力候補となっている主要部品の実寸を整理する。

このセクションは**物理寸法の基準**であり、電気仕様の決定を上書きしない。Grove / Qwiicの電気的扱いは、より新しい `Grove / Qwiic Final Direction Summary — 2026-09-19` を優先する。

### 1. UIAPduino Pro Micro CH32V003 V1.4

実機外形の最重要基準。

- Board size: **17.8 mm × 33.0 mm**
- Published product height: **3.2 mm**
- Weight: 2.3 g
- Mounting holes: **3 × Ø1.7 mm**
- Through holes: **24 × Ø0.9 mm**
- USB-C opening is aligned with the board edge.
- UIAP official dimension drawing is the primary physical reference.

外観イメージでは、UIAPduinoを概算ではなく17.8 × 33.0 mmの実寸比率で描く。

### 2. BASE MCU — CH32V203C8T6

- Package: **LQFP48**
- Molded body: **7.0 mm × 7.0 mm**
- Lead pitch: **0.5 mm**
- Approx. overall lead span: **9.0 mm × 9.0 mm**
- LQFP overall height: approximately **1.5 mm** class from package drawing

外観イメージでは7 mm角の黒いLQFP本体として扱い、リードを含めた占有幅は約9 mmを基準にする。

Source basis: WCH CH32V203 datasheet.

### 3. LED Driver — SM16206S

- Exact part: SM16206S / LCSC C121618
- Package: **QSOP-24**
- Nominal molded body: **8.65 mm × 3.9 mm × 1.4 mm**
- Lead pitch: **0.635 mm**
- Datasheet body tolerance:
  - length D: 8.2–9.2 mm
  - body width E1: 3.6–4.2 mm
  - overall lead span E: 5.6–6.5 mm
  - max package height A: 1.95 mm

外観イメージでは約8.65 × 3.9 mmの細長いIC本体として扱う。

Source basis: Shenzhen Sunmoon Micro SM16206 datasheet.

### 4. DPDT Mode Switch — HanElectricity MST22D18G40-B

- Exact candidate: **MST22D18G40-B**
- LCSC: **C22435667**
- Mounting: SMD
- Circuit: DPDT
- Body / package plan size: **9.1 mm × 3.5 mm**

LCSCの公開属性ではZ方向の全高が明示されていないため、外観イメージで高さを厳密値として固定しない。

Source basis: LCSC exact-part listing / footprint.

### 5. Grove / HY2.0-4P Connector Candidates

最新方針ではGroveは3.3V固定・UIAPduino D3/D4 I2C bus側として扱う。

#### Candidate A — CAX HY2.0-4P-WT

- JLCPCB: **C722729**
- Mounting: SMD right-angle
- Pitch: 2.0 mm
- Board plan envelope: **12.0 mm × 7.9 mm**
- Height above board: **5.1 mm**

#### Candidate B — XUNPU WAFER-HY2.0-4PWB

- JLCPCB: **C3029460**
- Mounting: SMD right-angle
- Pitch: 2.0 mm
- Board plan envelope: **12.0 mm × 9.2 mm**
- Height above board: **5.2 mm**
- Auxiliary solder supportあり

両候補とも幅12 mm級で、基板エッジ付近の物理占有が大きいため、PCB粗配置と外観イメージでは小物として扱わない。

Source basis: JLCPCB exact-part listings.

### 6. Qwiic Connector Physical Reference

BASE側Qwiicの最終BOM型番はまだ固定しない。

UIAPduino本体に採用されているJST SH 4P right-angle connectorを物理基準として使用できる。

Reference part:
- JST **SM04B-SRSS-TB(LF)(SN)**
- UIAPduino BOM / JLCPCB: C160404
- Pitch: 1.0 mm
- Plan envelope: approximately **6.0 mm × 4.32 mm**
- Height above board: **2.9 mm**
- Right-angle SMD

BASE側Qwiicを同系統部品で設計する場合、外観イメージではこの寸法を基準とする。

### 7. Parts Not Yet Dimension-Frozen

以下は機能として存在するが、部品型番またはpackageをまだ固定していないため、実寸イメージへ確定寸法で入れない。

- A action button
- B action button
- dedicated RESET button
- 15 status LEDs
- Secret LED
- left/right 2×12 female sockets for UIAPduino
- right-side terminal blocks
- corresponding 5-pin sockets
- mounting holes for UIAP BASE itself
- BASE-side USB DNP connector footprint
- external crystal package

これらは外観へ与える影響が大きい順に部品候補を固定して寸法を追加する。

### 8. Next Physical-Dimension Priority

実物に近い外観イメージを作るため、次は以下を優先して型番・寸法を決める。

1. **A / B action button**
2. **dedicated RESET button**
3. **right-side terminal block**
4. **2×12 female socket / pin-header stack height**
5. **status LED package**
6. **5-pin socket**
7. **UIAP BASE mounting hole size / positions**

特にボタン、端子台、ソケット高さは基板の見た目と立体感へ大きく影響するため、ICより優先して確定する。
