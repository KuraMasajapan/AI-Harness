"""Inspect the exported payload, reimport it, and probe the actual sink cavity."""
import hashlib
import io
import json
import struct
import sys
import zipfile
from pathlib import Path

from PIL import Image
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent/'kitchen-study-wide';WORK=ROOT/'work'
sys.path.insert(0,str(BASE))
import render_review
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree

def verify():
    render_review.WORK=WORK
    render_review.review(check_only=True,materials=True)
    path=WORK/'kitchen-study-materials.glb';blob=path.read_bytes()
    doc=render_review.glb_document(path)
    n=struct.unpack_from('<I',blob,12)[0];binary=blob[n+28:]
    images=[];decoded=0
    for item in doc['images']:
        v=doc['bufferViews'][item['bufferView']];offset=v.get('byteOffset',0)
        im=Image.open(io.BytesIO(binary[offset:offset+v['byteLength']]))
        im.load();assert max(im.size)<=1024
        decoded+=im.width*im.height*4
        images.append({'name':item.get('name'),'width':im.width,'height':im.height,'embedded':True})
    assert decoded<=64*1024*1024,decoded
    byname={m['name']:m for m in doc['materials']}
    mapped=[]
    for name in ['Refined '+k for k in ('wall-oak','honey-oak','warm-walnut','floor-oak')]+[
        'Refined woven ivory-linen','Refined woven plum-linen','Honed limestone slab','Fine-grained chopping board']:
        m=byname[name];p=m['pbrMetallicRoughness']
        assert 'baseColorTexture' in p and 'metallicRoughnessTexture' in p and 'normalTexture' in m,name
        mapped.append(name)
    for name in ('Satin champagne brass','Brushed nickel'):
        assert byname[name]['pbrMetallicRoughness']['metallicFactor']>=.85
    assert 'baseColorTexture' in byname['Cloth bindings and foil titles']['pbrMetallicRoughness']
    assert 'baseColorTexture' in byname['Ivory individual page edges']['pbrMetallicRoughness']
    assert not doc.get('animations') and not doc.get('skins')
    # A sink centre must reach the bottom, not an opaque slab under a bowl.
    verts=[];faces=[]
    for o in bpy.context.scene.objects:
        if o.type!='MESH' or o.get('layout_zone')!='kitchen':continue
        start=len(verts);verts.extend(o.matrix_world@v.co for v in o.data.vertices)
        faces.extend([start+i for i in f.vertices] for f in o.data.polygons)
    tree=BVHTree.FromPolygons(verts,faces)
    centre=tree.ray_cast(Vector((-3.31,1.70,1.6)),Vector((0,0,-1)),2)[0]
    border=tree.ray_cast(Vector((-3.635,1.70,1.6)),Vector((0,0,-1)),2)[0]
    assert centre is not None and border is not None
    assert .68<centre.z<.73 and .83<border.z<.86,(centre,border)
    lights=doc['extensions']['KHR_lights_punctual']['lights']
    previous=BASE/'work'/'kitchen-study-materials.glb'
    expected=(render_review.glb_document(previous)['extensions']['KHR_lights_punctual']['lights']
              if previous.exists() else json.loads((ROOT/'approved-evening-lights.json').read_text())['lights'])
    assert lights==expected
    assert len(lights)==4
    background=byname['Photographic sunset beyond both windows']
    assert 'emissiveTexture' in background
    bi=doc['materials'].index(background)
    assert sum(p.get('material')==bi for m in doc['meshes'] for p in m['primitives'])==2
    body=(WORK/'musan-butler-detail-v12.glb').read_bytes()
    assert hashlib.sha256(body).hexdigest()==render_review.AVATAR_SHA256
    archive_path=ROOT.parent/'Musan_Current_Summary_2026-11-27.zip'
    if archive_path.exists():
        with zipfile.ZipFile(archive_path) as z:assert body==z.read('models/musan-butler-detail-v12.glb')
    sources=json.loads((WORK/'material-sources.json').read_text())
    for asset in sources['assets']:
        for f in asset['files'].values():
            assert hashlib.sha256((ROOT/f['path']).read_bytes()).hexdigest()==f['sha256']
    report=json.loads((WORK/'verification-materials.json').read_text())
    assert report['room_triangles']<100000
    assert report['room_bytes']<12*1024*1024
    assert not report['furniture_intrusions']
    report.update({'room_sha256':hashlib.sha256(blob).hexdigest(),'embedded_images':images,
                   'largest_texture_edge':max(max(im['width'],im['height']) for im in images),
                   'decoded_rgba_texture_bytes':decoded,'estimated_rgba_bytes_with_mipmaps':round(decoded*4/3),
                   'textured_pbr_materials_verified':mapped,'material_count':len(doc['materials']),
                   'primitive_draw_batches':sum(len(m['primitives']) for m in doc['meshes']),
                   'original_evening_lights_preserved':True,'original_character_exact_bytes_preserved':True,
                   'original_zip_byte_comparison':archive_path.exists(),'photographic_background_shared_atlas_verified':True,
                   'exterior_3d_geometry':False,'exterior_parallax':False,
                   'sink_centre_height':centre.z,'sink_border_height':border.z,'sink_aperture_verified':True,
                   'source_material_hashes_verified':True,'Muse_iPhone_runtime_verified':False,
                   'fps_verified':False,'actual_gpu_memory_verified':False})
    (WORK/'verification-refined.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='embedded_images'},indent=2))

if __name__=='__main__':verify()
