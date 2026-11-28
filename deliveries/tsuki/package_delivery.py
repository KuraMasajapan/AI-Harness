"""Compose the review images and build the checked delivery ZIP."""
import hashlib
import json
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = Path(__file__).resolve().parent
WORK = HERE / "work"
VIEWS = {"front": (274, 234), "side": (743, 260), "back": (1276, 260)}
ARCHIVE = "Tsuki_Rigged_Owl_2026-11-28.zip"


def board(left, right, title, subtitle, labels):
    w, h = left.size
    image = Image.new("RGB", (2*w + 72, h + 173), "#f3f1ed")
    draw = ImageDraw.Draw(image)
    draw.rectangle((24, 77, 2*w + 48, 78), fill="#c7b69d")
    draw.text((24, 16), title, fill="#26231f", font=ImageFont.load_default(size=30))
    draw.text((24, 52), subtitle, fill="#635b50", font=ImageFont.load_default(size=16))
    for i, (panel, label) in enumerate(zip((left, right), labels)):
        x = 24 + i*(w + 24)
        image.paste(panel, (x, 104))
        draw.rectangle((x, 103, x+w, h+104), outline="#d4c8b9")
        draw.text((x, h+120), label, fill="#3a332c", font=ImageFont.load_default(size=17))
    return image


def comparisons():
    preview = HERE / "preview"
    preview.mkdir(exist_ok=True)
    source = (Image.open(HERE / "references/three-view.webp").convert("RGB")
              .resize((1550, 1033), Image.Resampling.LANCZOS))
    for name, (cx, half_width) in VIEWS.items():
        crop = source.crop((cx-half_width, 159, cx+half_width, 941))
        left = ImageOps.pad(crop, (500, 640), Image.Resampling.LANCZOS, color="#f0efed")
        right = Image.open(WORK / f"{name}.png").convert("RGB")
        board(left, right, f"TSUKI  /  {name.upper()}", "01   THREE-VIEW COMPARISON",
              ("REFERENCE  /  supplied three-view", "MODEL  /  exported GLB")).save(
            preview / f"{name}-comparison.png")
    left = Image.open(WORK / "head-open.png").convert("RGB")
    right = Image.open(WORK / "head-blink.png").convert("RGB")
    board(left, right, "TSUKI  /  TURN + BLINK", "02   ANIMATION CHECK FROM EXPORTED GLB  /  24 FPS",
          ("FRAME 23  /  turned, eyes open", "FRAME 27  /  turned, eyes closed")).save(
        preview / "head-turn-blink.png")
    scale = json.loads((WORK / "verification.json").read_text())["scale"]
    right = Image.open(WORK / "scale.png").convert("RGB")
    photo = Image.open(HERE / "references/musan-tsuki-scale.png").convert("RGB")
    left = ImageOps.pad(photo, right.size, Image.Resampling.LANCZOS, color="#f0efed")
    board(left, right, "TSUKI + MUSAN  /  SCALE",
          f"03   EXPORTED GLB HEIGHTS  /  TSUKI IS {scale['tsuki_to_musan_height_ratio']:.0%} OF MUSAN",
          ("REFERENCE  /  supplied portrait, feet cropped",
           f"MODELS  /  Musan {scale['musan_height_m']:.3f} m, Tsuki {scale['tsuki_height_m']:.3f} m")).save(
        preview / "scale-comparison.png")


def package():
    comparisons()
    files = {
        "models/tsuki.glb": (WORK / "tsuki.glb").read_bytes(),
        "README.md": (HERE / "README.md").read_bytes(),
        "verification.json": (WORK / "verification.json").read_bytes(),
    }
    for name in ("front-comparison", "side-comparison", "back-comparison", "head-turn-blink",
                 "scale-comparison"):
        path = f"preview/{name}.png"
        files[path] = (HERE / path).read_bytes()
    for name in ("build_tsuki.py", "render_review.py", "feathers.py", "package_delivery.py",
                 "requirements-build.txt", "README.md", "references/three-view.webp",
                 "references/rig-diagram.webp", "references/musan-tsuki-scale.png"):
        files["source/" + name] = (HERE / name).read_bytes()
    manifest = {
        "created": "2026-11-28",
        "latest_model": "models/tsuki.glb",
        "scale": json.loads(files["verification.json"])["scale"],
        "files": [{"path": path, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
                  for path, data in sorted(files.items())],
    }
    files["manifest.json"] = (json.dumps(manifest, indent=2, ensure_ascii=False) + "\n").encode()
    output = HERE / ARCHIVE
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path, data in sorted(files.items()):
            info = zipfile.ZipInfo(path, date_time=(2026, 11, 28, 12, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, data)
    with zipfile.ZipFile(output) as archive:
        assert archive.testzip() is None
        for item in manifest["files"]:
            data = archive.read(item["path"])
            assert len(data) == item["bytes"]
            assert hashlib.sha256(data).hexdigest() == item["sha256"]
    (HERE / "manifest.json").write_bytes(files["manifest.json"])
    sha = hashlib.sha256(output.read_bytes()).hexdigest()
    (HERE / "SHA256SUMS").write_text(f"{sha}  {ARCHIVE}\n")
    print(f"Packaged and verified {len(manifest['files'])} files: {output.name}")
    print(f"{output.stat().st_size:,} bytes; SHA-256 {sha}")


if __name__ == "__main__":
    package()
