"""Verify the actual GLB's material payload and the native edit receipts."""
import copy
import hashlib
import io
import json
import struct
import zipfile
from pathlib import Path
import numpy as np
from PIL import Image

ROOT=Path(__file__).resolve().parent
WORK=ROOT/'work'

def read_glb(path):
    raw=Path(path).read_bytes();magic,version,size=struct.unpack_from('<4sII',raw)
    assert magic==b'glTF' and version==2 and size==len(raw)
    length,kind=struct.unpack_from('<II',raw,12);assert kind==0x4e4f534a
    doc=json.loads(raw[20:20+length]);offset=20+length
    binary_length,kind=struct.unpack_from('<II',raw,offset);assert kind==0x004e4942
    binary=raw[offset+8:offset+8+binary_length]
    assert not any('uri' in value for key in ('buffers','images') for value in doc.get(key,[]))
    return doc,binary

def material_payload(doc,binary,material):
    material=copy.deepcopy(material)
    def resolve(value):
        if isinstance(value,dict):
            result={k:resolve(v) for k,v in value.items()}
            for key in list(result):
                if key.endswith('Texture') and isinstance(result[key],dict) and 'index' in result[key]:
                    info=result[key];texture=doc['textures'][info.pop('index')]
                    image=doc['images'][texture['source']];view=doc['bufferViews'][image['bufferView']]
                    start=view.get('byteOffset',0)
                    pixels=Image.open(io.BytesIO(binary[start:start+view['byteLength']])).convert('RGBA')
                    info['image']={'size':pixels.size,'pixels_sha256':hashlib.sha256(pixels.tobytes()).hexdigest()}
                    info['sampler']=doc.get('samplers',[])[texture['sampler']] if 'sampler' in texture else {}
            return result
        if isinstance(value,list):return [resolve(x) for x in value]
        return value
    return resolve(material)

def verify():
    build=json.loads((WORK/'build-manifest.json').read_text())
    assert all(hashlib.sha256((WORK/name).read_bytes()).hexdigest()==digest for name,digest in build.items()),'Stale build output'
    receipt=json.loads((WORK/'fitted'/'render-receipt.json').read_text())
    assert receipt['glb_sha256']==build['musan-bare-shape.glb'],'Renders do not match model'
    assert all(hashlib.sha256((WORK/'fitted'/(view+'.png')).read_bytes()).hexdigest()==digest for view,digest in receipt['views'].items())
    source,sbin=read_glb(WORK/'source-v12.glb')
    target,tbin=read_glb(WORK/'musan-bare-shape.glb')
    original={m['name']:material_payload(source,sbin,m) for m in source['materials']}
    materials={m['name']:material_payload(target,tbin,m) for m in target['materials']}
    assert all(value==original[name] for name,value in materials.items()),'Material or image changed'
    names={node['name'] for node in target['nodes']}
    assert len(names)==5 and any(name.startswith('tripo_node_') for name in names)
    assert {'Short plush silhouette fibres','Black button eye L','Black button eye R','Small smile'}<=names
    assert not target.get('skins') and not target.get('animations') and not target.get('cameras')
    body_node=next(node for node in target['nodes'] if node['name'].startswith('tripo_node_'))
    assert all('COLOR_0' in primitive['attributes'] and 'TEXCOORD_0' in primitive['attributes']
               for primitive in target['meshes'][body_node['mesh']]['primitives']),'Missing body paint or UVs'
    triangles=0
    for mesh in target['meshes']:
        for primitive in mesh['primitives']:
            assert primitive.get('mode',4)==4
            acc=target['accessors'][primitive['attributes']['POSITION']]
            assert np.isfinite(acc['min']).all() and np.isfinite(acc['max']).all()
            triangles+=target['accessors'][primitive['indices']]['count']//3
    edits=json.loads((WORK/'shape-preservation.json').read_text())
    repair=json.loads((WORK/'sculpt-preservation.json').read_text())
    assert all(v['preserved_uv_colors_topology'] for v in edits.values())
    report={'glb_valid':True,'clothing_removed':True,'retained_materials_match_v12':True,
            'embedded_image_pixels_unchanged':True,'external_uris':0,'nodes':sorted(names),
            'materials':sorted(materials),'triangles':triangles,
            'bytes':(WORK/'musan-bare-shape.glb').stat().st_size,
            'source_v12_sha256':hashlib.sha256((WORK/'source-v12.glb').read_bytes()).hexdigest(),
            'body_surface_repaired':repair,
            'post_repair_shape_stage_uv_colors_topology_preserved':True,
            'runtime_verified':False}
    (WORK/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
    return report

if __name__=='__main__':verify()
