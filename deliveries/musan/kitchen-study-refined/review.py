"""Render the reimported refined GLB with the approved comparison cameras."""
import argparse
import shutil
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent/'kitchen-study-wide'
sys.path.insert(0,str(BASE))
import render_review
import bpy
from mathutils import Vector

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--view');p.add_argument('--quick',action='store_true');p.add_argument('--check-only',action='store_true');p.add_argument('--baseline',action='store_true')
    a=p.parse_args();render_review.WORK=ROOT/'work'
    if a.baseline:
        render_review.WORK=ROOT/'work'/'baseline';render_review.WORK.mkdir(exist_ok=True)
        for name in ('kitchen-study-materials.glb','musan-butler-detail-v12.glb'):
            shutil.copy2(BASE/'work'/name,render_review.WORK/name)
    custom=[('books-detail',(-1.2,-1.25,1.95),(-3.67,.49,.91),2.2,(1600,1400)),
            ('window-detail',(1.10,-1.5,2.0),(1.10,2.19,1.45),1.92,(1400,1300))]
    render_review.review(view='setup-only' if a.view in {v[0] for v in custom} else a.view,quick=a.quick,check_only=a.check_only,materials=True)
    if not a.check_only:
        for name,position,target,span,resolution in custom:
            if a.view and a.view!=name:continue
            scene=bpy.context.scene;cam=scene.camera
            cam.location=position
            cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler()
            cam.data.type='ORTHO';cam.data.ortho_scale=span;cam.data.shift_y=0
            scene.render.resolution_x,scene.render.resolution_y=resolution
            scene.render.filepath=str(render_review.WORK/('draft' if a.quick else 'preview-materials')/(name+'.png'))
            bpy.ops.render.render(write_still=True)
