"""Package the room only; retain source licences and verify every ZIP member."""
import hashlib
import json
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parent;WORK=ROOT/'work';BASE=ROOT.parent/'kitchen-study-wide'

def package():
    report=json.loads((WORK/'verification-refined.json').read_text())
    assert report['avatar_unchanged'] and report['sink_aperture_verified']
    assert report['original_evening_lights_preserved'] and report['room_triangles']<100000
    files={}
    def add(name,path):files[name]=path.read_bytes()
    add('models/kitchen-study.glb',WORK/'kitchen-study-materials.glb')
    add('README.md',ROOT/'README.md')
    add('muse/lighting-evening.json',WORK/'lighting-evening.json')
    placement=json.loads((BASE/'scene-placement.json').read_text())
    placement['layout']['kitchen']='Back-left wall; refined fitted cabinetry, sink, worktops and cooking equipment'
    files['muse/scene-placement.json']=(json.dumps(placement,ensure_ascii=False,indent=2)+'\n').encode()
    add('verification-refined.json',WORK/'verification-refined.json')
    add('refinement.json',WORK/'refinement.json')
    for path in sorted((WORK/'preview-materials').glob('*')):
        if path.suffix in {'.png','.jpg'}:
            assert path.stat().st_mtime>=(WORK/'kitchen-study-materials.glb').stat().st_mtime,('Stale render',path)
            add('preview/'+path.name,path)
    assert len([n for n in files if n.startswith('preview/')])==11
    for path in sorted(ROOT.glob('*.py')):add('source/kitchen-study-refined/'+path.name,path)
    add('source/kitchen-study-refined/approved-evening-lights.json',ROOT/'approved-evening-lights.json')
    add('source/kitchen-study-refined/work/material-sources.json',WORK/'material-sources.json')
    for path in sorted((WORK/'sources').rglob('*')):
        if path.is_file():add('source/kitchen-study-refined/'+str(path.relative_to(ROOT)),path)
    for name in ('build_room.py','texture_room.py','lighting.py','render_review.py','requirements-build.txt','scene-placement.json'):
        add('source/kitchen-study-wide/'+name,BASE/name)
    add('source/kitchen-study-wide/work/kitchen-study.glb',BASE/'work'/'kitchen-study.glb')
    sha=lambda b:hashlib.sha256(b).hexdigest()
    assert sha(files['models/kitchen-study.glb'])==report['room_sha256']
    manifest={'created':'2026-11-28','scope':'Room only. Reuse the existing unchanged v12 character.',
              'room_sha256':report['room_sha256'],
              'files':[{'path':n,'bytes':len(b),'sha256':sha(b)} for n,b in sorted(files.items())]}
    files['manifest.json']=(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode()
    output=ROOT/'Musan_Kitchen_Study_Refined_2026-11-28.zip'
    with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED) as z:
        for n,b in sorted(files.items()):
            info=zipfile.ZipInfo(n,date_time=(2026,11,28,8,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16
            z.writestr(info,b)
    with zipfile.ZipFile(output) as z:
        assert z.testzip() is None
        assert not any(n.endswith('.glb') and 'kitchen-study.glb' not in n for n in z.namelist())
        for f in manifest['files']:
            b=z.read(f['path']);assert len(b)==f['bytes'] and sha(b)==f['sha256']
    result={'file':str(output),'bytes':output.stat().st_size,'entries':len(files),'sha256':sha(output.read_bytes()),'crc_and_all_member_hashes_verified':True,'character_included':False}
    (WORK/'package-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':package()
