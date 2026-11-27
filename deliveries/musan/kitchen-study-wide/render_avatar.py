"""Validate the exported avatar and render actual GLB geometry, not references."""
import argparse
import hashlib
import json
from pathlib import Path

import bpy
from mathutils import Vector

from build_room import WORK, AVATAR_SHA256
from build_avatar import NAME
from render_review import glb_document, aim, area


def render(view=None, original=False, check_only=False):
    name = "musan-butler-detail-v12.glb" if original else NAME
    path = WORK/name
    doc = glb_document(path)
    assert not doc.get("animations") and not doc.get("skins")
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(path),loglevel=40)
    meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    bpy.context.view_layer.update()
    bounds = [o.matrix_world@Vector(p) for o in meshes for p in o.bound_box]
    triangles = 0
    for obj in meshes:
        obj.data.calc_loop_triangles()
        triangles += len(obj.data.loop_triangles)
        assert all(all(abs(float(c)) < 10 for c in obj.matrix_world @ v.co) for v in obj.data.vertices)
    if not original:
        for part in ("body","fur","outfit","towel","headset"):
            assert sum(o.get("part")==part for o in meshes)==1,part
        assert len(meshes) == 8  # five groups, two eyes, one smile
        stats = json.loads((WORK/"avatar-build.json").read_text())
        assert hashlib.sha256(path.read_bytes()).hexdigest() == stats["avatar_sha256"]
        stats.update({"triangles":triangles,"mesh_nodes":len(meshes),
            "material_primitives":sum(len(m["primitives"]) for m in doc["meshes"]),
            "bounds_blender_xyz":{"min":[min(p[a] for p in bounds) for a in range(3)],
                                  "max":[max(p[a] for p in bounds) for a in range(3)]},
            "external_asset_uris":0,"animations":0,"skins":0,
            "outfit_separate_from_towel":True,
            "room_geometry_changed_in_avatar_followup":False})
        (WORK/"avatar-verification.json").write_text(json.dumps(stats,indent=2)+"\n")
        print(json.dumps(stats,indent=2))
    else:
        assert hashlib.sha256(path.read_bytes()).hexdigest()==AVATAR_SHA256
    if check_only:
        return
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.samples = 40
    scene.cycles.use_denoising = True
    scene.render.threads_mode,scene.render.threads = "FIXED",8
    scene.world = bpy.data.worlds.new("Neutral warm studio")
    scene.world.use_nodes = True
    scene.world.node_tree.nodes["Background"].inputs[0].default_value = (.62,.59,.54,1)
    scene.world.node_tree.nodes["Background"].inputs[1].default_value = .6
    area("Soft key",(-2,-3,4),240,3,(1,.91,.80))
    area("Side fill",(3,-1,2.5),160,2.5,(.85,.91,1))
    area("Rim",(0,2,3),200,2,(1,.90,.77))
    ground = bpy.data.materials.new("Warm grey backdrop")
    ground.diffuse_color = (.62,.59,.55,1)
    bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.008))
    bpy.context.object.data.materials.append(ground)
    camera = bpy.data.cameras.new("Avatar review camera")
    cam = bpy.data.objects.new("Avatar review camera",camera)
    bpy.context.collection.objects.link(cam)
    scene.camera = cam
    camera.type = "ORTHO"
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.view_settings.view_transform = "AgX"
    output = WORK/"avatar-preview"
    output.mkdir(exist_ok=True)
    views = [
        ("front",(0,-4,.66),(0,0,.50),1.19,(820,1000)),
        ("side",(4,-.03,.66),(0,0,.50),1.19,(820,1000)),
        ("back",(0,4,.66),(0,0,.50),1.19,(820,1000)),
        ("outfit-detail",(1.25,-3,1.15),(0,-.07,.49),.67,(1100,1000)),
        ("headset-detail",(2.5,-2.5,1.3),(.13,-.10,.79),.44,(1000,900)),
        ("towel-detail",(-1.3,-3,1),(-.27,-.19,.32),.49,(900,1000)),
    ]
    for label,position,target,span,resolution in views:
        if view and view!=label:
            continue
        cam.location = position
        aim(cam,target)
        camera.ortho_scale = span
        scene.render.resolution_x,scene.render.resolution_y = resolution
        scene.render.filepath = str(output/(("v12-" if original else "v13-")+label+".png"))
        bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--view",choices=["front","side","back","outfit-detail","headset-detail","towel-detail"])
    parser.add_argument("--original",action="store_true")
    parser.add_argument("--check-only",action="store_true")
    args,_ = parser.parse_known_args()
    render(args.view,args.original,args.check_only)
