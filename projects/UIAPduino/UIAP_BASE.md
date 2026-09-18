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

## RESET / MODE Button

UIAPduino CH32V003のリセット機能を利用できる物理スイッチをUIAP BASE側に搭載する方向で進める。

同じスイッチをゲーム選択やモード選択などにも利用する。

現時点では1個のスイッチを基本案とするが、ゲームや操作仕様によっては追加する可能性がある。

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

### RESET / MODE Button

RESET/MODEはBASE MCUファームウェアだけに依存させない。

基本回路：

- push switch：3.3V → BTN_NODE
- BTN_NODE：100k pull-down → GND
- BTN_NODE → CH32V203 PA4 input
- BTN_NODE → N-MOSFET gate
- N-MOSFET source → GND
- N-MOSFET drain → UIAPduino RESET

押下するとMOSFETがハードウェアとして直接UIAPduino RESETをLowにするため、BASE MCU firmwareが停止していてもRESET可能。

同時にPA4で押下時間を読み、BASE単独動作時のMODE操作や長押し判定に利用できる。

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
