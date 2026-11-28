"""Re-import the delivered GLB, verify the skin and animation, and render evidence."""
import hashlib
import json
import sys
import zipfile
from math import degrees
from pathlib import Path

import bpy
import numpy as np
from mathutils import Vector

HERE = Path(__file__).resolve().parent
WORK = HERE / "work"
sys.path.insert(0, str(HERE))
from build_tsuki import HEIGHT_RATIO, MUSAN_HEIGHT, NECK, TSUKI_HEIGHT, eye_frame, mesh_bounds
from feathers import HEIGHT, ring

MUSAN_MODEL = "models/musan-butler-detail-v12.glb"
MUSAN_ARCHIVE = "Musan_Current_Summary_2026-11-27.zip"
MUSAN_SHA256 = "a656295b226adb614281acfc2e6f61faeba9f1b66abe28dd6b9cdbd4dd11b84d"


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


def front_proportions(scene, rig, skins):
    # Read the exposed eye apertures from the imported mesh, not the eye sphere bounds.
    depsgraph = bpy.context.evaluated_depsgraph_get()
    eyes = []
    for sign in (-1, 1):
        hits = []
        for x in sign * np.arange(.105, .431, .005):
            for z in np.arange(2.350, 2.656, .005):
                origin = rig.matrix_world @ Vector((x, -2, z))
                hit, _, _, _, obj, _ = scene.ray_cast(depsgraph, origin, (0, 1, 0))
                if hit and obj.name.startswith(("Amber eye", "Lower lid edge", "Upper lid edge")):
                    hits.append((x, z))
        assert hits, sign
        coords = np.array(hits)
        eyes.append((coords.min(axis=0), coords.max(axis=0)))
    center = [(low + high)/2 for low, high in eyes]
    aperture_width = sum(high[0]-low[0]+.005 for low, high in eyes)/2
    head_width = float(2*ring(np.pi/2, (889-405)/220)[0])
    foot_low, foot_high = mesh_bounds(ob for ob in skins if ob.name.startswith(("Toe ", "Claw ")))
    body_low, body_high = mesh_bounds(skins)
    ratios = {
        "eye_height_percent_down_from_crown": (HEIGHT - (center[0][1] + center[1][1])/2)/(222/220),
        "eye_spacing_percent_of_head_width": (center[1][0]-center[0][0])/head_width,
        "eye_width_percent_of_head_width": aperture_width/head_width,
        "foot_span_percent_of_body_width": (foot_high[0]-foot_low[0])/(body_high[0]-body_low[0]),
    }
    reference = [116/222, 117/306, 44/306, 267/397]
    assert all(abs(value - target) < .045 for value, target in zip(ratios.values(), reference)), ratios
    return {key: {"reference": round(target*100, 1), "model": round(value*100, 1)}
            for (key, value), target in zip(ratios.items(), reference)}


def bill_proportions(scene, rig):
    depsgraph = bpy.context.evaluated_depsgraph_get()
    bill_parts = ("Upper mandible", "Lower mandible", "Gape interior", "Recessed cere", "Naris.")
    step = .004
    measurements = {}
    for view, start, end, direction, project, reference in (
        ("front", -.11, .111, (0, 1, 0), lambda u, z: (u, -2, z), (33/306, 56/222)),
        ("side", -.86, -.62, (1, 0, 0), lambda u, z: (-2, u, z), (18/295, 25/222)),
    ):
        hits = []
        for z in np.arange(2.13, 2.46, step):
            for u in np.arange(start, end, step):
                origin = rig.matrix_world @ Vector(project(u, z))
                hit, _, _, _, obj, _ = scene.ray_cast(depsgraph, origin, direction)
                if hit and obj.name.startswith(bill_parts):
                    hits.append((u, z))
        assert hits, view
        width, height = np.ptp(hits, axis=0) + step
        head_width = (float(2*ring(np.pi/2, (889-405)/220)[0]) if view == "front"
                      else float(ring(np.pi, 2.35)[1] - ring(0, 2.35)[1]))
        measurements[view] = {
            name: {"reference": round(target*100, 1), "model": round(value*100, 1)}
            for name, target, value in zip(("percent_of_head_width", "percent_of_head_height"),
                                           reference, (width/head_width, height/(222/220)))
        }
    return measurements


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


def studio(scene, units):
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
    bpy.ops.mesh.primitive_plane_add(size=800, location=(0, 0, -.001))
    floor = bpy.data.materials.new("Warm gallery floor")
    floor.use_nodes = True
    bsdf = floor.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (.72, .71, .69, 1)
    bsdf.inputs["Roughness"].default_value = .9
    bpy.context.object.data.materials.append(floor)
    key = light("Key", (-3, -4, 6), 540, 3.7, (1, .91, .82))
    fill = light("Fill", (3.8, -2.6, 3.8), 185, 4.0, (.82, .90, 1))
    top = light("Top softbox", (0, 2, 6), 320, 3.5, (1, .96, .91))
    for lamp in (key, fill, top):
        lamp.location *= units
        lamp.data.size *= units
        lamp.data.energy *= units**2
    camera = bpy.data.cameras.new("Orthographic review")
    camera.type = "ORTHO"
    camera.clip_end = 650
    scene.camera = bpy.data.objects.new(camera.name, camera)
    bpy.context.collection.objects.link(scene.camera)
    return key, fill


