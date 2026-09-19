# MediaPipe Interactive Segmentation PoC — HEAL3 SNS-Creator

## Purpose
Evaluate whether client-side object/character cutout is technically viable for HEAL3 SNS-Creator on mobile Safari, and determine whether it should become a primary product feature.

## Final Outcome
- Technical PoC: **Succeeded**
- iPhone Safari initialization and inference: **Verified**
- Product adoption as a primary user-facing feature: **Deferred / not primary**
- Reuse value: **High as a technical asset**

## Investigation Path

### 1. Legacy / Pure TypeScript Attempt
An earlier non-AI contour/alpha approach could isolate the rough subject area but produced visibly elliptical output and unstable transparency around head/feet. It was not good enough as the final method.

### 2. MediaPipe Interactive Segmenter Integration
The implementation moved to MediaPipe Tasks Vision with staged diagnostics.

Diagnostic stages:
1. MediaPipe module load
2. WASM loader fetch
3. WASM binary fetch
4. FilesetResolver init
5. Model fetch
6. Native InteractiveSegmenter creation
7. Warmup / first segmentation

This staged diagnostic structure made it possible to separate asset-loading success from native-engine creation failure.

### 3. Failed `.tflite` Path
The original local `magic_touch.tflite` path fetched successfully, but STEP 6 failed on iPhone Safari.

Observed failure included:
- V1 engine creation failure
- Legacy path error around `ExternalFile` initialization

Important lesson:
A fetched model asset does not prove that the native task graph can consume it.

### 4. Successful `.task` Path
A local `interactive_segmentation.task` bundle was added and used through:

```ts
InteractiveSegmenter.createFromOptions(wasmFileset, {
  baseOptions: {
    modelAssetPath: '/models/interactive_segmentation.task',
    delegate: 'CPU'
  }
})
```

After repository confirmation and deployment, iPhone Safari real-device diagnostics showed:
- STEP 6: OK
- STEP 7: OK
- Warmup mask produced successfully

This verified that the `.task` model path worked on the target device.

## Real Image Evaluation
Real HEAL3 result images were tested.

Findings:
- Character extraction quality was much better than expected.
- A difficult character example was almost fully extracted, with only part of one leg missing.
- Changing the official result-screen background from a dark color to a lighter contrasting color materially improved the result.

This suggests that background/subject contrast can strongly affect segmentation quality, and that HEAL3's existing background-color choice can sometimes be used as a practical input-quality control.

## Why the Feature Was Not Promoted to the Primary UX
Despite the technical success, the visible cutout workflow was removed from the current main product path.

Reasons:
- The original avatar imagery is not always high resolution.
- Enlarging a cutout can expose source-image softness.
- The original avatar still remains inside the base result image.
- The result can look duplicated or more heavily edited than intended.
- This conflicts with the product concept of making the official result image "a little nicer" with low effort.

Conclusion:
**Technical success does not automatically imply product fit.**

## Reuse Guidance
Preserve the implementation as a reusable capability.

Potential future uses:
- Extract a specific object or character for a different composition flow
- Turn selected image regions into reusable assets
- Support special templates where the original base image is intentionally restructured
- Future tooling outside the simple main editing flow

## Verification Model Used
The PoC followed this acceptance ladder:

```text
Hypothesis
→ Implemented (agent reported)
→ Repository Confirmed
→ Deployed
→ Device Tested
→ Verified
```

The real-device result overrode implementation-agent claims whenever they differed.

## Product Lesson
For HEAL3 SNS-Creator:
- preserve impressive technical capabilities as assets,
- but promote only the features that improve the posting experience simply and visibly,
- and prefer a lighter UX over exposing advanced editing power by default.
