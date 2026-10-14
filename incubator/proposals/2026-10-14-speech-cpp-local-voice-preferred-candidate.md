---
status: proposal
created: 2026-10-14
origin: Human-provided speech.cpp v0.8.5 announcement and official GitHub review
human_preference: speech.cpp preferred first candidate
decision: PREFERRED_COMPARISON_CANDIDATE
implementation: HOLD
evaluation: A+
evidence_status: CONFIRMED (official release, published source/benchmarks) / UNVERIFIED (independent reproduction and actual Harness hardware performance)
tags:
  - local-ai
  - speech
  - tts
  - stt
  - asr
  - vad
  - cpu
  - gpu
  - voice-assistant
  - preferred-candidate
trigger_topics:
  - speech.cpp
  - speech-cpp
  - speech synthesis
  - speech recognition
  - local voice
  - family voice agent
  - Japanese TTS
  - low latency audio
  - first audio
  - sherpa-onnx
  - VoiceStudio
  - VibeASR
---

# speech.cpp — ローカル音声対話基盤の暫定第一候補

## Human decision / 2026-10-14

**Humanの明示的な現在の選好:「改めて現状ではspeech.cpp 推しと記録しておこう」。**

- AI-Harnessの将来の**ローカル音声対話（STT / VAD / TTS）実行エンジン**として、speech.cppを**現時点の第一比較・試用候補**として記録する。
- これは**優先して試したいという選好**であり、製品採用、インストール、既存音声構成の置換、定常運用、GitHub Core変更の承認ではない。
- **Implementation: HOLD**。実機条件や具体的な開発タイミングが決まったら比較検証して判断する。
- 他候補を削除しない。用途が異なるVoiceStudio等を無理に同一順位に並べない。

## Official sources checked

- Repo: https://github.com/nyosegawa/speech.cpp
- Release v0.8.5: https://github.com/nyosegawa/speech.cpp/releases/tag/v0.8.5
- Source README: https://github.com/nyosegawa/speech.cpp/blob/v0.8.5/README.md
- Model catalog: https://github.com/nyosegawa/speech.cpp/blob/v0.8.5/docs/models.md
- Platform/install details: https://github.com/nyosegawa/speech.cpp/blob/v0.8.5/docs/install.md
- API/server: https://github.com/nyosegawa/speech.cpp/blob/v0.8.5/docs/server.md
- Official benchmark project: https://github.com/nyosegawa/speech-bench
- 2026-10-14時点の公式リリース情報で評価。リリース日は2026-10-14。エンジンのリポジトリのライセンスはMIT。モデル重みはモデルごとに別ライセンス・制約がある。

## Reasons for current preference

1. **音声対話向けにまとまっている**: C++/ggmlによる一つの実行系で、STT、TTS、Silero VAD、音声ストリーミング、Realtime文字起こしを提供。
2. **低遅延TTS**: Qwen3-TTS 0.6Bのtime-to-first-audioは公式のApple M5 / RTX 2080 GPU測定でそれぞれ35ms / 24ms。会話の応答開始を速める設計に魅力。
3. **軽量な配布形態**: PythonやCUDAを必須とせず、単一コマンド/共有ライブラリで実行できる。**ただしモデルファイル自体は数百MB〜GB級**。
4. **日本語モデル選択**: Qwen3-TTS 0.6B、Irodori-TTS、ReazonSpeech v2、Parakeet 0.6B JA、Qwen3-ASR等の実装。日本語を直接検証できる。
5. **統合しやすい接点**: OpenAI互換の音声APIの一部、Realtime文字起こし、ローカルHTTPサーバー、C API、workerモードを提供。将来の音声→分類→Cloud/Local LLM→発話の中で部品として扱いやすい。

## Important constraints and evidence boundaries

