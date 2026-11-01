# Assault Gear Reference for Hangfire

Purpose: Hangfire開発の参考として、Assault Gearの公開情報からゲームメカニクスを研究する。

## Usage
通常、Codexは次だけを必要に応じて読む。
1. `CLEAN_ROOM/HANGFIRE_MAPPING.md`
2. 必要な場合だけ `SOURCE_INDEX.md`
3. 境界確認が必要なら `CLEAN_ROOM/DO_NOT_COPY.md`

## Policy
- Assault GearのソースコードをHangfireへコピーしない
- 元ゲームの画像・音声・マップ・名称・UIをそのまま使用しない
- 元ゲームの具体的なバランス値をそのまま採用しない
- 実装はHangfireのSource of Truthを優先する
- 出所不明・流出と説明されているコードは参照対象にしない
- 参考資料から未定義のHangfire仕様を勝手に補完しない

## Core finding
参考価値が高い要素:
- angle + power + wind による砲撃
- 行動の強さと次手番遅延のtrade-off
- 移動と攻撃で競合するresource
- 多人数チーム砲撃戦
- 地形・位置による戦術
- limited-use tactical modifiers

これは元ゲーム再現仕様ではなく、Hangfire独自実装のための研究資料である。


## Related AI-Harness research — 2026-11-02

- [Reverse Engineering Research Toolkit — 18 repositories + 2 workflows](../../../incubator/proposals/2026-11-02-reverse-engineering-research-toolkit-package.md) は、**権限のあるソフトウェア解析／独立再実装の一般的な研究資料**としてのみ参照する。
- Hangfire固有のクリーンルーム判断は引き続き `CLEAN_ROOM/HANGFIRE_MAPPING.md` と `CLEAN_ROOM/DO_NOT_COPY.md` が優先。今回のリンクはAssault Gear等の解析・ソース取得・固有要素の模倣を新たに許可するものではない。
- ツール導入、元ゲームの調査対象・権限拡大、仕様変更、再実装は一切自動で行わない。
