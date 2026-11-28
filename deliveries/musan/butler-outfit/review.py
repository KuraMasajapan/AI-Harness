"""Render the exported wardrobe GLB, not the authoring scene."""
import hashlib
import json
from pathlib import Path
import bpy
from mathutils import Vector
from build import ROOT,WORK,BODY

def render(kind):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    paths=[WORK/'musan-butler-outfit.glb']
    if kind=='dressed':paths.insert(0,BODY)
    for path in paths:bpy.ops.import_scene.gltf(filepath=str(path),loglevel=40)
    scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=40
    scene.cycles.use_denoising=True;scene.render.threads_mode='FIXED';scene.render.threads=8
    scene.render.resolution_x=1000;scene.render.resolution_y=1100;scene.render.resolution_percentage=100
    scene.render.film_transparent=True
    scene.world=bpy.data.worlds.new('Neutral studio');scene.world.use_nodes=True
    bg=scene.world.node_tree.nodes['Background'];bg.inputs[0].default_value=(1,1,1,1);bg.inputs[1].default_value=.5
    scene.view_settings.view_transform='AgX'
    for name,loc,power,size in [('Key',(-2,-3,4),300,3),('Fill',(3,-1,2),150,3),('Rim',(0,3,3),220,2)]:
        data=bpy.data.lights.new(name,'AREA');data.energy=power;data.shape='DISK';data.size=size
        obj=bpy.data.objects.new(name,data);scene.collection.objects.link(obj);obj.location=loc
        obj.rotation_euler=(Vector((0,0,.5))-obj.location).to_track_quat('-Z','Y').to_euler()
    data=bpy.data.cameras.new('Orthographic review');cam=bpy.data.objects.new('Orthographic review',data)
    scene.collection.objects.link(cam);scene.camera=cam;data.type='ORTHO'
    output=WORK/kind;output.mkdir(exist_ok=True)
    target=Vector((0,0,.5 if kind=='dressed' else .36));data.ortho_scale=1.14 if kind=='dressed' else .82
    views={'front':(0,-3,target.z),'side':(-3,0,target.z),'back':(0,3,target.z),'three-quarter':(2,-3,target.z+.12)}
    receipt={'assets':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},'views':{}}
    for view,loc in views.items():
        cam.location=loc;cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
        scene.render.filepath=str(output/(view+'.png'));bpy.ops.render.render(write_still=True)
        receipt['views'][view]=hashlib.sha256((output/(view+'.png')).read_bytes()).hexdigest()
    (output/'render-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')

if __name__=='__main__':
    import sys
    for kind in sys.argv[1:] or ['dressed','outfit']:render(kind)
