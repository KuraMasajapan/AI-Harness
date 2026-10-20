# Local AI Soul UI v0.1

静かな「魂」の存在感を中心にした独立ビジュアルプロトタイプです。添付画像の構図（左ナビ・中央ビジュアル・右ステータス・下部バー）を保ちつつ、発光、粒子、波形、HUD装飾を控えめにしています。

## 起動

```powershell
cd C:\Users\Owner\Documents\ChatGPT\UI_develop_lab\local-ai-soul-ui
python -m http.server 8000
```

`http://localhost:8000/` を開いてください。`file://` 直開きでは ES module 制約のため動作確認しません。

## 実装範囲

- WebGL2 の局所グロー + Canvas 2D の流線・粒子表現
- WebGL2 非対応時の Canvas 2D fallback
- Eco / Balanced / High の描画目安（初期は Balanced）
- Ready / Listening / Processing / Speaking / Attention のデモ切替
- reduced-motion、レスポンシブ、キーボード操作可能なボタン
- 実AI接続、マイク権限、STT/TTS、CPU/VRAM測定は未実装。画面上も Demo / not connected と明示

## 参照画像との差分

レイアウトの大枠と青白い中心発光は継承しています。一方で、中心を単一の静かな塊にまとめ、外周の粒子、強い床反射、大きな同心円、常時動く波形、過剰なHUD装飾は削減しました。性能値はブラウザ上の簡易フレーム目安のみで、実機ベンチマーク結果ではありません。

