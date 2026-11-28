"""Re-import the delivered GLB, verify the skin and animation, and render evidence."""
import json
import sys
from math import degrees
from pathlib import Path

import bpy
from mathutils import Vector

HERE = Path(__file__).resolve().parent
WORK = HERE / "work"
sys.path.insert(0, str(HERE))
from build_tsuki import NECK, eye_frame


def assert_pose(rig, scene):
    def sightline(sign, horizontal=0, vertical=0):
        p, n, u, up = eye_frame(sign)
        p += horizontal * u + vertical * up
        head = rig.pose.bones["Head"]
        pose = head.matrix @ head.bone.matrix_local.inverted()
        transform = rig.matrix_world @ pose
        origin = transform @ (p + n*.38)
        direction = -(transform.to_3x3() @ n)
        hit, _, _, _, obj, _ = scene.ray_cast(bpy.context.evaluated_depsgraph_get(), origin, direction)
        return obj.name if hit else "no intersection"

    scene.frame_set(1)
    neutral = rig.pose.bones["Head"].matrix.to_quaternion()
    opened = [sightline(sign) for sign in (1, -1)]
    scene.frame_set(27)
    turned = degrees(neutral.rotation_difference(rig.pose.bones["Head"].matrix.to_quaternion()).angle)
    turned = min(turned, 360-turned)
    closed = [sightline(sign) for sign in (1, -1)]
    exposed = [sightline(sign, x, y) for sign in (1, -1) for x in (-.087, -.049, 0, .049, .087)
               for y in (-.055, -.028, 0, .028, .055)]
    assert all(name.startswith("Amber eye") for name in opened), opened
    assert all("lid" in name.lower() for name in closed), closed
    assert not any(name.startswith("Amber eye") for name in exposed), exposed
    assert 40 < turned < 60, turned
    scene.frame_set(1)
    return {"rest_eye_center_hits": opened, "frame_27_eye_center_hits": closed,
            "frame_27_test_rays_without_visible_iris": len(exposed),
            "frame_27_head_rotation_degrees": round(turned, 2)}


def aim(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat("-Z", "Y").to_euler()


def light(name, location, energy, size, color):
    data = bpy.data.lights.new(name, "AREA")
    data.energy, data.shape, data.size, data.color = energy, "DISK", size, color
    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    obj.location = location
    aim(obj, (0, 0, 1.44))
    return obj


def studio(scene):
    scene.render.engine = "CYCLES"
    scene.cycles.samples = 14
    scene.cycles.use_denoising = True
    scene.render.resolution_x = 500
    scene.render.resolution_y = 640
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.world = bpy.data.worlds.new("Soft studio")
    scene.world.use_nodes = True
    scene.world.node_tree.nodes["Background"].inputs[0].default_value = (.62, .66, .72, 1)
    scene.world.node_tree.nodes["Background"].inputs[1].default_value = .40
    scene.view_settings.view_transform = "AgX"
    scene.view_settings.look = "AgX - Medium High Contrast"
    scene.view_settings.exposure = .4
    bpy.ops.mesh.primitive_plane_add(size=800, location=(0, 0, .007))
    floor = bpy.data.materials.new("Warm gallery floor")
    floor.use_nodes = True
    bsdf = floor.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (.72, .71, .69, 1)
    bsdf.inputs["Roughness"].default_value = .9
    bpy.context.object.data.materials.append(floor)
    key = light("Key", (-3, -4, 6), 540, 3.7, (1, .91, .82))
    fill = light("Fill", (3.8, -2.6, 3.8), 235, 4.0, (.82, .90, 1))
    light("Top softbox", (0, 2, 6), 320, 3.5, (1, .96, .91))
    camera = bpy.data.cameras.new("Orthographic review")
    camera.type = "ORTHO"
    camera.clip_end = 650
    scene.camera = bpy.data.objects.new(camera.name, camera)
    bpy.context.collection.objects.link(scene.camera)
    return key, fill


def review():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    glb = WORK / "tsuki.glb"
    bpy.ops.import_scene.gltf(filepath=str(glb), disable_bone_shape=True)
    scene = bpy.context.scene
    scene.render.fps = 24
    rig, = (ob for ob in scene.objects if ob.type == "ARMATURE")
    names = [bone.name for bone in rig.data.bones]
    assert len(names) == 18
    for parent, child in zip(NECK, NECK[1:]):
        assert rig.data.bones[child].parent.name == parent
    for side in ("L", "R"):
        for joint, parent in (("Wing", "Body"), ("LidUpper", "Head"), ("LidLower", "Head"),
                              ("Leg", "Body"), ("Ankle", f"Leg.{side}"), ("Toes", f"Ankle.{side}")):
            assert rig.data.bones[f"{joint}.{side}"].parent.name == parent
    assert rig.data.bones["Tail"].parent.name == "Body"
    skins = [ob for ob in scene.objects if ob.type == "MESH"]
    assert all(any(m.type == "ARMATURE" and m.object == rig for m in ob.modifiers) for ob in skins)
    assert glb.stat().st_size <= 10_000_000
    statistics = {
        "bytes": glb.stat().st_size,
        "joint_count": len(names),
        "joint_names": names,
        "triangles": sum(len(face.vertices)-2 for ob in skins for face in ob.data.polygons),
        **assert_pose(rig, scene),
    }
    (WORK / "verification.json").write_text(json.dumps(statistics, ensure_ascii=False, indent=2) + "\n")
    print("GLB verification:", json.dumps(statistics, ensure_ascii=False), flush=True)
    if "--check-only" in sys.argv:
        return

    key, fill = studio(scene)
    views = [
        ("front", 1, (0, -8, 1.87), (0, 0, 1.51), 3.58),
        ("side", 1, (-8, .25, 1.87), (0, .25, 1.51), 3.58),
        ("back", 1, (0, 8, 1.87), (0, 0, 1.51), 3.58),
        ("head-open", 23, (-.24, -8, 2.64), (-.24, 0, 2.49), 1.92),
        ("head-blink", 27, (-.24, -8, 2.64), (-.24, 0, 2.49), 1.92),
    ]
    for name, frame, position, target, scale in views:
        scene.frame_set(frame)
        if name == "side":
            key.location, fill.location = (-5, -3, 6), (-3, 4, 4)
        elif name == "back":
            key.location, fill.location = (3, 4, 6), (-3.8, 2.6, 3.8)
        else:
            key.location, fill.location = (-3, -4, 6), (3.8, -2.6, 3.8)
        aim(key, (0, 0, 1.44))
        aim(fill, (0, 0, 1.44))
        scene.camera.location = position
        scene.camera.data.ortho_scale = scale
        aim(scene.camera, target)
        scene.render.filepath = str(WORK / f"{name}.png")
        bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    review()