def import_musan():
    archive = HERE.parent / "musan" / MUSAN_ARCHIVE
    if "--musan-archive" in sys.argv:
        archive = Path(sys.argv[sys.argv.index("--musan-archive") + 1]).resolve()
    with zipfile.ZipFile(archive) as bundle:
        data = bundle.read(MUSAN_MODEL)
    assert hashlib.sha256(data).hexdigest() == MUSAN_SHA256
    path = WORK / "musan.glb"
    path.write_bytes(data)
    old = set(bpy.context.scene.objects)
    bpy.ops.import_scene.gltf(filepath=str(path), disable_bone_shape=True)
    new = set(bpy.context.scene.objects) - old
    low, high = mesh_bounds(ob for ob in new if ob.type == "MESH")
    measured = float(high[2] - low[2])
    assert abs(measured - MUSAN_HEIGHT) < .00002, measured
    for obj in new:
        if obj.parent not in new:
            obj.location += Vector((-.30 - (low[0] + high[0])/2, 0, -low[2]))
    return measured


def render_scale(scene, rig, key, fill):
    scene.frame_set(12)
    measured = import_musan()
    rig.location.x += .414
    key.location = (-.58, -.95, 1.66)
    fill.location = (.83, -.80, .99)
    key.data.size, fill.data.size = .90, .90
    key.data.energy, fill.data.energy = 42, 22
    aim(key, (0, 0, .54))
    aim(fill, (0, 0, .52))
    scene.render.resolution_x, scene.render.resolution_y = 640, 590
    scene.camera.location = (-.07, -3.3, .68)
    scene.camera.data.ortho_scale = 1.41
    aim(scene.camera, (-.07, 0, .53))
    scene.render.filepath = str(WORK / "scale.png")
    bpy.ops.render.render(write_still=True)
    return measured


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
    scene.frame_set(1)
    low, high = mesh_bounds(skins)
    height = float(high[2] - low[2])
    assert abs(height - TSUKI_HEIGHT) < .00002 and abs(low[2]) < .00002, (low, high)
    statistics = {
        "bytes": glb.stat().st_size,
        "joint_count": len(names),
        "joint_names": names,
        "triangles": sum(len(face.vertices)-2 for ob in skins for face in ob.data.polygons),
        "scale": {"tsuki_height_m": round(height, 6), "musan_height_m": round(MUSAN_HEIGHT, 6),
                  "tsuki_to_musan_height_ratio": HEIGHT_RATIO},
        **assert_pose(rig, scene),
        "front_proportions": front_proportions(scene, rig, skins),
        "beak_proportions": bill_proportions(scene, rig),
    }
    print("GLB verification:", json.dumps(statistics, ensure_ascii=False), flush=True)
    if "--check-only" in sys.argv:
        return

    units = height / 3.01
    key, fill = studio(scene, units)
    views = [
        ("front", 1, (0, -8, 1.87), (0, 0, 1.51), 3.58),
        ("side", 1, (-8, .25, 1.87), (0, .25, 1.51), 3.58),
        ("back", 1, (0, 8, 1.87), (0, 0, 1.51), 3.58),
        ("head-open", 23, (-.24, -8, 2.64), (-.24, 0, 2.49), 1.92),
        ("head-blink", 27, (-.24, -8, 2.64), (-.24, 0, 2.49), 1.92),
        ("face-detail", 1, (0, -8, 2.54), (0, 0, 2.50), 1.567),
        ("beak-detail", 27, (-.24, -8, 2.50), (-.60, -.10, 2.37), .80),
    ]
    for name, frame, position, target, scale in views:
        scene.frame_set(frame)
        if name in ("face-detail", "beak-detail"):
            scene.render.resolution_x, scene.render.resolution_y = 620, 476
        if name == "side":
            key.location, fill.location = (-5, -3, 6), (-3, 4, 4)
        elif name == "back":
            key.location, fill.location = (3, 4, 6), (-3.8, 2.6, 3.8)
        else:
            key.location, fill.location = (-3, -4, 6), (3.8, -2.6, 3.8)
        key.location *= units
        fill.location *= units
        aim(key, (0, 0, 1.44 * units))
        aim(fill, (0, 0, 1.44 * units))
        scene.camera.location = Vector(position) * units
        scene.camera.data.ortho_scale = scale * units
        aim(scene.camera, Vector(target) * units)
        scene.render.filepath = str(WORK / f"{name}.png")
        bpy.ops.render.render(write_still=True)
    measured = render_scale(scene, rig, key, fill)
    statistics["scale"]["musan_height_m"] = round(measured, 6)
    assert abs(height/measured - HEIGHT_RATIO) < .00002
    print(f"Measured height: Tsuki {height:.6f} m / Musan {measured:.6f} m = {height/measured:.4%}")
    (WORK / "verification.json").write_text(json.dumps(statistics, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    review()
