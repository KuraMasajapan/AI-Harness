# Gemini API CLI — 公式無料枠・利用上限・料金事故防止の詳細調査

- Date: 2026-11-23
- Origin: user requested deeper free tier evaluation of https://github.com/google-gemini/gemini-api-cli
- Status: KNOWLEDGE / FUTURE VALIDATION CANDIDATE / NOT IMPLEMENTED
- Initial Rank: A++
- Secondary Rank: A+ (official billing and pricing confirmed; account-specific quotas and running commands not tested)
- Evidence: CONFIRMED (official published descriptions and pricing) / UNVERIFIED (actual project quotas, individual access rights, account billing setting, beta stability, workload consumption)
- Disposition: CANDIDATE
- Related: incubator/proposals/2026-11-23-google-gemini-api-cli-multimodal-managed-agents.md
- Authorization: Human standing approval for B+ proposal storage. No installation, billing or account changes, production rollout.

## Central point

The OSS CLI binary is free (Apache 2.0), but Gemini API charges or free quotas are tied to the project, model, feature and billing tier, not the CLI. A Google AI Pro or Antigravity subscription does not automatically make all Gemini API calls free. User-specific active quotas must be read in https://aistudio.google.com/rate-limit ; generic published numbers should not be invented.

## Models with Free Tier tokens (Google official pricing verified)

- gemini-3.6-flash: Free Tier standard input/output, availability and rate limit account dependent
- gemini-3.5-flash: Free Tier standard input/output
- gemini-3.5-flash-lite: Free Tier standard input/output; low-cost/default candidate for Harness
- gemini-3.1-flash-lite: Free Tier standard input/output
- gemini-3.1-flash-tts-preview: Free Tier standard input/output (speech synthesis)
- gemini-2.5-flash-preview-tts: Free Tier standard input/output, older preview
- gemini-3.1-flash-live-preview and gemini-2.5-flash-native-audio-preview-12-2025: Free Tier audio in/out in official pricing; actual API support and model availability need checking
- gemini-embedding-2: free text/image/audio/video embedding input in Standard Free Tier

Excluded or paid API endpoints: gemini-3.1-flash-image / -flash-lite-image (Nano Banana) and 2.5-flash-image, image generation; gemini-omni-flash-preview video; Lyria 3 music; Gemini 2.5 Pro Preview TTS, computer-use. Some other Pro models also do not have Free Tier.

Very important: Gemini API CLI README default for `gemini-api generate` = `gemini-4-hydrogen`, whose free eligibility is NOT established in this research. Explicitly pass `--model gemini-3.5-flash-lite` or another verified free model. The advertised default `image`, `video`, `music` commands must not be assumed free.

Free vs standard paid:
- gemini-3.5-flash-lite standard paid $0.30/1M input and $2.50/1M output (price displayed on official site as checked; may be promotional)
- gemini-3.5-flash standard paid $1.50 input, $9.00 output / 1M
- gemini-3.6-flash standard paid $1.50 input, $7.50 output / 1M in previously crawled price
- gemini-3.1-flash-tts-preview paid $1.00 text input and $20.00 audio output / 1M; Free Tier marked Free of charge
- gemini-3.1-flash-lite-image standard paid $0.0336/1K image; Free Tier not available
- gemini-3.1-flash-image standard paid $0.067/1K image; Free Tier not available
- Lyria 3 preview $0.04/30s clip or $0.08/full song; Free Tier not available
Pricing is dynamic, revalidate on each release/use.

## Quotas and resets

Google API rate limits assessed per Google Cloud project, not independent per API key:
- RPM requests per minute
- TPM input tokens per minute
- RPD requests per day (reset at midnight Pacific time), other special IPM/TPD possible
- Any one cap exceeded => 429 RESOURCE_EXHAUSTED
- Effective quotas vary by project/model/preview status; see https://aistudio.google.com/rate-limit . Current account-specific numeric quotas not accessible in research, no reliable universal "X per day."
- A failed 400/500 request is not billed by tokens per Google's FAQ but still may consume rate-limit quota.
- Free plan has no specified monthly replenishment like AWS Quick; central constraint is daily and per-minute quotas; some tools may have distinct monthly quota.

## Search grounding trap

Official pricing lists some free Search grounding for Gemini 2.5 Flash/Lite models (500 RPD) but Search grounding for Gemini 3.x model free tier is listed 'not available' in per-model table. Paid tier lists 5,000 search queries per month free followed by $14/1000, which does NOT imply Gemini 3 free-tier projects can use it for free. Google AI Studio may offer playground testing separately. Preserve distinction. URL context, file search, code execution tool fees depend on the model.

## Managed agents

https://ai.google.dev/gemini-api/docs/agents describes agents with free tier quota, but notes per interaction roughly 100k-3M tokens typical, including internal agentic reasoning loops, and separately charges inference/tool usage at standard rates for paid accounts. Cloud environment compute billed $0 in preview, not necessarily external VM or model inference. Active free agent task counts are not universally published and need project-specific verification. Environments deleted after 7d inactivity and VM sleeps when idle; **not a free always-on VPS**. For self-hosted agent worker, own container/VM cost and security apply. Avoid invoking managed agent before limits are confirmed.

## Billing and security

New accounts Free Tier with some models accessible. Paid upgrade requires linking Cloud billing and possibly $10 minimum prepaid. Google AI Studio Dashboard > Usage shows usage. Prepay credits expire after 12 months and are generally non-refundable; auto reload optional. Postpay available for some accounts. Project spend cap experimental; around ten minute billing latency, long agent jobs can exceed cap. Free Tier project without billing is safest for strict $0. Google Cloud $300 welcome credit (new accounts from March 2026) cannot fund Gemini API; not a usable free bonus.

Google free-tier pricing page says submitted content may be used to improve Google products; paid API terms differ. Do not submit Harness secrets, family data, credentials, unpublished proprietary business documents on Free Tier without permission and appropriate privacy review. API keys stored outside source control (OS credential store) and redacted dry-run is advised.

## Operational recommendation

1. Set up separate Free Tier Google AI Studio project and API key (do not enable billing), inspect quota and model eligibility at https://aistudio.google.com/rate-limit and Pricing.
2. Install pinned binary after checksum verification; first test `gemini-api --usage`/`--schema`/`--dry-run` without touching network/API or secrets.
3. Explicit `gemini-api generate "hello" --model gemini-3.5-flash-lite` once, monitor usage; do not launch image/music/video/Deep Research until verified budget.
4. Test 3.1 Flash TTS with non-sensitive text and check response, eligibility, quota, latency and Japanese accuracy.
5. If agent delegated tasks are needed, create sandboxed throwaway environment, no write permissions to Harness, inspect maximum tokens and runtime cost, track all calls using gates.
6. Record actual RPM/TPM/RPD per model, region and date. No guarantee of fixed quota outside this account.

## Primary sources

- https://github.com/google-gemini/gemini-api-cli
- https://ai.google.dev/gemini-api/docs/pricing
- https://ai.google.dev/gemini-api/docs/rate-limits
- https://ai.google.dev/gemini-api/docs/agents
- https://ai.google.dev/gemini-api/docs/billing
- https://ai.google.dev/gemini-api/docs/api-key
- https://github.com/google-gemini/gemini-api-cli/blob/main/docs/self-hosted/README.md

## Recall triggers

Gemini API CLI, Free Tier, Gemini 3.5 Flash-Lite, Gemini 3.6 Flash, Gemini 3.1 Flash TTS, Google AI Studio, RPD, RPM, TPM, billing, managed agents, Nano Banana, Lyria, API key, spend cap
