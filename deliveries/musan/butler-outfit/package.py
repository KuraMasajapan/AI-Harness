"""Package only the clothing registration asset, never a re-exported wearer."""
import argparse
import hashlib
import json
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parent;WORK=ROOT/'work'

def sha(data):return hashlib.sha256(data).hexdigest()

def package(reference):
    report=json.loads((WORK/'verification.json').read_text())
    comparison=json.loads((WORK/'comparison-receipt.json').read_text())
    assert sha((WORK/'musan-butler-outfit.glb').read_bytes())==report['outfit_sha256']
    assert comparison['reference_sha256']==sha(reference.read_bytes())
    for kind,digest in comparison['render_receipts'].items():
        assert digest==sha((WORK/kind/'render-receipt.json').read_bytes())
        receipt=json.loads((WORK/kind/'render-receipt.json').read_text())
        assert receipt['assets']['musan-butler-outfit.glb']==report['outfit_sha256']
        for view,png_digest in receipt['views'].items():
            assert sha((WORK/kind/(view+'.png')).read_bytes())==png_digest
    files={
        'models/musan-butler-outfit.glb':(WORK/'musan-butler-outfit.glb').read_bytes(),
        'README.md':(ROOT/'README.md').read_bytes(),
        'reference/IMG_4914.png':reference.read_bytes(),
    }
    for name in ('reference-comparison.png','wearing-review.png'):
        files['previews/'+name]=(WORK/name).read_bytes()
    for kind in ('dressed','outfit'):
        for name in ('front','side','back','three-quarter'):
            files[f'previews/{kind}/{name}.png']=(WORK/kind/(name+'.png')).read_bytes()
        files[f'receipts/{kind}-render.json']=(WORK/kind/'render-receipt.json').read_bytes()
    for name in ('build-manifest.json','comparison-receipt.json','verification.json'):
        files['receipts/'+name]=(WORK/name).read_bytes()
    for name in ('build.py','review.py','compare.py','verify.py','package.py','requirements-build.txt'):
        files['source/'+name]=(ROOT/name).read_bytes()
    registration={'id':'musan-butler-outfit','revision':'surface-fit-long-tailcoat','label':'執事服一式','asset':'models/musan-butler-outfit.glb',
        'root':'ButlerOutfit','part_count':1,'slot':'full_outfit','towel_included':False,'character_included':False,
        'wearer':{'file':'musan-bare-shape.glb','sha256':report['body_sha256_unchanged'],'included':False},
        'placement':{'same_parent_as_wearer':True,'position':[0,0,0],'rotation_quaternion_xyzw':[0,0,0,1],
                     'scale':[1,1,1],'up':'+Y'},
        'rigged':False,'animation_following':False,'runtime_verified':False}
    files['wardrobe.json']=(json.dumps(registration,ensure_ascii=False,indent=2)+'\n').encode()
    manifest={name:{'bytes':len(data),'sha256':sha(data)} for name,data in sorted(files.items())}
    files['manifest.json']=(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode()
    path=ROOT/'Musan_Butler_Outfit_Refined_2026-11-28.zip'
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
        for name,data in sorted(files.items()):z.writestr(name,data)
    with zipfile.ZipFile(path) as z:
        assert z.testzip() is None
        for name,entry in manifest.items():assert sha(z.read(name))==entry['sha256']
    print(json.dumps({'zip':str(path),'bytes':path.stat().st_size,'sha256':sha(path.read_bytes()),
                      'entries':len(files),'body_included':False},indent=2))
    return path

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('reference',type=Path);a=p.parse_args();package(a.reference)
