"""Validate the shipped GLB, source preservation, and sampled worn coverage."""
import hashlib
import io
import json
import struct
from pathlib import Path
import bpy
import numpy as np
from PIL import Image
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from build import ROOT,WORK,BODY,BODY_SHA

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def read_glb(path):
    raw=Path(path).read_bytes();magic,version,size=struct.unpack_from('<4sII',raw)
    assert magic==b'glTF' and version==2 and size==len(raw)
    n,kind=struct.unpack_from('<II',raw,12);assert kind==0x4e4f534a
    doc=json.loads(raw[20:20+n]);nb,kb=struct.unpack_from('<II',raw,20+n);assert kb==0x004e4942
    binary=raw[28+n:28+n+nb]
    assert not any('uri' in value for key in ('buffers','images') for value in doc.get(key,[]))
    assert len(doc['buffers'])==1 and doc['buffers'][0]['byteLength']<=len(binary)
    for v in doc['bufferViews']:assert v.get('byteOffset',0)+v['byteLength']<=len(binary)
    return doc,binary

def bvh(objects):
    vertices=[];faces=[]
    for obj in objects:
        if obj.type!='MESH':continue
        offset=len(vertices);vertices.extend([obj.matrix_world@v.co for v in obj.data.vertices])
        faces.extend([[offset+i for i in f.vertices] for f in obj.data.polygons])
    return BVHTree.FromPolygons(vertices,faces)

def coverage():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(BODY),loglevel=40)
    body_objects=list(bpy.context.scene.objects);body_tree=bvh(body_objects)
    bpy.ops.import_scene.gltf(filepath=str(WORK/'musan-butler-outfit.glb'),loglevel=40)
    outfit=next(o for o in bpy.context.scene.objects if o not in body_objects)
    assert outfit.name=='ButlerOutfit' and outfit.type=='MESH'
    assert len([o for o in bpy.context.scene.objects if o not in body_objects])==1
    cloth_tree=bvh([outfit]);result={}
    regions={
        'front_torso':[(Vector((x,-3,z)),Vector((0,1,0))) for x in np.linspace(-.235,.235,25) for z in np.linspace(.36,.585,22)],
        'back_torso':[(Vector((x,3,z)),Vector((0,-1,0))) for x in np.linspace(-.235,.235,25) for z in np.linspace(.355,.585,22)],
        'left_sleeve':[(Vector((-3,y,z)),Vector((1,0,0))) for y in np.linspace(-.07,.07,15) for z in np.linspace(.335,.49,20)],
        'right_sleeve':[(Vector((3,y,z)),Vector((-1,0,0))) for y in np.linspace(-.07,.07,15) for z in np.linspace(.335,.49,20)]}
    failures=[]
    for name,rays in regions.items():
        hits=0;uncovered=0;clearances=[]
        for origin,direction in rays:
            bp,_,_,bd=body_tree.ray_cast(origin,direction)
            if bp is None:continue
            hits+=1;cp,_,_,cd=cloth_tree.ray_cast(origin,direction)
            if cp is not None:clearances.append(bd-cd)
            if cp is None or cd>bd+.0005:
                uncovered+=1;failures.append({'region':name,'body_point':list(bp),'clearance':None if cp is None else bd-cd})
        result[name]={'body_hits':hits,'exposed_inside_expected_clothing_region':uncovered,
                      'median_view_ray_clearance':float(np.median(clearances)),
                      'p95_view_ray_clearance':float(np.percentile(clearances,95))}
    # This is a bounded visibility test, not a universal self-intersection proof.
    assert not failures,f'Exposed wearer in covered regions: {failures[:12]}'
    before={o.name:len(o.data.vertices) for o in body_objects}
    outfit.hide_render=True;outfit.hide_set(True)
    assert all(not o.hide_render and not o.hide_get() for o in body_objects)
    assert before=={o.name:len(o.data.vertices) for o in body_objects}
    outfit.hide_render=False;outfit.hide_set(False)
    return result

def verify():
    path=WORK/'musan-butler-outfit.glb';doc,binary=read_glb(path)
    build=json.loads((WORK/'build-manifest.json').read_text())
    assert sha(BODY)==BODY_SHA==build['body_glb_sha256']
    assert sha(path)==build['files'][path.name]
    assert len(doc['nodes'])==1 and len(doc['meshes'])==1
    node=doc['nodes'][0];assert node['name']=='ButlerOutfit' and node['mesh']==0
    assert all(key not in node for key in ('rotation','translation','scale','matrix','children'))
    assert node['extras']['includes_towel'] is False
    assert not doc.get('skins') and not doc.get('animations') and not doc.get('cameras')
    materials=[m['name'] for m in doc['materials']]
    assert not any(any(part in name.lower() for part in ('skin','fur','plush','eye','towel','headset')) for name in materials)
    assert {'Ivory woven cotton','Charcoal botanical jacquard','Black fine wool','Black satin lapels and bow','Brushed warm gold'}<=set(materials)
    triangles=0
    for primitive in doc['meshes'][0]['primitives']:
        assert primitive.get('mode',4)==4 and 'NORMAL' in primitive['attributes'] and 'TEXCOORD_0' in primitive['attributes']
        for index in primitive['attributes'].values():
            a=doc['accessors'][index];v=doc['bufferViews'][a['bufferView']]
            assert a['componentType']==5126
            array=np.frombuffer(binary,dtype='<f4',count=a['count']*{'VEC2':2,'VEC3':3,'VEC4':4}[a['type']],offset=v.get('byteOffset',0)+a.get('byteOffset',0))
            assert np.isfinite(array).all()
        triangles+=doc['accessors'][primitive['indices']]['count']//3
    textures=[]
    for image in doc['images']:
        v=doc['bufferViews'][image['bufferView']];start=v.get('byteOffset',0)
        im=Image.open(io.BytesIO(binary[start:start+v['byteLength']]))
        assert im.width<=512 and im.height<=512;im.load();textures.append({'name':image.get('name'),'size':list(im.size)})
    for kind in ('dressed','outfit'):
        receipt=json.loads((WORK/kind/'render-receipt.json').read_text())
        for name,digest in receipt['assets'].items():assert digest==sha(BODY if name==BODY.name else WORK/name)
        for view,digest in receipt['views'].items():assert digest==sha(WORK/kind/(view+'.png'))
    report={'glb_version':2,'valid_embedded_binary':True,'node_count':1,'mesh_count':1,
        'registration_parts':['ButlerOutfit'],'body_in_outfit':False,'towel_included':False,
        'body_sha256_unchanged':BODY_SHA,'outfit_sha256':sha(path),'bytes':path.stat().st_size,
        'triangles':triangles,'material_batches':len(doc['meshes'][0]['primitives']),
        'materials':materials,'embedded_textures':textures,'coverage_samples':coverage(),
        'visibility_toggle_in_blender_verified':True,'identity_placement':True,
        'rigged':False,'animation_following':False,'Muse_iPhone_runtime_verified':False,
        'coverage_scope':'Sampled torso and upper/middle sleeve regions including fur; not a complete collision proof.'}
    (WORK/'verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
    return report

if __name__=='__main__':verify()
