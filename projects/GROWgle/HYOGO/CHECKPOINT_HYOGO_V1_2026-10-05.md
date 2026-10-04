# GROWgle — 兵庫県 v1 Checkpoint

更新: 2026-10-05
State: CHECKPOINT / HYOGO_V1_COMPLETE_WITH_BACKLOG

## 完了範囲

兵庫県を以下のブロックでFirst Pass完了。

1. 西播磨〜中播磨
2. 中央播磨〜東播磨
3. 南東部
4. 丹波
5. 但馬
6. 淡路

## 代表的ベンチマーク

- 佐用町「夏のさよう子ども体験くらぶ」
- 三田市「こうみん未来塾」
- 宝塚市「KIDSフェス」
- 尼崎市「あまづくりパビリオン / こども発明プロジェクト」
- 豊岡市「コウノトリを核にしたふるさと教育」
- 洲本市「すもとオープンファクトリー＋」
- 南あわじ市「全15校区アフタースクール」
- 姫路科学館「ジュニア学芸員」
- 加西市「子ども情報誌」
- 宍粟市「森林・木育」
- 熊野的モデルではなく兵庫では地域クラブ・学校体験教育が強い

## 兵庫県で確立した重要知見

### 1. SCHOOL_ONLYが非常に厚い
兵庫型体験教育として、
- 自然学校
- 環境体験
- 海に学ぶ体験
- トライやる・ウィーク
が多数自治体で制度化。

### 2. SUPPORTING_INFRASTRUCTUREが強い
- 地域クラブ
- アフタースクール
- 体験支援制度
- 団体補助
- 学校外活動支援

イベントだけでなく「参加できる仕組み」を保存する必要がある。

### 3. SOURCE_MASTER型が多い
- 科学館
- 公民館
- 児童館
- 子ども情報誌
- 自治体広報
- 大学/高専/研究機関
を年単位で監視する方が効率的。

### 4. 圏域タグが必要
淡路島など、市境をまたぐ企画が多い。
市町村タグだけでなく REGION_CLUSTER を持つ候補。

## データ型候補

- EVENT
- CONTINUOUS_PROGRAM
- CONSTANT_FACILITY
- SCHOOL_ONLY
- SOURCE_MASTER
- SUPPORTING_INFRASTRUCTURE
- REGION_CLUSTER

## 補助タグ候補
- MARITIME
- CULTURE
- GLOBAL / COMMUNICATION
- LIFE_SKILLS
- DIGITAL / AI
- FUTURE_TECH
- CIVIC
- PEER_TEACHING

## BACKLOG優先
- 養父
- 朝来
- 新温泉
- 香美
- 赤穂
- 相生
- 西宮
- 神戸
- 淡路島3市の圏域イベント全抽出

## 次地域
大阪府。

入口候補:
- 大阪市
- 豊中
- 吹田
- 箕面
- 池田
- 茨木
- 高槻
- 枚方
- 東大阪
- 堺
などをブロック分割して進める。

## 再開
「兵庫Checkpointから再開」
または
「大阪へ進めて」
で再開。
