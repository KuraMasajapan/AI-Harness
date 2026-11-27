"""Recolour the fitted GLB without re-exporting any geometry or surface detail."""
import copy
import hashlib
import json
import struct
from pathlib import Path

import numpy as np
from verify import read_glb

ROOT=Path(__file__).resolve().parent
WORK=ROOT/'work'
PLUSH='Cream plush with brushed pile'
SKIN='Unified cream skin and undercoat'
PALETTE={PLUSH:[.58,.43,.26,1], 'Matte cream fibre':[.58,.43,.26,1]}

def material_positions(doc,binary,name):
    primitive=next(p for m in doc['meshes'] for p in m['primitives']
                   if doc['materials'][p['material']]['name']==name)
    acc=doc['accessors'][primitive['attributes']['POSITION']]
    view=doc['bufferViews'][acc['bufferView']]
    assert acc['componentType']==5126 and acc['type']=='VEC3' and view.get('byteStride',12)==12
    return np.frombuffer(binary,dtype='<f4',count=acc['count']*3,
        offset=view.get('byteOffset',0)+acc.get('byteOffset',0)).reshape(-1,3)

def rim_weight(doc,binary):
    skin=material_positions(doc,binary,SKIN);fur=material_positions(doc,binary,PLUSH)
    fur=fur[((fur>=skin.min(axis=0)-.02)&(fur<=skin.max(axis=0)+.02)).all(axis=1)]
    assert len(fur)>0
    distance=np.concatenate([np.sqrt(((part[:,None,:]-fur[None,:,:])**2).sum(axis=2).min(axis=1))
                             for part in np.array_split(skin,32)])
    t=np.clip((distance-.003)/.010,0,1)
    return 1-t*t*(3-2*t)

def color_arrays(doc,binary):
    """Yield writable RGB streams and their complete, non-interleaved byte ranges."""
    for mesh in doc['meshes']:
        for primitive in mesh['primitives']:
            name=doc['materials'][primitive['material']]['name']
            if name not in (SKIN,PLUSH):continue
            index=primitive['attributes']['COLOR_0'];acc=doc['accessors'][index]
            view=doc['bufferViews'][acc['bufferView']]
            assert acc['componentType']==5126 and acc['type']=='VEC3'
            assert view.get('byteStride',12)==12
            offset=view.get('byteOffset',0)+acc.get('byteOffset',0)
            end=offset+acc['count']*12
            values=np.frombuffer(binary,dtype='<f4',count=acc['count']*3,offset=offset).reshape(-1,3)
            yield name,index,values,offset,end

def certify(source,target):
    before,sbin=read_glb(source);after,tbin=read_glb(target)
    clean=copy.deepcopy(after)
    for old,new in zip(before['materials'],clean['materials']):
        if old['name'] in PALETTE:
            assert new['pbrMetallicRoughness']['baseColorFactor']==PALETTE[old['name']]
            new['pbrMetallicRoughness']['baseColorFactor']=old['pbrMetallicRoughness']['baseColorFactor']
    assert clean==before,'Non-colour GLB structure changed'
    restored=bytearray(tbin);scrubbed=bytearray(sbin);changes={}
    original={index:(name,colors.copy()) for name,index,colors,_,_ in color_arrays(before,sbin)}
    for name,index,colors,start,end in color_arrays(after,tbin):
        old=original[index][1]
        assert np.isfinite(colors).all() and (colors>=0).all() and (colors<=1).all()
        if name==SKIN:
            p=material_positions(before,sbin,SKIN)
            interior=(abs(p[:,0])<.14)&(p[:,1]>.67)&(p[:,1]<.84)&(p[:,2]>.12)
            assert interior.any() and np.array_equal(colors[interior],old[interior]),'Face interior/blush changed'
        else:assert np.all(colors==1),'Fur base is not uniform'
        changes[str(index)]={'material':name,'vertices':len(colors),
            'changed_vertices':int(np.any(colors!=old,axis=1).sum())}
        restored[start:end]=sbin[start:end];scrubbed[start:end]=bytes(end-start)
    assert bytes(restored)==sbin,'Geometry, UVs, normals, indices or image bytes changed'
    return {'source_glb_sha256':hashlib.sha256(Path(source).read_bytes()).hexdigest(),
            'output_glb_sha256':hashlib.sha256(Path(target).read_bytes()).hexdigest(),
            'geometry_uv_normals_images_unchanged':True,'face_interior_and_blush_unchanged':True,
            'non_color_binary_sha256':hashlib.sha256(scrubbed).hexdigest(),
            'palette_linear_rgba':PALETTE,'color_accessors':changes}

def recolor(source,target):
    doc,binary=read_glb(source);binary=bytearray(binary)
    edge=rim_weight(doc,binary)
    for material in doc['materials']:
        if material['name'] in PALETTE:
            material['pbrMetallicRoughness']['baseColorFactor']=PALETTE[material['name']]
    for name,_,colors,_,_ in color_arrays(doc,binary):
        if name==PLUSH:
            # Reprojection had carried some face paint onto the fur rim.
            colors[:]=1
        else:
            # Only neutral/white rim vertices; keep the existing face and blush.
            weight=np.clip((colors[:,2]-.46)/.44,0,1)
            weight=weight*weight*(3-2*weight)
            weight=1-(1-weight)*(1-edge)
            colors[:]=colors*(1-weight[:,None])+np.asarray(PALETTE[PLUSH][:3])*weight[:,None]
    payload=json.dumps(doc,separators=(',',':'),ensure_ascii=False).encode()
    payload+=b' '*((-len(payload))%4)
    raw=struct.pack('<4sII',b'glTF',2,12+8+len(payload)+8+len(binary))
    raw+=struct.pack('<II',len(payload),0x4e4f534a)+payload
    raw+=struct.pack('<II',len(binary),0x004e4942)+binary
    Path(target).write_bytes(raw)
    report=certify(source,target)
    (WORK/'color-adjustment.json').write_text(json.dumps(report,indent=2)+'\n')
    return report

if __name__=='__main__':
    recolor(WORK/'musan-bare-shape-uncolored.glb',WORK/'musan-bare-shape.glb')
    manifest=json.loads((WORK/'build-manifest.json').read_text())
    for name in ['musan-bare-shape.glb','color-adjustment.json']:
        manifest[name]=hashlib.sha256((WORK/name).read_bytes()).hexdigest()
    (WORK/'build-manifest.json').write_text(json.dumps(manifest,indent=2))