- **v0.8.5はGPUでの高速化が主**: 公式リリースは「CPUだけではv0.8.4と同速度」と明記。GPUなしPCで最新版だけが速くなったとは主張しない。
- **Windows標準版はVulkan前提**: Vulkan loaderがないWindows PCでは公式インストーラーが停止する。Linux x64にはCPU専用の公式バイナリがある。Windows上で完全CPU専用が必要なら別検証。
- **配布バイナリが軽量でもモデルは軽量とは限らない**: 例として標準Qwen3-TTS 0.6Bは1.21GB、Qwen3-ASR 0.6Bは0.84GB、ReazonSpeech v2は0.66GB。メモリ使用量・同時常駐は実測する。
- **ベンチマークは開発者公表値**: Apple M5 / RTX 2080での高速性は独立追試ではない。CPU-onlyや古いi5・8GB RAMの実機性能を保証しない。
- **低TTFA ≠ 音声会話の総遅延**: VAD終話判定、STT認識確定、LLM推論、音声再生開始までをエンドツーエンド測定する。
- **APIの互換は部分的**: 例としてMP3など一部形式は非対応。公式ローカルHTTPサーバーは既定loopbackかつ認証/TLSなし。LANや外部に直接公開しない。
- **品質・安全**: 日本語の子どもの声、雑音、固有名詞、TTS自然さ・音量、モデルと声の利用条件は現物で確認。録音を使った声の再現には権利・同意が必要。
- **新規OSS**: 長期運用、アップデート追従、依存関係リスクは未評価。

## Other options and distinct roles

| Candidate | Role vs speech.cpp | Retention decision |
| --- | --- | --- |
| sherpa-onnx https://github.com/k2-fsa/sherpa-onnx | STT/TTS/他の音声処理を提供する実行基盤。プラットフォーム対応や実機CPU性能の直接比較対象 | KEEP as comparator |
| VibeASR.cpp https://github.com/microsoft/VibeASR.cpp | STT専用。CPUでの音声認識精度・遅延を比較する対象。TTS代替ではない | KEEP as comparator |
| VoiceStudio https://github.com/debpalash/VoiceStudio | 声のデザイン・クローニング・吹替えなど音声**制作ツール**寄り。対話ランタイムと目的が違う | KEEP as separate tool |
| speech.cpp https://github.com/nyosegawa/speech.cpp | 日本語のSTT+VAD+TTSを一体的に動かす音声対話ランタイム | **HUMAN PREFERENCE / FIRST TO EVALUATE** |

Existing Harness reference: `incubator/proposals/2026-10-11-practical-oss-tool-candidates.md` (VoiceStudioの既存候補)。別途 `incubator/proposals/2026-10-14-microsoft-bitnet-cpu-efficient-local-inference.md` にVibeASR.cpp関連記述。

## Minimal future test — NOT STARTED

1. 音声エンジン導入が必要になったとき、実際のCPU、RAM、GPU/Vulkan可否、OS、用途を決める。
2. speech.cppを第一に検証し、必要な環境でsherpa-onnx、STT専用にはVibeASR.cppなどと同じ日本語音声を用いて比較。
3. **品質**: 認識CER/WER、子どもの声・雑音・固有名詞、自然さ、誤認識・誤発話。
4. **速度・資源**: cold start、model load、話し終わり→認識確定、文字列受領→first audio、全体の応答待ち、CPU/RAM/ストレージ・電力。
5. **保守性**: Windows標準配布の制限、Linux CPU版、API差分、プロセス起動停止、モデルライセンス・権限。
6. 効果が実測されたときだけ採用案をHumanに提示する。採用する場合も音声部品の差し替えにとどめ、Harnessの既存権限・記憶・ルーティングを勝手に変更しない。

## Decision summary / recall

- **Current recommendation by Human**: speech.cpp preferred as the first voice-runtime candidate.
- **Analysis ranking**: A+ (favorable but conditional).
- **State**: saved as research; **not installed**, not adopted.
- **Recall when**: 家族向けLocal AI、音声メンバー化、GPUなしPC、STT/TTS比較、日本語音声、低TTFA、音声Gateway設計。
