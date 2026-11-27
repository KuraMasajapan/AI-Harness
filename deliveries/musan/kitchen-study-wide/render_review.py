"""Reimport the delivered GLBs, check floor clearance, and render review views.

This is offline evidence, not a Muse/iPhone runtime test. Requires bpy==4.5.4.
"""
import argparse
import hashlib
import json
import math
import struct
from pathlib import Path

import bpy
from mathutils import Matrix, Vector

from build_room import AVATAR_SHA256, ROOT, WORK


def glb_document(path):
    data = path.read_bytes()
    magic, version, total = struct.unpack_from("<4sII", data)
    assert (magic, version, total) == (b"glTF", 2, len(data))
    length, kind = struct.unpack_from("<I4s", data, 12)
    assert kind == b"JSON"
    doc = json.loads(data[20:20 + length])
    assert not any("uri" in item for item in doc.get("buffers", []))
    assert not any("uri" in item for item in doc.get("images", []))
    return doc


def aim(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat("-Z", "Y").to_euler()


def area(name, position, power, size, color):
    data = bpy.data.lights.new(name, "AREA")
    data.energy, data.shape, data.size, data.color = power, "DISK", size, color
    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    obj.location = position
    aim(obj, (0, 0, .5))


def review(view=None, check_only=False, refined=False):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    room_doc = glb_document(WORK / "kitchen-study.glb")
    avatar_name = "musan-butler-refined-v13.glb" if refined else "musan-butler-detail-v12.glb"
    avatar_sha = (json.loads((WORK / "avatar-verification.json").read_text())["avatar_sha256"]
                  if refined else AVATAR_SHA256)
    avatar_doc = glb_document(WORK / avatar_name)
    assert hashlib.sha256((WORK / avatar_name).read_bytes()).hexdigest() == avatar_sha
    assert not avatar_doc.get("animations")
    bpy.ops.import_scene.gltf(filepath=str(WORK / "kitchen-study.glb"), loglevel=40)
    bpy.context.view_layer.update()
    placement = json.loads((ROOT / ("scene-placement-refined.json" if refined else "scene-placement.json")).read_text())
    lane = placement["layout"]["clear_floor_bounds_xz"]
    intrusions = []
    counts = {}
    for obj in bpy.context.scene.objects:
        if obj.type != "MESH":
            continue
        zone = obj.get("layout_zone")
        assert zone, "Unclassified exported mesh: " + obj.name
        counts[zone] = counts.get(zone, 0) + 1
        if zone not in {"kitchen", "study", "bed", "tea"}:
            continue
        points = [obj.matrix_world @ Vector(p) for p in obj.bound_box]
        xs, zs = [p.x for p in points], [-p.y for p in points]
        overlaps = (min(xs) < lane["max"][0] and max(xs) > lane["min"][0]
                    and min(zs) < lane["max"][1] and max(zs) > lane["min"][1])
        if overlaps:
            intrusions.append(obj.name)
    assert not intrusions, "Furniture enters reserved floor: " + repr(intrusions)
    report = {
        "room_bytes": (WORK / "kitchen-study.glb").stat().st_size,
        "room_meshes": len(room_doc["meshes"]),
        "room_triangles": 0,
        "zone_mesh_counts": counts,
        "reserved_floor_xz": lane,
        "furniture_intrusions": intrusions,
        "avatar_sha256": avatar_sha,
        "avatar_unchanged": not refined,
        "external_asset_uris": 0,
        "runtime_test": "Not run in Muse or on iPhone",
    }
    triangles = 0
    for obj in bpy.context.scene.objects:
        if obj.type == "MESH":
            obj.data.calc_loop_triangles()
            triangles += len(obj.data.loop_triangles)
    report["room_triangles"] = triangles
    (WORK / ("verification-refined.json" if refined else "verification.json")).write_text(json.dumps(report, indent=2) + "\n")
    if check_only:
        print(json.dumps(report, indent=2))
        return

    previous = set(bpy.context.scene.objects)
    bpy.ops.import_scene.gltf(filepath=str(WORK / avatar_name), loglevel=40)
    avatar = placement["avatar"]
    x, y, z = avatar["position"]
    transform = (Matrix.Translation((x, -z, y))
                 @ Matrix.Rotation(avatar["rotation_y_radians"], 4, "Z")
                 @ Matrix.Scale(avatar["scale"], 4))
    for obj in set(bpy.context.scene.objects) - previous:
        if obj.parent is None:
            obj.matrix_world = transform @ obj.matrix_world

    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = 32
    scene.cycles.use_denoising = True
    scene.render.threads_mode = "FIXED"
    scene.render.threads = 8
    scene.world = bpy.data.worlds.new("Review studio")
    scene.world.use_nodes = True
    scene.world.node_tree.nodes["Background"].inputs[0].default_value = (.55, .49, .40, 1)
    scene.world.node_tree.nodes["Background"].inputs[1].default_value = .5
    area("Large warm key", (-3, -4, 7), 1050, 6, (1, .84, .65))
    area("Soft cool fill", (4, -1, 6), 750, 5, (.80, .88, 1))
    area("Ceiling bounce", (0, 1, 6), 500, 4, (1, .88, .72))
    groundmat = bpy.data.materials.new("Studio sand")
    groundmat.diffuse_color = (.29, .26, .22, 1)
    bpy.ops.mesh.primitive_plane_add(size=200, location=(0, 0, -.335))
    bpy.context.object.data.materials.append(groundmat)
    camera = bpy.data.cameras.new("Review camera")
    cam = bpy.data.objects.new("Review camera", camera)
    bpy.context.collection.objects.link(cam)
    scene.camera = cam
    camera.type = "ORTHO"
    scene.view_settings.view_transform = "AgX"
    scene.render.image_settings.file_format = "PNG"
    scene.render.resolution_percentage = 100
    preview = WORK / ("preview-refined" if refined else "preview")
    preview.mkdir(exist_ok=True)
    views = [
        ("wide-room", (0, -12.5, 7.8), (0, 0, .8), 10.1, (1600, 1100)),
        ("floor-clearance", (0, -.01, 13), (0, 0, 0), 9.5, (1600, 1050)),
        ("study-detail", (0, -4.8, 3.9), (-3.10, -.05, .95), 4.4, (1200, 1100)),
    ]
    for name, position, target, span, resolution in views:
        if view and name != view:
            continue
        cam.location = position
        aim(cam, target)
        camera.ortho_scale = span
        scene.render.resolution_x, scene.render.resolution_y = resolution
        scene.render.filepath = str(preview / (name + ".png"))
        bpy.ops.render.render(write_still=True)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--view", choices=["wide-room", "floor-clearance", "study-detail"])
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--refined-avatar", action="store_true", help="Use the follow-up v13 avatar, not the unchanged v12 baseline")
    # Blender itself supplies unrelated arguments when run with --python.
    args, _ = parser.parse_known_args()
    review(args.view, args.check_only, args.refined_avatar)
