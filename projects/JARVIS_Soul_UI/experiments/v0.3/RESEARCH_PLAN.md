# Soul v0.3 — rendering research plan

Status: Windows local experiment executed and evidence recorded. This plan was successfully read before implementation. See RESULTS.md for findings and remaining visual acceptance work. The formal renderer has NOT been replaced.

Baseline: `bdd2225403bd9ba3d582a35bd82809f978caa0e7` on `development`.
The source snapshot was obtained in a separate checkout. The formal v0.2 files are untouched.
Execution environment: Windows local, explicitly approved after the original Cloud request. No claim of Cloud execution is made.

## Source findings (verified by inspection)

- `js/soul-renderer.js:10` draws a filled radial-gradient ellipse, filaments and square particles on every frame without `clearRect`. Source-over compositing therefore accumulates coverage. For a constant per-frame alpha a, accumulated alpha is `1 - (1-a)^n`; this is a mathematical prediction, not a pixel measurement.
- The core already has alpha 0.96 at its center, with 0.70 at the next gradient stop. Clearing cannot by itself create an open, translucent center. The ellipse clips the radial gradient to a regular shape.
- Filaments are 2D curves. Particle size is constant. The variable named z is derived from one of seven radius groups, not camera-space depth. There is no perspective, depth-dependent optical softness or genuine volumetric distribution.
- `this.gl = null` means the WebGL branch is inactive. The existing README's WebGL/fallback description does not describe the active implementation.
- Only Listening changes the visual geometry (+0.03 breath scale); Processing, Speaking and Attention do not have distinct rendering behavior.
- The displayed FPS is derived from the selected target interval, not measured render timestamps. Reduced motion selects Eco but does not stop the JavaScript animation loop.

## Experiment A — minimal control

Reuse the baseline drawing routine without invoking its constructor/frame loop. Apply transparent `clearRect` before each draw. Keep core alpha, colors, seeds, particle count, curves and geometry identical so this isolates clearing. Use one shared test clock to render the original and corrected paths at the same size. Capture the first frame, 5 seconds and 15 seconds, including actual timestamps, rendered-frame counts and measured pixel alpha/coverage. Do not present a higher-quality redesign as the minimal correction.

Use a separate lifecycle adapter for real FPS reporting, resize, pause/visibility, reduced motion, quality controls and fallback. Document these changes separately from the one-line visual correction. Retain A's visual limitations in the comparison.

## Experiment B — Three.js/WebGL2

Use a pinned, locally packaged Three.js version and original GLSL, without a framework migration. Proposed scene: perspective camera; open, warped 3D filament ribbons with soft transverse falloff; sparse particles following the same field; a few dim interior light concentrations rather than a filled sphere. Leave negative space through the center. Use near/far modulation of size, brightness and hue. Avoid complete rings and a uniform Fresnel shell.

Use `THREE.Points` with analytical circular falloff, additive blending, transparent materials and disabled depth writes. Generate seeds/attributes once and animate through uniforms. Start with modest counts, then revise only on visual and measured evidence. Keep the coherent field shared by ribbons and particles.

Bloom OFF is the default. Compare a limited-resolution threshold/blur/composite path on the Soul canvas only. A full multi-mip UnrealBloomPass was considered; a smaller custom pass is preferred initially to limit transparent overdraw, render targets and bandwidth. Eco disables Bloom. Balanced and High cap pixel count separately from CSS text/UI resolution.

API: `setInput({ state, audioLevel })`, `setQuality`, `resize`, `render`, `dispose`. Smooth transitions; separate speed/shape/envelope parameters for Ready, Listening, Processing, Speaking and Attention. No real audio or AI input. Context loss switches to a newly created Canvas2D element; never request incompatible contexts on the same canvas.

## Validation and reporting plan

Preserve v0.2 markup/layout in the experiment shell and add clearly labeled research controls. Validate desktop and iPhone-sized portrait layout, keyboard controls, pause/reduced motion, visibility, fallback and resize. Report render interval mean, standard deviation and p95, actual FPS, JS submission time, backing resolution, counts and Bloom setting. GPU timer queries may provide GPU render duration; this is not GPU utilization. Exact CPU/GPU utilization and physical iPhone/iGPU validation remain unmeasured unless actually tested.

Capture Ready for A; Ready, Listening, Speaking and Bloom OFF/ON for B; iPhone-sized Ready; accumulation evidence; short recordings if practical. Inspect screenshots and animation, iterate on remaining visual defects, and distinguish subjective quality assessment from measured performance. Do not call cinematic quality accepted until the visual criteria have been evaluated; final adoption is the Human's decision.

Commit only experiment code/docs/dependencies and optimized previews under `docs/previews/v0.3/`. Verify all pre-existing repository blobs remain unchanged. Publish ordinary GitHub links for Safari access; do not replace the formal renderer.

## References inspected

- [Born of Data](https://codepen.io/VoXelo/pen/VYexvqY): analytical point falloff, additive compositing and layered particle structures considered. Its code is not copied; no unverified license assumption is made.
- [Jarvis AI Orb](https://github.com/cyber1443/jarvis-ai-orb-web-animation): state-target smoothing, quality controls and lifecycle considered. MIT license verified. Its orbital ring composition and React wrapper are not adopted; no source is copied.
- [Three.js ShaderMaterial](https://threejs.org/docs/pages/ShaderMaterial.html) and [UnrealBloomPass](https://threejs.org/docs/pages/UnrealBloomPass.html).
- Packaged dependency: Three.js 0.180.0, MIT, pinned in package-lock.json and vendored locally with its license. No runtime CDN dependency.
