# AI音声会話向けリアルタイムノイズ除去 OSS 比較

- Date: 2026-11-21
- Scope: デスクトップ/ノートPCのローカルAI音声入力（USB卓上マイク・着用型クリップマイク）
- Status: KNOWLEDGE / FUTURE VALIDATION CANDIDATE / NOT IMPLEMENTED
- Stage 1: A+
- Stage 2: A+（公式実装と機能を確認。個別ハード・音声認識精度の比較は未実施）
- Evidence: CONFIRMED（公式コード・記載機能）/ UNVERIFIED（対象PCでの負荷・日本語STTへの影響・音質優劣）
- Decision: CANDIDATE
- Prior work: `incubator/proposals/2026-10-14-speech-cpp-local-voice-preferred-candidate.md`; 音声対話ランタイムの優先方針は変更しない。
- Authorization: Humanの2026-11-21「B以上のものは保存までを評価の作業完了」による研究候補保存。実装・本番採用は未承認。

## 要点

ノイズ抑制（NS）、音響エコーキャンセル（AEC）、音声区間検出（VAD）、自動ゲイン調整（AGC）は異なる機能。特にPCスピーカーからAI音声を再生する場合は、NSだけでなく再生音を参照したAECが重要。マイクが近接したクリップ型でもスピーカー回り込みは完全に防げない。

## 候補と一次資料

| 候補 | 主な機能 | 特徴・想定用途 | 公式資料 |
|---|---|---|---|
| RNNoise（最初に検証） | RNNベースのNS | 軽量なリアルタイム背景雑音抑制。CPU-onlyマイク入力で第一候補 | https://github.com/xiph/rnnoise |
| WebRTC Audio Processing (APM) | AEC・NS・AGC等 | PCスピーカー併用で優先。入力と再生側の同期・参照信号配線が必要 | https://webrtc.googlesource.com/src/ / https://github.com/strands-labs/pywebrtc-audio |
| DeepFilterNet | ディープラーニングベースの音声強調/NS | ノイズの多い環境の高品質比較候補。CPU負荷・遅延を測る | https://github.com/Rikorose/DeepFilterNet |
| SpeexDSP | 従来型NS・AEC・AGC・VAD等 | 低負荷なDSP処理とAECの比較候補 | https://github.com/xiph/speexdsp |
| NoiseTorch | Linuxの仮想マイク方式、RNNoiseを利用 | Linux環境でGUIを使った簡易評価に適する。Windows用としては推奨しない | https://github.com/noisetorch/NoiseTorch |
| Windows専用XMic（追加調査候補） | WebRTC AEC3・RNNoise・AGC・VAD等 | Windowsの実機評価候補。ただし新規・第三者実装の安全性、ビルド出所、保守状況を別途確認 | https://github.com/mengshouer/XMic |

順位は日本語認識精度のベンチマーク結果ではなく、AI-Harnessへの導入検証優先度。

## 推奨アーキテクチャ（構想・未実装）

USBマイク → （必要ならAEC：再生PCM参照） → NS（まずRNNoise、代替DeepFilterNet） → VAD → STT（既存のspeech.cpp候補など） → LLM → TTS → スピーカー。

- AECが必ずNSより先であるべきかは採用ライブラリの推奨パイプライン・二重処理有無に従って決める。
- Bluetooth/USBやOSの音声ドライバーによる遅延差、OS標準のノイズ除去二重適用、AGCの過剰増幅に注意。
- 近接マイクの場合は最初に無加工の入力と比較する。過度なNSは語頭・小声・子どもの声・破裂音を失わせうる。
- Windows仮想マイク方式とアプリ内蔵方式は別設計。OSSライブラリそのものをインストールしただけでOS全体の入力がノイズ除去されるとは限らない。
- インターネット/外部API不要の構成を優先。使用する各実装のライセンスと依存関係は正式採用前に別途精査。

## 最小検証

1. 無加工/ RNNoise / WebRTC NS+AEC / DeepFilterNet を同じ録音素材・実機で比較。
2. 机の振動、キーボード、ファン、家電、テレビ、AIスピーカーの回り込みを試す。
3. 客観指標は日本語STTのCER/WER、音切れ、誤起動、ダブルトーク時の認識と、CPU/RAM、追加遅延。単に波形が静かになったことを品質の証拠としない。
4. 卓上・クリップ型で口距離と設置条件を固定し測定。入出力デバイス切り替え・PC再起動後の動作を検証。
5. 小さく可逆なPoCのみ実施。必要なら音声処理の比較結果をHumanへ報告して採用判断。

## 参照・関連キーワード

RNNoise、DeepFilterNet、WebRTC APM、AEC3、SpeexDSP、NoiseTorch、音声ノイズ除去、エコーキャンセル、AGC、VAD、speech.cpp、ローカル音声会話、クリップマイク、卓上マイク
