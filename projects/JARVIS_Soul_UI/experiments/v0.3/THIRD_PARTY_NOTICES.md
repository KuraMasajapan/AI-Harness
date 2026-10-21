# Third-party notices

## Runtime dependency

- Three.js **0.180.0 / r180** — MIT License.
- Copyright © 2010–2025 three.js authors.
- Source: https://github.com/mrdoob/three.js/tree/r180
- Official package: https://www.npmjs.com/package/three/v/0.180.0
- Vendored files: `vendor/three.module.min.js`, `vendor/three.core.min.js`.
- Complete license: [vendor/THREE-LICENSE.txt](vendor/THREE-LICENSE.txt).
- The exact dependency and registry integrity are recorded in `package-lock.json`. `scripts/vendor.mjs` copies the official modules and license without altering them.

Retain the license when redistributing these files. No runtime request to a CDN is required.

## Design references (no code or assets incorporated)

- [Born of Data / VoXelo](https://codepen.io/VoXelo/pen/VYexvqY): considered layered light, analytical soft particles and compositing. Its license was not assumed. No code copied; its particle budgets and expensive post-processing were not imported.
- [Jarvis AI Orb / cyber1443](https://github.com/cyber1443/jarvis-ai-orb-web-animation): MIT license inspected; copyright 2026 cyber1443. Considered state interpolation and quality controls. No React implementation, orbital-ring shader or assets copied.
- [Three.js ShaderMaterial documentation](https://threejs.org/docs/pages/ShaderMaterial.html) and [UnrealBloomPass documentation](https://threejs.org/docs/pages/UnrealBloomPass.html): implementation reference. No EffectComposer or UnrealBloomPass source is included; this experiment uses its own small separable blur.

The flow field, scene layout, shaders and research adapters in this experiment are original project code. The existing project's license/policies remain applicable; this notice does not relicense them. Experiment A reuses the project's formal baseline renderer unmodified.
