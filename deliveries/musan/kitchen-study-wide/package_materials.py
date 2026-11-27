"""Package the material room and byte-identical v12, preserving both baselines."""
import hashlib
import json
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parent
WORK=ROOT/"work"


def package():
    files={"models/kitchen-study.glb":(WORK/"kitchen-study-materials.glb").read_bytes(),
           "models/musan-butler-detail-v12.glb":(WORK/"musan-butler-detail-v12.glb").read_bytes(),
           "muse/scene-placement.json":(ROOT/"scene-placement.json").read_bytes(),
           "README.md":(ROOT/"MATERIALS.md").read_bytes(),
           "verification-materials.json":(WORK/"verification-materials.json").read_bytes(),
           "material-assignments.json":(WORK/"material-assignments.json").read_bytes()}
    for path in sorted((WORK/"preview-materials").glob("*.png")):
        files["preview/"+path.name]=path.read_bytes()
    assert len([p for p in files if p.startswith("preview/")])==9
    for path in sorted((WORK/"textures").glob("*.png")):
        files["textures/"+path.name]=path.read_bytes()
    for name in ["build_room.py","texture_room.py","render_review.py","verify_materials.py",
                 "compose_materials.py","package_materials.py","requirements-build.txt",
                 "README.md","MATERIALS.md","scene-placement.json"]:
        files["source/"+name]=(ROOT/name).read_bytes()
    sha=lambda data:hashlib.sha256(data).hexdigest()
    with zipfile.ZipFile(ROOT.parent/"Musan_Current_Summary_2026-11-27.zip") as original:
        assert files["models/musan-butler-detail-v12.glb"]==original.read("models/musan-butler-detail-v12.glb")
    report=json.loads(files["verification-materials.json"])
    assert sha(files["models/kitchen-study.glb"])==report["room_sha256"]
    assert report["avatar_unchanged"] and report["metallic_texture_channels_verified"]
    manifest={"created":"2026-11-27","avatar":"Original v12, unchanged; no v13",
              "source_archive":"Musan_Current_Summary_2026-11-27.zip",
              "files":[{"path":p,"bytes":len(data),"sha256":sha(data)} for p,data in sorted(files.items())]}
    files["manifest.json"]=(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n").encode()
    output=ROOT/"Musan_Kitchen_Study_Materials_2026-11-27.zip"
    with zipfile.ZipFile(output,"w",compression=zipfile.ZIP_DEFLATED) as archive:
        for name,data in sorted(files.items()):
            info=zipfile.ZipInfo(name,date_time=(2026,11,27,13,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o644<<16
            archive.writestr(info,data)
    with zipfile.ZipFile(output) as archive:
        assert archive.testzip() is None
        for item in manifest["files"]:
            data=archive.read(item["path"])
            assert len(data)==item["bytes"] and sha(data)==item["sha256"]
        assert not any("v13" in name for name in archive.namelist())
    print(f"Verified {len(manifest['files'])} files; {output.stat().st_size} bytes; SHA-256 {sha(output.read_bytes())}")


if __name__=="__main__":
    package()
