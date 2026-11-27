"""Package the refined avatar with the unchanged wide room and review renders."""
import hashlib
import json
import zipfile

from build_room import ROOT, WORK, AVATAR_SHA256
from build_avatar import NAME


def package():
    report = json.loads((WORK/"avatar-verification.json").read_text())
    assert report["avatar_sha256"] == hashlib.sha256((WORK/NAME).read_bytes()).hexdigest()
    assert report["source_sha256"] == AVATAR_SHA256
    with zipfile.ZipFile(ROOT/"Musan_Kitchen_Study_Wide_2026-11-27.zip") as old:
        assert old.read("models/kitchen-study.glb") == (WORK/"kitchen-study.glb").read_bytes()
    files = {"models/"+NAME:(WORK/NAME).read_bytes(),
             "models/kitchen-study.glb":(WORK/"kitchen-study.glb").read_bytes(),
             "muse/scene-placement.json":(ROOT/"scene-placement-refined.json").read_bytes(),
             "README.md":(ROOT/"AVATAR_REFINEMENT.md").read_bytes(),
             "avatar-verification.json":(WORK/"avatar-verification.json").read_bytes(),
             "room-verification.json":(WORK/"verification-refined.json").read_bytes()}
    for path in sorted((WORK/"avatar-preview").glob("*.png")):
        files["preview/"+path.name] = path.read_bytes()
    files["preview/wide-room.png"] = (WORK/"preview-refined/wide-room.png").read_bytes()
    for name in ["build_room.py","build_avatar.py","render_review.py","render_avatar.py",
                 "package_delivery.py","package_refined.py","compose_previews.py",
                 "scene-placement.json","scene-placement-refined.json","README.md",
                 "AVATAR_REFINEMENT.md","requirements-build.txt"]:
        files["source/"+name] = (ROOT/name).read_bytes()
    manifest = {"created":"2026-11-27","source_archive":"Musan_Current_Summary_2026-11-27.zip",
        "avatar_revision":"v13","room_revision":"wide-room unchanged",
        "files":[{"path":p,"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()} for p,b in sorted(files.items())]}
    files["manifest.json"] = (json.dumps(manifest,indent=2,ensure_ascii=False)+"\n").encode()
    output = ROOT/"Musan_Kitchen_Study_Refined_2026-11-27.zip"
    with zipfile.ZipFile(output,"w",compression=zipfile.ZIP_DEFLATED) as archive:
        for path,data in sorted(files.items()):
            info = zipfile.ZipInfo(path,date_time=(2026,11,27,12,0,0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info,data)
    with zipfile.ZipFile(output) as archive:
        assert archive.testzip() is None
        for item in manifest["files"]:
            data = archive.read(item["path"])
            assert len(data)==item["bytes"]
            assert hashlib.sha256(data).hexdigest()==item["sha256"]
    print(f"Verified {len(manifest['files'])} files; {output.stat().st_size} bytes")
    print(output)


if __name__ == "__main__":
    package()
