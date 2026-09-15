# UIAPduino Project Context

## Overview

このファイルは、UIAPduino本体と、その利用・開発環境に関する基本情報をまとめる。

UIAP BASE（仮）など、UIAPduinoを利用した個別製品の設計・仕様・判断履歴は、それぞれ専用ファイルに分離する。

現在の主対象は **UIAPduino Pro Micro CH32V003 V1.4**。

---

## Hardware

### Board

- ボード名：UIAPduino Pro Micro CH32V003 V1.4
- MCU：CH32V003F4U6
- 基板全長：約33.0 mm
- 左右ピン列間隔：約30.0 mm
- ピンホール：24箇所
- マウント穴：3箇所
- USB-Cコネクタ搭載
- 電源：3.3 V / 5 V 選択式

### Pins / Special Notes

- D11（PD1）はSWIO兼用ピン
- SWIOは書き込み・デバッグに関係するため、他用途との競合に注意する
- ピン配置・各通信機能の割り当ては、今後このファイル内で整理・更新する

---

## Development Environment

UIAPduino CH32V003の利用・開発環境に関する情報をここに集約する。

今後、確認できた内容を以下の観点で追加する。

- ファームウェア書き込み方法
- 使用する書き込み・デバッグツール
- SWIOの扱い
- Arduino互換環境での利用方法
- 3.3 V / 5 V使用時の注意点
- UART / I²C / SPIなどの通信機能
- ピン配置と各ピンの役割
- 公式資料・開発者情報・参考資料

未確認の情報は推測で確定せず、必要に応じて一次情報を確認して追加する。

---

## Usage / Product Environment

UIAPduinoは、教育・入門用途を含む小型マイコンボードとして扱う。

UIAPduino本体に関する情報と、UIAPduinoを利用して開発する周辺製品の情報は区別して管理する。

例：

- UIAPduino本体・開発環境 → `UIAPduino.md`
- UIAP BASE（仮）の設計・仕様 → `UIAP_BASE.md`

---

## Related Projects

### UIAP BASE（仮）

UIAPduino CH32V003向けに開発中の周辺開発ボード。

UIAP BASEの以下の情報は、このファイルではなく `UIAP_BASE.md` に記載する。

- BASEの回路・部品構成
- GPIO LED可視化
- BASE側MCU
- ゲーム機能
- RESET / MODE
- 検品モード
- 端子台・ソケット構成
- USB拡張案
- A案 / B案などのアーキテクチャ比較
- コスト・JLCPCB実装方針
- ファームウェア設計方針

---

## Information Management Policy

今後、UIAPduino関連の情報を追加するときは、内容の所属を先に判断する。

### `UIAPduino.md` に記載するもの

- UIAPduino本体の仕様
- CH32V003に関する基本情報
- UIAPduinoのピン・電源・通信・書き込み・デバッグ
- UIAPduinoを使うための開発環境
- 公式資料や参考情報
- UIAPduino全体に関係する情報

### `UIAP_BASE.md` に記載するもの

- UIAP BASE固有の設計
- BASEの部品・回路・レイアウト
- BASE側MCUの役割
- ゲーム・検品・追加機能
- BASEのコスト・製造・試作判断
- BASE固有のA/B案や設計変更

重複記載はできるだけ避け、必要な場合は詳細を持つファイルへの参照を置く。
