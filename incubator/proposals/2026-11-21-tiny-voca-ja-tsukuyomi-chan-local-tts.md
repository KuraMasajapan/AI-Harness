# Tiny Voca Japanese — つくよみちゃん：超軽量CPUローカル日本語TTS

- Date: 2026-11-21
- Origin: Human提供モデルURL https://huggingface.co/ayousanz/tiny-voca-ja-tsukuyomi-chan
- Source code: https://github.com/ayutaz/tiny-voca/tree/research/japanese-tts
- Source status: 公開GitHub README / docs/japanese-status.md / docs/japanese-comparison.md / docs/licenses/tsukuyomi-chan.md を2026-11-21に確認。Hugging Faceモデルカード本体の直接取得は未確認
- Status: KNOWLEDGE / FUTURE VALIDATION CANDIDATE / NOT IMPLEMENTED
- Stage 1 Rank: A+ 
- Stage 2 Final Rank: A+（公開仕様確認済み、実機・独立品質評価は未検証）
- Evidence: CONFIRMED（公開コードと公式記録にある仕様） / UNVERIFIED（Harness環境の速度、自然さ、運用適合性）
- Decision: CANDIDATE
- Related existing proposal: `incubator/proposals/2026-10-14-speech-cpp-local-voice-preferred-candidate.md`
- Save authorization: Humanの「B以上は保存まで評価作業」「今の音声生成についても保存」に基づく研究候補記録。実装・採用許可ではない

## 概要と確認できた事実

Tiny Voca日本語forkが公開した、つくよみちゃん（CV.夢前黎）の単一音声による日本語TTSモデル。コードはApache-2.0だが、つくよみちゃん由来モデル・生成音声には別の利用条件が適用される。

- CPUのみでPyTorch / ONNX Runtime推論可能。推論中のクラウドAPI・GPU・APIキーは不要（初回モデル・辞書・依存関係取得にはネット接続）。
- 日本語の音素・アクセント・句境界にpyopenjtalk-plusを使用。
- 4,589,131 parameters、PyTorchモデル18,418,638 bytes、最終版のONNX共有4資産21,882,892 bytes（開発者公開記録による）。
- 出力24kHz mono。Python 3.11以上、git/uvを使うコード起動。ローカルWeb画面で再生・WAV保存。
- 公開のWindows ZIP配布は終了。GitHubの `research/japanese-tts` ブランチを使用。
- 独立した第三者のHarness実機再現は未実施。

## 開発者報告の測定値と限界

最終P1モデルについて、Ryzen 9 5900X・4 CPUスレッドの50文測定でPyTorch RTF 0.0208 / RSS約483 MiB、ONNX RTF 0.0341 / RSS約322 MiBと記録。実際のコード起動の既定は2スレッドで、この数字を既定の実測とは見なさない。前段階のM3 E2モデルに関するPiper比較（RTF等）と最終P1の数値を混同しない。

開発者は小規模音声の評価を完了しているが、MOSや日本語全般のアクセント精度、新規OS・空キャッシュでの再現は未確認。感情表現、声の自然さ、長文の品質、連続会話のレイテンシーを実機評価すること。

## AI-Harnessでの位置づけ・重複比較

- 対象: Local AI / Japanese TTS / Agent voice / CPU-only。
- `speech.cpp` はHumanが以前選好したSTT・VAD・TTS一体型のローカル音声対話基盤。今回のTiny Vocaは軽量な**TTSエンジン/モデル**であり完全な代替ではない。speech.cppの優先候補という既存判断は変更しない。
- GPU不要、省メモリ、ローカル完結で少額運用・常駐クラウド非依存の会話音声に適する可能性。
- 単一話者の声が現在のエージェントの性格・外見に合うかは別の課題。STT・VAD・LLM機能は本モデル単独では提供しない。
- ローカルWeb画面があることと、認証付き外部HTTP APIが完成していることを混同しない。外部接続を自動公開しない。

## 利用規約の重要点

つくよみちゃんコーパス由来部分には公式利用規約が適用。開発者のライセンス説明では商用利用可能だが、批判・攻撃用途、特定政治・宗教・思想への賛否勧誘、強い刺激表現の無区分公開、第三者に声質や生成音声の二次利用を許可する配布などは禁止されている。キャラクター利用、再配布、派生モデルは別途規約確認を要する。エージェントを第三者向けサービスとして公開する場合には特に再検討。

公式案内: https://github.com/ayutaz/tiny-voca/blob/research/japanese-tts/docs/licenses/tsukuyomi-chan.md
原規約: https://tyc.rei-yumesaki.net/material/corpus/

## 導入しない最小検証案

1. 公開モデルの取得・ハッシュ照合とライセンス再確認。
2. CPU-onlyの対象PCでcold start / 合成速度 / メモリ / 日本語発音・アクセント・自然さを評価。
3. Piper系とspeech.cpp経由の日本語TTSを同一文・同等条件で比較（同一声でない比較は声質の好みとエンジン品質を分ける）。
4. 自作エージェントへの組み込み方式・外部公開時の権限とライセンスを確認してからHumanに採用案を提示。

## 確認した主資料

- https://github.com/ayutaz/tiny-voca/blob/research/japanese-tts/README.md
- https://github.com/ayutaz/tiny-voca/blob/research/japanese-tts/docs/japanese-status.md
- https://github.com/ayutaz/tiny-voca/blob/research/japanese-tts/docs/japanese-comparison.md
- https://github.com/ayutaz/tiny-voca/blob/research/japanese-tts/docs/licenses/tsukuyomi-chan.md

## Recall triggers

tiny-voca、Tiny Voca Japanese、つくよみちゃん、CPU音声合成、日本語TTS、ONNX、Piper、speech.cpp、ローカルAI音声
