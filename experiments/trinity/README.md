# TRINITY V0.1 local prototype

This experimental implementation follows the supplied TRINITY V0.1 Implementation
Specification. It is not formally adopted, production-ready, or a claim of semantic
conformance. All changes are contained in experiments/trinity/.

## Run locally

Python 3.10 or newer; standard library only. No installation, database, network,
external service, or model access is required.

From this directory:

```text
python -m unittest discover -s tests -v
```

This one command validates generated records against the JSON Schemas, runs
state-machine, artifact integrity, binding, release, isolation, conformance and
semantic adapter regression tests, and prints PASS/FAIL for all nine required
fixtures. Run the fixture suite with retained audit files using:

```text
python -m fixtures.runner --output .local/fixture-audit
```

Each fixture produces a JSON audit, and test-audit.json contains the sealed Test
Manifest, input hashes and Test Results. Expected results are loaded and sealed
before any checker runs. The fixed response corpus is a **test double**: it tests
the adapter contract and release controls, not real semantic detection quality.
The production semantic regression acceptance threshold remains unresolved.

## Architecture and role boundaries

- A and B receive separately deserialized copies of the same sealed task, with
  no shared workspace, peer outputs, or old transcript references.
- C first receives both sealed analyst artifacts when comparator execution starts.
  Its input includes the canonical task, operator log and explicit comparison
  instructions. C compares once; it does not select a winner or certify truth.
- O is RunManager and the deterministic gates. O validates structure, hashes,
  ordering and routing; it does not interpret task text or perform reasoning.
- H records a separate immutable disposition. H can disagree with C without
  changing C's historical artifact.

The trusted host owns RunManager and ArtifactStore. Reasoning roles receive only
the detached JSON from role_inputs(); do not give roles the controller object,
store directory, host filesystem access or shared model/session history. This
prototype is a local protocol controller, not a sandbox for arbitrary hostile
Python code. A real runtime must provide fresh isolated contexts and enforce that
host boundary. No AI execution engine is included.

Evidence is data. The controller never executes instruction-like artifact text.
Only the explicit task instructions field is routed as task instructions; the
prototype rejects extra analyst input references, source imports and transcripts.
An imported immutable evidence lineage adapter is not included.

## Lifecycle and API

The public API is controller.run_manager.RunManager:

1. create(task) seals a task. Supply title, objective, instructions,
   required_output, constraints and requirements. Each requirement explicitly
   supplies requirement_id, text and material (boolean), declared by the caller.
2. input_manifest(run) returns a clean input descriptor.
   start_analysts(run, a_input, b_input) checks exact descriptor equality before
   either analyst starts. A mismatch invalidates the run.
3. role_inputs(run, "A") / role_inputs(run, "B") return independent input copies.
   register_analyst(run, role, text) seals each externally produced final output.
4. start_comparator(run) returns C's inputs only after both analysts are sealed.
   register_comparator(run, text) seals C's externally produced comparison.
5. disposition(run, decision, ...) logs the human intervention and seals it.
6. freeze(run, exact_text, producer_id) creates the exact user-visible candidate.
7. checks(run, validator, contract) writes separate binding and semantic artifacts.
8. release(run) records RELEASE or DENY. Only RELEASE returns the exact frozen
   text and transitions to RELEASED. A terminal-run attempt returns DENY without
   changing the historical release decision.

A new candidate can be frozen after an unsuccessful check/decision. It gets a new
artifact ID and clears both checks and the prior decision reference. Historical
artifacts remain available. Checks are never retried automatically; invoking
checks twice for the same frozen candidate is rejected. A recorded decision is
immutable. No downstream rewriting is permitted.

Task-changing amendments require an explicit declaration:

```python
replacement = manager.amend(
    run_id,
    {"type": "TASK_AMENDMENT", "reason": "Human changes the objective",
     "changes_task_conditions": True},
    updated_task,
)
```

