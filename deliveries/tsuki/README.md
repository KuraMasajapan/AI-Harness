# ツキ — rigged snowy owl

Unzip [Tsuki_Rigged_Owl_2026-11-28.zip](Tsuki_Rigged_Owl_2026-11-28.zip)
and import `models/tsuki.glb`. The self-contained GLB includes plumage and iris
textures and one 3-second clip, **Tsuki • head turn, tilt & blink**. At 24 fps,
frame 23 shows the eyes open with the head turned; frame 27 shows both eyes
closed while the head is turned and tilted.

- Three-view comparisons: [front](preview/front-comparison.png),
  [side](preview/side-comparison.png), [back](preview/back-comparison.png)
- [Face close-up against the reference](preview/face-comparison.png)
- Rig demo stills: [turned, open vs. closed](preview/head-turn-blink.png)
- Scale: [ツキ next to むーさん, with the supplied portrait](preview/scale-comparison.png)
- Integrity: [per-file manifest](manifest.json) · [ZIP checksum](SHA256SUMS)

## Model and rig

The mesh is a continuous sculpt derived from the supplied front and profile
silhouettes, with separate flight feathers, toes, talons, beak, eyes and lids.
Feather markings and color were baked from the supplied three-view, keeping the
face light and the wings and back more heavily spotted. No paid image-to-3D
service was used. The layering and feather detail are simplified for real-time use.
The revision recesses the smaller eyes under a feathered brow and shades the
sockets, facial disc and bill base. The amber iris uses a dark inner gradient,
radial fibers, and a subdued catchlight beneath a glTF clearcoat. The toes
are wider, fuller, and feathered with dark claws. The hooked bill, cere, and
nostrils retain their previous size.

The rig has 18 deform joints: `Body`, `Neck_01`, `Neck_02`, `Neck_03`, `Head`,
`Tail`, and left/right pairs of `Wing`, `Leg`, `Ankle`, `Toes`, `LidUpper`
and `LidLower`. The diagram lists a ROOT in addition to those 18 joints;
`Tsuki_ROOT` is the armature object, so it moves the entire owl without counting
as a nineteenth joint. GLB playback uses sampled FK rotations; the leg chains
do not ship with Blender IK controls. No changes were made to any Muse space.

The review script renders the **re-imported GLB** and verifies the hierarchy and
eye closure at the turned pose. It measures the exposed eyes from the front
and compares their placement and width, and the foot span, against landmarks
on the supplied sheet. The ZIP includes those measurements in
`verification.json`. Muse/player or mobile performance has not been tested.

## Scale next to むーさん

The exported GLBs measure **0.482503 m (ツキ)** and **1.005214 m (むーさん v12)**
from the bottom to the top of their neutral-pose meshes. ツキ is **48%** of
むーさん's height. In the supplied portrait, ツキ's crown is level with his jacket
pocket, but the photo cuts off both characters' feet, so 48% is an estimate
rather than an exact measurement of the photo. The scale render places both
models on the same floor without independently normalizing their sizes.

## Rebuild

Use Blender 4.5 LTS and a Python environment with `requirements-build.txt`
installed. Run from this directory (or the ZIP's `source/` directory):

```sh
python3 -m pip install -r requirements-build.txt
python3 feathers.py
blender -b --python-exit-code 1 --python build_tsuki.py
blender -b --python-exit-code 1 --python render_review.py
python3 package_delivery.py
sha256sum -c SHA256SUMS
```

The inputs are [the three-view sheet](references/three-view.webp) and
[the rig diagram](references/rig-diagram.webp) plus the
[scale portrait](references/musan-tsuki-scale.png); intermediate files go to `work/`.
The scale render loads `Musan_Current_Summary_2026-11-27.zip` from the adjacent
`musan/` directory. When rebuilding outside the repository, pass
`-- --musan-archive /path/to/Musan_Current_Summary_2026-11-27.zip` to the review command.
Use `blender -b --python-exit-code 1 --python render_review.py -- --check-only`
to verify an existing `work/tsuki.glb` without rendering.
