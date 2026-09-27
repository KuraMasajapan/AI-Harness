# Hangfire — Low-Cost Server Architecture Rule

## Purpose

Hangfireは、無料枠または極低コストの小規模サーバーで運用できることを優先する。

大規模サービス向けの構成を最初から作らない。

---

## 1. Core Goal

目標は、

**最大8人の少人数Roomを、無料枠または低コストの小さなServerで複数同時に処理できること。**

性能・構成の優先順位:

1. Game Stateの正しさ
2. Server authority
3. 安定した少人数Room処理
4. 低CPU / 低Memory
5. 単純なDeployment
6. 将来拡張
7. 大規模Scale

---

## 2. Server Responsibilities

Serverが担当する。

- room state
- players / teams
- turn order
- wind
- projectile authoritative result
- collision result
- damage
- resource
- turn delay
- HP
- elimination
- winner
- input validation
- match log

ServerはGame Stateの正本を保持する。

---

## 3. Client Responsibilities

Clientが担当する。

- rendering
- UI
- input
- animation
- camera
- particles
- explosion effects
- smoke
- screen shake
- local visual interpolation

Visual effectはServerで処理しない。

---

## 4. Avoid Heavy Server Work

PrototypeではServerで次を行わない。

- image processing
- high-resolution terrain rendering
- particle simulation
- audio processing
- complex real-time 3D physics
- continuous expensive simulation when nothing is happening
- unnecessary background jobs
- analytics pipelines
- large persistent state

Game Logicに必要な計算だけ行う。

---

## 5. Projectile Calculation

ProjectileはServer authorityとする。

ただし計算方式は、

- simple
- deterministic
- low-cost

を優先する。

Projectileの見た目の補間や演出はClientで行ってよい。

Serverで毎frame高負荷な描画計算をしない。

---

## 6. Terrain Destruction

地形破壊はGame StateとしてServerが判定する。

ただし、

**高解像度表示画像そのものをServerの破壊判定データにしない。**

推奨:

- low-resolution collision / destruction mask
- simple grid
- compact shape representation

のいずれか。

Visual terrainとauthoritative collision dataを分離してよい。

目標:

- crater
- terrain removal
- projectile collision
- falling / positional effects

を低負荷で処理すること。

---

## 7. Room Model

1 Server processで複数Roomを扱える単純構造を優先する。

概念:

```text
Server
├─ Room A
├─ Room B
├─ Room C
└─ Room D
```

各Roomは最大8人。

RoomごとのStateを分離する。

1 Room専用processを常に1つ起動する設計は、
必要性が出るまで採用しない。

---

## 8. Persistence

Prototype初期では、永続DBを必須にしない。

最初はMemory上のRoom Stateでよい。

必要になった場合のみ永続化を追加する。

現段階では以下を要求しない。

- account database
- ranking database
- replay database
- matchmaking database
- analytics database

---

## 9. Dependencies

次のようなInfrastructureは、明確な必要性が出るまで追加しない。

- Redis
- message queue
- Kubernetes
- service mesh
- distributed cache
- multiple microservices
- dedicated matchmaking service
- separate analytics backend

追加する場合は事前に、

```text
DEPENDENCY:
REASON:
WHY_CURRENT_SIMPLE_ARCHITECTURE_IS_NOT_ENOUGH:
SERVER_COST_IMPACT:
```

を示す。

---

## 10. Network Traffic

送信する情報は必要最小限にする。

Client → Server:
- player input
- action request

Server → Client:
- authoritative result
- state change
- turn change
- match state

Visual-only eventを大量に同期しない。

---

## 11. Idle Cost

Roomが存在しない、または試合が進行していないときに、
不要な高頻度loopを回し続けない。

可能ならevent-drivenまたは低頻度処理を優先する。

---

## 12. Low-Spec Client Compatibility

Server CostとClient Graphicsは別に考える。

Client側も、

- 10年前程度の一般的PC
- high-end GPU不要
- 2D中心
- lightweight effects

を目標とする。

Graphics Qualityを上げるためにServer負荷を増やさない。

---

## 13. ASTRA Rule

ASTRAは新しいBackend / Infrastructureを追加する前に、

1. 現在の無料枠・低コスト目標に必要か
2. 標準機能で代替できないか
3. 既存1-process構成で十分ではないか
4. CPU / Memory / Network / Storageコストを増やさないか
5. Deploymentを複雑化しないか

を確認する。

「将来Scaleするかもしれない」という理由だけでは追加しない。

---

## 14. Acceptance

Server Architecture関連の変更では最低限、

- 1 Room最大8人を処理できる設計である
- ServerがGame Stateの正本である
- Visual処理をServerに持ち込んでいない
- 不要な常時計算がない
- 不要なDB / Cache / Queueを追加していない
- 無料枠または極低コスト運用を妨げる構成になっていない
- Deployment手順が過度に複雑化していない

ことを確認する。

---

## 15. Escalation

無料枠で成立しないことがEvidenceで確認された場合は、

1. 何がCost bottleneckか
2. CPU / Memory / Network / Storageのどれか
3. 何を簡略化できるか
4. 最小の追加費用で何が解決するか

を先に示す。

Infrastructureを先に増やさない。
