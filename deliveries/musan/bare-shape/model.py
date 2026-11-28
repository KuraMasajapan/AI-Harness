"""Shape-only editing of the original Tripo-derived v12 undercoat mesh."""
import hashlib
import json
import zipfile
from pathlib import Path

import bpy
import numpy as np
from mathutils import Vector

ROOT=Path(__file__).resolve().parent
WORK=ROOT/'work'
SOURCE=ROOT.parent/'Musan_Current_Summary_2026-11-27.zip'
SOURCE_SHA='a656295b226adb614281acfc2e6f61faeba9f1b66abe28dd6b9cdbd4dd11b84d'
KEEP={'Short plush silhouette fibres','Black button eye L','Black button eye R','Small smile'}

def load_original():
    WORK.mkdir(exist_ok=True)
    with zipfile.ZipFile(SOURCE) as z:
        data=z.read('models/musan-butler-detail-v12.glb')
    assert hashlib.sha256(data).hexdigest()==SOURCE_SHA
    path=WORK/'source-v12.glb'
    path.write_bytes(data)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(path),loglevel=40)
    for obj in list(bpy.data.objects):
        if not (obj.name.startswith('tripo_node_') or obj.name in KEEP):
            bpy.data.objects.remove(obj,do_unlink=True)
    return list(bpy.context.scene.objects)

def export(path):
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.export_scene.gltf(filepath=str(path),export_format='GLB',use_selection=True,
        export_apply=True,export_extras=True,export_animations=False,export_cameras=False,
        export_lights=False,export_vertex_color='ACTIVE',export_all_vertex_colors=False)

def positions(obj):
    values=np.empty(len(obj.data.vertices)*3,dtype=np.float32)
    obj.data.vertices.foreach_get('co',values)
    return values.reshape(-1,3)

def render(path,prefix='baseline',views=('front','side','back')):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(path),loglevel=40)
    scene=bpy.context.scene
    scene.render.engine='CYCLES'
    scene.cycles.samples=24
    scene.cycles.use_denoising=True
    scene.render.threads_mode='FIXED';scene.render.threads=8
    scene.render.resolution_x=700;scene.render.resolution_y=800
    scene.render.resolution_percentage=100
    scene.render.film_transparent=True
    scene.world=bpy.data.worlds.new('Neutral studio')
    scene.world.use_nodes=True
    scene.world.node_tree.nodes['Background'].inputs[0].default_value=(1,1,1,1)
    scene.world.node_tree.nodes['Background'].inputs[1].default_value=.5
    scene.view_settings.view_transform='AgX'
    for name,loc,power,size in [('Key',(-2,-3,4),300,3),('Fill',(3,-1,2),150,3),('Rim',(0,3,3),220,2)]:
        data=bpy.data.lights.new(name,'AREA');data.energy=power;data.shape='DISK';data.size=size
        obj=bpy.data.objects.new(name,data);scene.collection.objects.link(obj);obj.location=loc
        obj.rotation_euler=(Vector((0,0,.5))-obj.location).to_track_quat('-Z','Y').to_euler()
    camera=bpy.data.cameras.new('Orthographic review')
    obj=bpy.data.objects.new('Orthographic review',camera);scene.collection.objects.link(obj)
    scene.camera=obj;camera.type='ORTHO';camera.ortho_scale=1.14
    output=WORK/prefix;output.mkdir(exist_ok=True)
    locations={'front':(0,-3,.5),'side':(-3,0,.5),'back':(0,3,.5),'three-quarter':(2,-3,1)}
    for view in views:
        obj.location=locations[view]
        obj.rotation_euler=(Vector((0,0,.5))-obj.location).to_track_quat('-Z','Y').to_euler()
        scene.render.filepath=str(output/(view+'.png'))
        bpy.ops.render.render(write_still=True)
    import json
    receipt={'glb_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
             'views':{view:hashlib.sha256((output/(view+'.png')).read_bytes()).hexdigest() for view in views}}
    (output/'render-receipt.json').write_text(json.dumps(receipt,indent=2))

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--baseline',action='store_true');a=p.parse_args()
    if a.baseline:
        load_original();path=WORK/'musan-bare-baseline.glb';export(path);render(path)