The old run terminates before the new task/run is created. The manifests link
previous/replacement IDs. Both new analyst starts use identical empvKZ\İÜBš[œ]Ëˆ\™H\È›ÈØ[YK\[ˆ[Y[™Y[™YÛİX][Û‹ÜˆË]ËPKĞˆÚ[›™[‚“›Û‹]\ÚËXÚ[™Ú[™ÈÜ\˜]Üˆ›İXÙ\ÈX^H™HÙÙÙY›Üˆ]Y]È[š™Xİ[™ÈY][Û˜[›X]\šX[[ÈXİ]™HKĞˆÛÛ^È\È[X™\˜][H[˜]˜Z[X›H[ˆ\È›İİ\K‚‚ˆÈÈš[™[™È[™Ù[X[XÈ[YÛ›Y[‚š[™[™ÈÚXÚÜÈ[‹İ\ÚËØØ[™Y]HY[]K\Ú\Ë™\]Z\™YÙX[YKĞ‹ĞËÒ˜\Y˜XİËİ\œ™[\[ˆÛİ\˜ÙH[™XYÙH[™\›Z[˜[Ú[˜[Y][Ûˆİ]\Ëˆ]™]™\‚\Ù\È^Ú[Z[\š]KˆÙ[X[XÈ[YÛ›Y[™XÙZ]™\È[[]]X›H”ÓÓˆİš[™ÜÈ›ÜˆB™^Xİ\ÚË^XİØ[™Y]H[™ÚXÚÙ\ˆÛÛ˜Xİ‚‚˜[Y][Û‹œÙ[X[X×Ø[YÛ›Y[•˜[Y]ÜˆYš[™\ÈHY\\ˆ[\™˜XÙK‚˜[Y][Û‹›ØØ[Ü™]šY]Ë“ØØ[™]šY]Õ˜[Y]ÜˆXØÙ\ÈHÙ\\˜][H™\\™YØØ[œ™]šY]È”ÓÓˆÛÛZ[š[™È\Ú×ÜXÚØYÙWÚ\ÚØ[™Y]WØ\Y˜XİÚY˜Ø[™Y]WØÛÛ[Ú\Ú›İ™[˜[˜ÙH[™™\]Z\™[Y[Ëˆ›İ™[˜[˜ÙH]\İİ\B˜ÚXÚÙ\—ÚYÚXÚÙ\—İ\KÚXÚÙ\—İ™\œÚ[Û‹[Ù[Û˜[YK[Ù[İ™\œÚ[Ûˆ[™›Û\Ú\Ú
ÒKLMˆÙ‚HØ[›ÛšXØ[ÛÛ˜Xİ
KˆHY\\ˆ\š]™\ÈÛÛ™šY×Ú\Úœ›ÛHH™]šY]ÈÛÛ[‚•HØ]HYÈH[š\]YH^Xİ][Û—ÚYˆXXÚ™\]Z\™[Y[›İÈİ\Y\È™\]Z\™[Y[ÚYœİ]\Ë™\ÜÛœÙWÙ]šY[˜ÙH[™›İ\Ëˆ]šY[˜ÙH›ÜˆÓÕ‘T‘QĞÓÓ•QPÕQ]\İ™HB›]\˜[^Ù\œ[ˆHœ›Ş™[ˆ™\ÜÛœÙKˆH”ÓÓˆ\È™XYÛ˜ÙHÛÈİXœÙ\]Y[š[B™Y]ÈØ[››İ[\ˆ][›ØØ][Û‹‚‚[HÛÛ˜YXİ[ÛˆÜˆ^XÚ]HX]\šX[Z\ÜÚ[™È][HZY[ÈRTĞSQÓ‘Q‚•[œ™\ÛÛ™YX]\šX[Ûİ™\˜YÙKZ\ÜÚ[™ËÛX[›Ü›YY˜[Y]Üˆİ]][™œ˜\İXİ\™B™˜Z[\™Kİ[HØØ[™]šY]ÈÜˆ[˜]˜Z[X›H˜[Y]ÜˆZY[ÈS”‘TÓÓ‘Qˆİ\Ú\ÙBHXÛ\™Y™\]Z\™[Y[X\[™ÈZY[ÈSQÓ‘Qˆ\ÈYÙÜ™YØ][Ûˆ\È[ˆB˜[Y][Ûˆ›İ[™\K›İHÛÛ›Û\‰ÜÈ™X\ÛÛš[™Ëˆ›ÙXÙ\ˆÙ[‹]˜[Y][Û‚š\È™Z™XİYˆËX\Ë]˜[Y]Üˆ\È\ØX›Y[[]È[[YHY™XŞXÛH\È™]šY]ÙY‚•HÜİ]\İ]][XØ]H[X[‹İ˜[Y]ÜˆY[]Y\ÎÈ\ÙHİš[™ÜÈ\™Bœ›İ™[˜[˜ÙHY[YšY\œË›İ]][XØ][ÛˆÜ™Y[X[Ë‚‚”™[X\ÙH™\]Z\™\ÈHœ™\Úš[™[™ÈTÔËÙ[X[XÈSQÓ‘Q[X[ˆ\ÜÜÚ][Ûˆ[™˜[™\]Z\™YÙX[Y\Y˜XİËˆRSRTĞSQÓ‘QS”‘TÓÓ‘Qİ[H™\İ[Ë˜ÛÜœ\[ÛˆÜˆZ\ÜÚ[™È\Y˜XİÈ[H™[X\ÙKˆ[X[ˆ\ÜÜÚ][ÛˆXÚ\Ú[Ûˆ˜[Y\Â˜\™H™\Ù\™Y\ÈÜXÚYšYYÈ›È™]ÈXÚ\Ú[Û‹Y[[HÛXŞH\È[™[Y‚‚ˆÈÈİÜ˜YÙH[™]Y]‚’”ÓÓˆ[™”ÓÓ“\ÙHU‹NÚ]İ]“ÓH[™‹ˆXXÚ”ÓÓ“[™H\ÈÛ™H”ÓÓˆ]™[‚•HØ[›ÛšXØ[Ù\šX[^˜][Ûˆ\È]Ûˆ”ÓÓˆÚ]ÛÜYÙ^\ËÛÛ\XİÙ\\˜]ÜœË™[œİ\™WØ\ØÚZOQ˜[ÙK[İ×Û˜[Q˜[ÙKˆÒKLMˆ[Ø^\È\Ú\È]ÈU‹N]\Ë‚“›ÈÜ›ÜÜË[[™İXYÙHØ[›ÛšXØ[^˜][Ûˆİ[™\™\ÈÛZ[YY‚‚•\ÚÈ\Ú^ÛY\ÈÛ›H]ÈİÛˆ\Ú×ÜXÚØYÙWÚ\ÚšY[ˆ\Y˜XİÛÛ[Ú\Úš\Ú\ÈÛÛ[È™XÛÜ™Ú\ÚY][Û˜[H›İXİÈHÛÛ\]HY]Y]H[™[ÜK‚‘]™[ÈØ\œHH\ÚÚZ[ˆ[™[Û›İÛšXØ[H[˜Ü™X\Ú[™È]™[ÜÙ\H\ÈBœ™\İ[[™ÈX[šY™\İÛ˜\Úİˆ[Y\İ[\È\™H[™›Ü›X][Û˜[Û[‚‚\Y˜XİÈ\™HÜ™X]Y^Û\Ú]™[H[™™]™\ˆY]Y›İYÚHTKˆÜ\˜]Ü‚›ÙÈ[šY\È]™H[ˆH\[™[Û›H›İ\›˜[™Y™\™[˜ÙYHH[[]]X›HÙÂ˜\Y˜Xİˆ]Y]Ü™\Z\ˆ™XÛÜ™ÈHÜšYÚ[˜[\Ú^XİYYš\ÚX›H˜[œØÜš\˜[™™X\ÛÛ‹[˜ÛY[™ÈY\ˆ\›Z[˜][Û‹Ü™[X\ÙKÚ]İ]™[Ü[š[™ÈHİ]HÜ‚›[ÙYZ[™ÈÙX[Y›ÜÜØ[Ëˆ]Ù\È›İØ\\™HY[ˆ™X\ÛÛš[™Ë‚‚˜]Y]
[ŠH^ÜÈX[šY™\İË]™[Ë[\™[[Ûˆ[šY\Ë™Xİ\œÚ]™[H™Y™\™[˜ÙY˜\Y˜XİÈ[™˜[Y]HXYÛ›ÜİXÜËˆ[˜[YÛZ\ÜÚ[™È™XÛÜ™È™[XZ[ˆY[YšXX›Bš[ˆ˜[Y]WÜ™XÛÜ™ËˆHXÚ\Ú[Ûˆ™Y™\™[˜Ù\ÈH^Xİ™[X\ÙY\Y˜Xİ‚‚HØØ[^Û\Ú]™HÜš]\ˆX\šÙ\ˆ™Z™XİÈİ™\›\[™È]]][ÛœËˆ›Ü›X[ÛÛ\]Yœ[œÈ™[ØYœ›ÛHš[\Ëˆ[\œ\YÜˆ[˜ÛÛœÚ\İ[›İ\›˜[È˜Z[ÛÜÙY[™œ™\]Z\™HX[X[™]šY]ÎÈHX\šÙ\ˆ\È›İHÜ˜\Ú\™XÛİ™\H›İØÛÛˆš[\Ş\İ[B˜YZ[š\İ˜]ÜœÈØ[ˆ™]Üš]H[œÚYÛ™Y\Ú\ÎÈÚYÛ˜]\™\Ë™[[İH]\İ][Ûˆ[™šÜİ[]™[Y™\œØ\H™\Ú\İ[˜ÙH\™Hİ]ÚYHŒŒK‚‚ˆÈÈØÚ[X\È[™ØÛÜB‚œ›İØÛÛÜØÚ[X\ËÈÛÛZ[œÈ˜YŒŒLLˆ”ÓÓˆØÚ[X\È›Üˆ[™[Ü\È[™\Y˜ÛÛ[Ëˆ\Y˜Xİ›ÙY\È\™H˜[Y]YÙ\\˜][HH\Y˜Xİİ\NÈ[™[ÜB™šY[ÈİXÚ\È[—ÚY[™ÙX[Y\™H›İ\XØ]Y[ˆ]™\H›ÙKˆHÙ™›[™B˜[Y]Üˆ[\[Y[ÈÛ›HH›ØØX[\H\ÙY\™H[™™Z™XİÈ[œİ\ÜYšÙ^]ÛÜ™ÎÈ]\È›İH™\XÙ[Y[›ÜˆHÙ[™\˜[”ÓÓˆØÚ[XH[™Ú[™K‚‚˜ÛÛ™šYËšœÛÛˆ™XÛÜ™Èš^Y[\[Y[][ÛˆÚÚXÙ\È[™[œ™\ÛÛ™YÛÛ™šYİ\˜][Û‚œÚ[Ëˆ]\È\ØÜš\]™K›İHİÚ]Ú]Ø[ˆÚ[™ÙH›İØÛÛÛXŞK‚•S”‘TÓÓ‘Q›YØİ[Y[È™]šY]ËÜ[[YHXÚ\Ú[ÛœËˆ›İØÛÛÜİ]WÛXXÚ[™K›Y™\ØÜšX™\È[İÙY˜[œÚ][ÛœË‚‚“›İ[˜ÛYYˆ[Ù[ËÜÙ\šXÙ\Ë‹RK[\ÜY]šY[˜ÙH›İ][™Ë›ÙXİ[Û‚˜ÛÛ˜İ\œ™[˜ŞKÜ™XÛİ™\K›İ[™ËÛÛœÙ[œİ\ÈØÛÜ™\Ë[˜[\İX˜]KRHÜ˜Ú\İ˜]Ü‹˜]]Û›Û[İ\È™]šY\ËY[ˆÚZ[‹[Ù‹]İYÚØ\\™KÜˆ]]ÛX]XÈÛÜ™HÈ•STÈÂ“TÔÓÓ”È›Û[İ[Û‹ˆÜ[Û˜[Ñ]\™H™X]\™\È™[XZ[ˆİ]ÚYH\È›İİ\K‚‚‚ˆÈÈXØÙ\YZ][HÙ[X[XÈÛİ™\˜YÙH
ŒKPˆŒŒJB‚š[™[™È™[XZ[œÈY[]KÜÙX[Û[™XYÙHÛ›KˆÙ[X[XÈ›İÈİ\Y\ÈH[[]]X›B’[X[ˆ\ÜÜÚ][Ûˆ[™Ü™\™YXØÙ\YZ][HØØİ\œ™[˜Ù\ÈÈH^\›˜[˜[Y]Ü‚š[ˆ\ÜÜÚ][Û—ÚœÛÛˆ[™XØÙ\YÚ][\×ÚœÛÛ‹[Û™ÜÚYHH^\İ[™È\ÚË˜Ø[™Y]H[™ÛÛ˜Xİİš[™ÜËˆXXÚØØİ\œ™[˜ÙH\ÈH\ÜÜÚ][Û‹RQÚ[™^˜\ÙYš][WÚY][WÚ[™^ÜšYÚ[˜[^[™™\]Z\™Y]YKˆ\]X[İš[™ÜÈ\™H›İY\™ÙYÂœ™Z™XİYÙY™\œ™Y[šY\È\™H›İ[˜ÛYYˆHİ\œ™[\ÜÜÚ][ÛˆØÚ[XH\È›Â›Ü[Û˜[Z][HY]Y]Nˆ[XØÙ\Y[šY\È\™H™\]Z\™Yˆ›È^Ù\[Ûˆ\È[™™\œ™Y‚‚•˜[Y]Ü‹™]˜[X]H™]\›œÈÛ™HØš™XİÚ]™\]Z\™[Y[È
H^\İ[™È\ÚÈ›İÜÊB˜[™XØÙ\YÚ][WØÛİ™\˜YÙKˆH]\ˆÛÛZ[œÈÛİ™\˜YÙWİ™\œÚ[ÛH˜XØÙ\YZ][\Ë]ŒŒH‹˜ÚXÚÙ\—İ™\œÚ[ÛˆX]Ú[™È›İ™[˜[˜ÙK˜ÚXÚÙ\—İ™\œÚ[Û‹[X[—Ù\ÜÜÚ][Û—Ø\Y˜XİÚYš[X[—Ù\ÜÜÚ][Û—ØÛÛ[Ú\Ú[™][\ËˆXXÚ›İÈØ\œšY\È][WÚY][WÚ[™^œ™\]Z\™Y]YKİ]\Ë™\ÜÛœÙWÙ]šY[˜ÙK[™›Û˜›[šÈ›İ\È^Z[š[™ÈH™\™Xİ‚”İ]\Ù\È\™HÓÕ‘T‘QÓRTÔÒS‘ËĞÓÓ•QPÕQÕS”‘TÓÓ‘QÛ›KˆÓÕ‘T‘QĞÓÓ•QPÕQœ™\]Z\™H[ˆ^Xİ›Û˜›[šÈØ[™Y]H^Ù\œˆÚXÚÚ[™È^Ù\œ›İ™[˜[˜ÙHÙ\È›İš[™™\ˆÙ[X[XÈÛİ™\˜YÙNˆH^\›˜[˜[Y]Üˆİ\Y\ÈHÙ[X[XÈYÛY[‚•\™H\È›ÈÙ^]ÛÜ™ÜİXœİš[™ÈÛİ™\˜YÙHÛ\ÜÚYšY\ˆ[ˆ›ÙXİ[ÛˆÛÙK‚‚•HÙ[X[XÈ›İ[™\H˜[Y]\ÈİXİ\™KØØİ\œ™[˜ÙHY[]K\ÜÜÚ][Ûˆš[™[™Â˜[™YÙÜ™YØ][Û‹ˆ]YÈ[\WÜÙ][™Ûİ™\˜YÙWÜØ]\ÙšYYÈHİÜ™Y™\İ[‚[™\]Z\™Y][\È]\İ™HÓÕ‘T‘Q›ÜˆÛİ™\˜YÙWÜØ]\ÙšYYˆRTÔÒS‘ËĞÓÓ•QPÕQœ›ÙXÙHRTĞSQÓ‘QÈ[œ™\ÛÛ™YÛİ™\˜YÙHØ[››İ›ÙXÙHSQÓ‘Qˆ^\İ[™È\ÚÂœ™\]Z\™[Y[ÚXÚÜÈ]\İ[ÛÈ\ÜËˆ[\H][\È\™H^XÚ]HX\šÙY[\WÜÙ]]YNÂ˜Xİ[İ\ÈØ]\Ù˜Xİ[ÛˆÙ\È›İÛZ[HYX[š[™Ù[Ûİ™\˜YÙKˆ˜[Y]ÜS›Û™H™[XZ[œÂ•S”‘TÓÓ‘Q[™™[X\ÙHS–K[˜ÛY[™È›Üˆ[ˆ[\HÙ]‚‚“ØØ[™]šY]Õ˜[Y]Üˆ[\ÜÈ[ˆ[™\[™[H›ÙXÙY˜[Y]Üˆ™\İ[Ú]BœØ[YH™\]Z\™[Y[È[™XØÙ\YÚ][WØÛİ™\˜YÙHšY[Ë\È^\İ[™È\ÚËØØ[™Y]B˜š[™[™ÜÈ[™›İ™[˜[˜ÙKˆ[X[‹[ØØ[\™]šY]ËÚ[X[‹\™]šY]È\\ÈØ[››İİXœİ]]B™›Üˆ\ÈÛÛ˜Xİˆ\™H\È›ÈX[X[İ™\œšYHÙˆHİÜ™YS”‘TÓÓ‘Q™\İ[‚•H\İYÜİ]\İ]][XØ]HÚXÚÙ\ˆY[]NÈİš[™ÜÈ\™H›İÜ™Y[X[Ë‚‚“YØXŞHÙ[X[XÈØÚ[XH›ÙY\È™[XZ[ˆ™XYX›HÚ]İ]™]Üš][™ËØ˜XÚÙš[ˆ™]ÛB˜Ü™X]YÙ[X[XÈ™\İ[È[Ø^\È[˜ÛYHÛİ™\˜YÙNÈ™[X\ÙHÚXÚÜÈ]È™\œÚ[Û™Y˜š[™[™È›İYÚHÙ[X[XÈ™XÙZ\˜[Y]Üˆ[™˜Z[ÈÛÜÙY›ÜˆYØXŞKÛZ\ÜÚ[™ËÂœİ[HÛİ™\˜YÙKˆ™[X\ÙHÙ\È›İ[\œ™]YX[š[™ËˆÛš^\™\ÉÈØ]™Y\Y˜XİÂ˜\™H[˜Ú[™ÙYˆš^\™HÙ]‹\ŒXˆ^XİÈS”‘TÓÓ‘Q˜]\ˆ[ˆSQÓ‘Q›Üˆ›Ü™ZYÛ‹\[‚˜[™ÛXØ[™Y]HÛİ™\˜YÙKÚ]š[™[™ÈRSÈ™[X\ÙHS–H[˜Ú[™ÙY‚‚•\İÈ\ÙH^XÚ]HX™[Yš^Y™\™XİË[˜ÛY[™È\˜\˜\ÙH[™ÛÛ˜YXİ[Û‚˜Ø\Ù\ËÈ\İHÛÛ˜Xİˆ^HÈ›İ˜[Y]HH›ÙXİ[ÛˆÙ[X[XÈ[Ù[	ÜÂ˜XØİ\˜XŞKˆ›È[Ù[ÜÙ\šXÙH[YÜ˜][ÛˆÜˆš\ÚÈ‹Ì›ÙXİ[ÛˆÚ[™ÙH\È[˜ÛYY‚