# Ollama Streaming Failure Reporting: Validation Candidate (2026-10-25)

Status: **CANDIDATE / MEDIUM; KEEP for future local runtime validation**  
Origin: Grok daily report (2026-10-25), independent review  
Primary release: https://github.com/ollama/ollama/releases/tag/v0.40.9  
Official releases: https://github.com/ollama/ollama/releases

## Report and evidence limits
Grok reported that Ollama v0.40.9 improves reporting of mid-stream generation failures on OpenAI Responses and Anthropic Messages streaming interfaces, avoiding silent partial completion. The follow-up review found supporting official release-list / issue material. **Caution**: the individual v0.40.9 tag page also prominently describes Gradium speech checkpoint changes, so a version-to-fix mapping should be checked against the precise upstream issue/commit before version pinning. No local runtime reproduction was performed.

## AI-Harness value
A partial stream treated as a successful completed response could cause an agent to accept incomplete tool results, truncated plans or false success. This is relevant to Ollama / Hermes local runtimes, independent of model intelligence.

## Existing overlap
`core/WORKFLOW.md` already describes failure handling and verification, but these are principles rather than protocol-level stream-completion tests. The gap to evaluate is concrete client/runtime behavior.

## Future minimum test
- Normal completed generation.
- Transport disconnect / interrupted response.
- Model generation failure after some streamed tokens.
- Missing terminal done/stop event, error object and client timeout.
- Verify whether each API/client combination reports failure, avoids marking task success, and can retry safely without duplicate side effects.
- Run on a currently supported stable Ollama version when the local stack is ready; do not pin to v0.40.9 solely based on a social post.

## Decision
**CANDIDATE / KEEP**. No current install, upgrade, production change, or Core rule modification. Research note only.