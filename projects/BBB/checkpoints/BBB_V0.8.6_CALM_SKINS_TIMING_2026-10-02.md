# BBB v0.8.6 Calm Skins + Run Timing — Checkpoint
Date: 2026-10-02

## Human feedback
- 実行開始から完了までの時間を計測したい。
- v0.8.5の新Skinは明るいというより眩しい。
- 公開されているアプリUIデザインギャラリーを参考に、落ち着いた雰囲気へ寄せる。

## Implemented
- 全background jobへelapsed_seconds。
- running中のelapsedは動的更新。
- Historical ImportカードへElapsed / 経過時間。
- Historical Replay reportへelapsed_seconds。
- 4 Skinを低彩度へ再設計:
  - Aurora Mist / オーロラミスト
  - Sand Gold / サンドゴールド
  - Slate Midnight / スレートミッドナイト
  - Dusty Sakura / ダスティサクラ
- pure white、高彩度accent、大きなradial glow、強いgradient/shadowを削減。
- 参考方向: Mobbin / SaaSFrame等の実製品UIギャラリー。特定UIのコピーはしない。

## Validation
- pytest: 50 passed
- compileall: PASS
- UI JS syntax: PASS
- packaged ZIP再展開後pytest: 50 passed
- package: BBB_v0.8.6_Calm_Skins_Run_Timing.zip
- SHA-256: 98dd5b6ae6934a7258f4619b3f3bb710eac3ff018e34d0b479ebae8d3b2e3e19

## Safety
変更なし。Historical Import / Replay / Local AIはSandbox onlyで、Paper / Risk / Liveへ自動影響しない。
