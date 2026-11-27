"""Package only the revised room, unchanged avatar, placement and review evidence."""
import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WORK = ROOT / "work"


def package():
    files = {}
    for name in ["kitchen-study.glb", "musan-butler-detail-v12.glb"]:
        files["models/" + name] = (WORK / name).read_bytes()
    files["muse/scene-placement.json"] = (ROOT / "scene-placement.json").read_bytes()
    files["README.md"] = (ROOT / "README.md").read_bytes()
    files["verification.json"] = (WORK / "verification.json").read_bytes()
    for name in ["wide-room", "floor-clearance", "study-detail"]:
        files["preview/" + name + ".png"] = (WORK / "preview" / (name + ".png")).read_bytes()
    for name in ["build_room.py", "render_review.py", "package_delivery.py", "requirements-build.txt",
                 "README.md", "scene-placement.json"]:
        files["source/" + name] = (ROOT / name).read_bytes()
    manifest = {
        "created": "2026-11-27",
        "source_archive": "Musan_Current_Summary_2026-11-27.zip",
        "source_note": "Rebuild from the repository directory; keep the original archive one directory above the scripts.",
        "files": [{"path": path, "bytes": len(data),
                   "sha256": hashlib.sha256(data).hexdigest()} for path, data in sorted(files.items())],
    }
    files["manifest.json"] = (json.dumps(manifest, indent=2, ensure_ascii=False) + "\n").encode()
    avatar_sha = hashlib.sha256(files["models/musan-butler-detail-v12.glb"]).hexdigest()
    assert avatar_sha == "a656295b226adb614281acfc2e6f61faeba9f1b66abe28dd6b9cdbd4dd11b84d"
    output = ROOT / "Musan_Kitchen_Study_Wide_2026-11-27.zip"
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path, data in sorted(files.items()):
            info = zipfile.ZipInfo(path, date_time=(2026, 11, 27, 12, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, data)
    with zipfile.ZipFile(output) as archive:
        assert archive.testzip() is None
        for item in manifest["files"]:
            data = archive.read(item["path"])
            assert len(data) == item["bytes"]
            assert hashlib.sha256(data).hexdigest() == item["sha256"]
    print(f"Packaged and verified {len(manifest['files'])} files: {output.name}")
    print(f"{output.stat().st_size} bytes; SHA-256 {hashlib.sha256(output.read_bytes()).hexdigest()}")


if __name__ == "__main__":
    package()
