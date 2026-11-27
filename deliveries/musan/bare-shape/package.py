"""Package only the separate bare model; never overwrite the room or v12."""
import hashlib
import json
import zipfile
from pathlib import Path
from verify import verify

ROOT=Path(__file__).resolve().parent
WORK=ROOT/'work'
OUTPUT=ROOT/'Musan_Bare_Shape_2026-11-28.zip'

def package():
    report=verify()
    files={'models/musan-bare-shape.glb':WORK/'musan-bare-shape.glb','README.md':ROOT/'README.md'}
    for name in ['reference-comparison.png','silhouette-comparison.png']:
        files['review/'+name]=WORK/name
    for view in ['front','side','back']:files['review/'+view+'.png']=WORK/'fitted'/(view+'.png')
    for name in ['verification.json','shape-preservation.json','sculpt-preservation.json','silhouette-measurements.json','deformation-fields.json','build-manifest.json','color-adjustment.json','color-measurements.json']:
        files['verification/'+name]=WORK/name
    files['verification/render-receipt.json']=WORK/'fitted'/'render-receipt.json'
    for name in ['model.py','fit.py','retopo.py','color.py','reference.py','compare.py','verify.py','package.py','requirements-build.txt','shape-target.json']:
        files['source/'+name]=ROOT/name
    payload={name:path.read_bytes() for name,path in files.items()}
    manifest={'model':'models/musan-bare-shape.glb','source_v12_sha256':report['source_v12_sha256'],
              'files':{name:{'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()} for name,data in payload.items()}}
    payload['manifest.json']=(json.dumps(manifest,indent=2)+'\n').encode()
    with zipfile.ZipFile(OUTPUT,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for name,data in payload.items():archive.writestr(name,data)
    with zipfile.ZipFile(OUTPUT) as archive:
        assert archive.testzip() is None
        for name,entry in manifest['files'].items():
            assert hashlib.sha256(archive.read(name)).hexdigest()==entry['sha256']
    print(OUTPUT,OUTPUT.stat().st_size,'bytes; CRC and manifest hashes passed')

if __name__=='__main__':package()
