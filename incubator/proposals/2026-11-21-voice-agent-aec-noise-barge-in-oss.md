# ローカル音声AI：ノイズ除去・AEC・バージインを統合するOSS候補

- Date: 2026-11-21
- Status: KNOWLEDGE / FUTURE VALIDATION CANDIDATE / NOT IMPLEMENTED
- Stage 1: A+
- Stage 2: A+（公開機能の一次資料を確認、環境別の独立実測は未実施）
- Evidence: CONFIRMED（公開ソース・機能説明）/ UNVERIFIED（実機統合、WindowsでのAEC品質、CPU負荷、日本語会話品質）
- Decision: CANDIDATE
- Scope: Windowsデスクトップ・ノートPCでのローカルAI音声対話
- Related: `incubator/proposals/2026-11-21-realtime-voice-noise-suppression-oss.md`、`incubator/proposals/2026-10-14-speech-cpp-local-voice-preferred-candidate.md`
- Authorization: Humanの2026-11-21「B以上の評価は保存まで完了」の継続指示。研究保存であり、導入/正式採用は未承認。

## 調査の中心課題
AIがスピーカーから発した音を自分のマイクで再認識・再発話しないこと（AEC）、キーボード音・ファン音などを抑えること（NS）、人がAI発話中に話し始めたとき再生や生成を中断すること（barge-in）を、同じ音声パイプラインで実現するOSSを探す。

AEC・NS・VAD・barge-inは別機能。AECとNSがあるだけではbarge-inは完成しない。誤割り込み防止には人の声/残響判別、割り込み検出、出力停止とTTSバッファ処理が必要。

## 候補比較

| OSS | 役割 | 3機能を実現する条件 | 無償・ローカル性 |
|---|---|---|---|
| Speech Core / Soniqo | C++17音声対話フレームワーク | barge-in実装、DeepFilterNet3音声強調、LocalVQE AEC対応モデルを統合・設定 | OSS、CPU・Windows/Linux対応、Apache-2.0（モデルは個別確認） |
| Pipecat | Python音声エージェントパイプライン | RNNoise音声フィルタ・割り込みハンドリングは存在。AECはWebRTC等のトランスポート/追加実装と接続 | OSS BSD-2-Clause、ローカル構成可能だが追加サービス依存に注意 |
| LiveKit Agents | リアルタイム音声エージェント | WebRTC AEC/NSと割り込み機構を接続。適応型割り込みや高度NSはクラウド機能が絡む場合あり | OSS部分とLiveKit Cloud依存部分を区別 |
| LocalVQE | CPU向けAEC+NS+残響抑制のDSP/NNライブラリ | v1.2/1.3は一体処理だがbarge-in機構は持たない。Speech Core等へ接続 | Apache-2.0、推論がローカルCPU |
| XMic | Windowsマイク前処理 | RNNoise+AEC3+VAD Gateを提供。AIのLLM/TTS再生を止めるbarge-inは別途必要 | ローカル、Windows、単体では音声AI全体ではない |

## 重要な一次資料（2026-11-21確認）

- https://github.com/soniqo/speech-core : VAD、STT、TTS、barge-in、音声パイプライン; サポートモデルにDeepFilterNet3・LocalVQE v1.4 AEC。対応モデルの存在を意味し、無設定で全機能が動く保証ではない。
- https://github.com/localai-org/LocalVQE : v1.3 AEC+NS+dereverb、v1.2軽量版、v1.4 AECのみ。どのモデルもスピーカーの音声参照信号を要する。開発者公表のRyzen 9 7900測定値は独立追試なし。Windows実装の評価は未確認。
- https://github.com/pipecat-ai/pipecat 、https://github.com/pipecat-ai/pipecat/blob/main/src/pipecat/audio/filters/rnnoise_filter.py : RNNoiseフィルタ、割り込み制御。
- https://docs.livekit.io/transport/media/noise-cancellation/ 、https://docs.livekit.io/agents/logic/turns/adaptive-interruption-handling/ : WebRTC AEC/NS、クラウド適応型割り込みの区別。
- https://github.com/mengshouer/XMic : Windowsマイク前処理（AEC3/RNNoise/VAD/AGC）。barge-in制御は別。

## Harnessとの重複・判断

- 既存のspeech.cppはHumanが優先したSTT/VAD/TTS対話ランタイムであり、その選好は変更しない。Speech Coreは「AEC・NS・barge-inを同一パイプラインで統合できるか」の比較候補として保持。
- 既存のノイズ除去OSS比較は個別DSP技術の記録。本資料は音声AI全体の中断制御を含む点が追加価値。
- 最初の検証順は Speech Core → Pipecat+AEC → LiveKitの必要に応じた比較が妥当。正式採用順位ではない。

## 最小検証案（未実施）

1. WindowsのUSBスタンド/クリップマイク、PCスピーカーを使用。再生データのfar-end referenceがAECへ到達することを確認。
2. 自分の声なしでAIが発話：誤認識、誤barge-in、ループが起きないか確認。
3. AIが話している途中に人が発話（double-talk）：割り込み検知、音声停止までの遅延、聞き取り文字化の精度を測る。
4. ノイズ下（キーボード、ファン、テレビ）でNSあり/なし・AECあり/なしの日本語STT誤り率とCPU/RAM負荷を評価。
5. Windowsの音声ドライバ、再生デバイス変更、音声前処理の二重適用、ローカル通信権限、第三者モデルライセンスを確認。
6. 効果確認後にのみ実装提案。Harness Core、既存音声系、他の研究候補を自動置換しない。

## Recall triggers
Speech Core、LocalVQE、Pipecat、LiveKit、RNNoise、DeepFilterNet3、AEC、NS、VAD、barge-in、ダブルトーク、自分の声を拾う、ローカル音声AI
