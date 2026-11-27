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
from lighting import add_room_lights


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


def review(view=None, check_only=False, materials=False, quick=False, neutral_light=False):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    room_path = WORK / ("kitchen-study-materials.glb" if materials else "kitchen-study.glb")
    room_doc = glb_document(room_path)
    avatar_doc = glb_document(WORK / "musan-butler-detail-v12.glb")
    assert hashlib.sha256((WORK / "musan-butler-detail-v12.glb").read_bytes()).hexdigest() == AVATAR_SHA256
    assert not avatar_doc.get("animations")
    bpy.ops.import_scene.gltf(filepath=str(room_path), loglevel=40)
    for obj in bpy.context.scene.objects:
        if obj.type=="LIGHT":
            # Shadow flags are not part of KHR_lights_punctual. Restore our
            # exported node extras, also documented in lighting-evening.json.
            obj.data.use_shadow=bool(obj.get("runtime_cast_shadow",False))
    bpy.context.view_layer.update()
    placement = json.loads((ROOT / "scene-placement.json").read_text())
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
        "room_bytes": room_path.stat().st_size,
        "room_meshes": len(room_doc["meshes"]),
        "room_triangles": 0,
        "zone_mesh_counts": counts,
        "reserved_floor_xz": lane,
        "furniture_intrusions": intrusions,
        "avatar_sha256": AVATAR_SHA256,
        "avatar_unchanged": True,
        "external_asset_uris": 0,
        "runtime_test": "Not run in Muse or on iPhone",
    }
    triangles = 0
    for obj in bpy.context.scene.objects:
        if obj.type == "MESH":
            obj.data.calc_loop_triangles()
            triangles += len(obj.data.loop_triangles)
    report["room_triangles"] = triangles
    report_name = "verification-materials.json" if materials else "verification.json"
    (WORK / report_name).write_text(json.dumps(report, indent=2) + "\n")
    if check_only:
        print(json.dumps(report, indent=2))
        return

    previous = set(bpy.context.scene.objects)
    bpy.ops.import_scene.gltf(filepath=str(WORK / "musan-butler-detail-v12.glb"), loglevel=40)
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
    scene.cycles.samples = 16 if quick else 32
    scene.cycles.use_denoising = True
    scene.render.threads_mode = "FIXED"
    scene.render.threads = 8
    scene.world = bpy.data.worlds.new("Review studio")
    scene.world.use_nodes = True
    scene.world.node_tree.nodes["Background"].inputs[0].default_value = (.14, .08, .035, 1)
    scene.world.node_tree.nodes["Background"].inputs[1].default_value = .16
    area("Large golden key", (-3, -4, 7), 320, 5, (1, .72, .44))
    area("Low dusk fill", (4, -1, 6), 100, 4, (.65, .72, .85))
    area("Warm ceiling bounce", (0, 1, 6), 180, 4, (1, .74, .44))
    if not materials:
        add_room_lights()
    if neutral_light:
        # A same-asset lighting control, not a separate material/model change.
        for obj in list(bpy.context.scene.objects):
            if obj.type=="LIGHT":
                bpy.data.objects.remove(obj,do_unlink=True)
        scene.world.node_tree.nodes["Background"].inputs[0].default_value=(.55,.49,.40,1)
        scene.world.node_tree.nodes["Background"].inputs[1].default_value=.25
        area("Neutral warm key",(-3,-4,7),800,5,(1,.84,.65))
        area("Neutral cool fill",(4,-1,6),220,4,(.80,.88,1))
        area("Neutral ceiling bounce",(0,1,6),300,4,(1,.88,.72))
    groundmat = bpy.data.materials.new("Studio sand")
    groundmat.diffuse_color = (.10, .060, .033, 1)
    bpy.ops.mesh.primitive_plane_add(size=200, location=(0, 0, -.335))
    bpy.context.object.data.materials.append(groundmat)
    camera = bpy.data.cameras.new("Review camera")
    cam = bpy.data.objects.new("Review camera", camera)
    bpy.context.collection.objects.link(cam)
    scene.camera = cam
    camera.type = "ORTHO"
    scene.view_settings.view_transform = "AgX"
    scene.view_settings.exposure = .45
    if neutral_light:
        scene.view_settings.exposure=0
        groundmat.diffuse_color=(.29,.26,.22,1)
    scene.render.image_settings.file_format = "PNG"
    scene.render.resolution_percentage = 60 if quick else 100
    preview = WORK / ("draft" if quick else "preview-neutral" if neutral_light
                      else "preview-materials" if materials else "preview")
    preview.mkdir(exist_ok=True)
    views = [
        ("wide-room", (0, -12.5, 7.8), (0, 0, .8), 10.1, (1600, 1100)),
        ("floor-clearance", (0, -.01, 13), (0, 0, 0), 9.5, (1600, 1050)),
        ("study-detail", (0, -4.8, 3.9), (-3.10, -.05, .95), 4.4, (1200, 1100)),
        ("wood-detail", (-1.6, -2.8, 2.6), (-3.5, -.95, .75), 1.9, (1400, 1100)),
        ("fabric-detail", (1.6, -1.9, 2.5), (3.45, .53, .68), 2.25, (1400, 1100)),
        ("kitchen-detail", (-1, -.7, 2.7), (-1.9, 1.6, .9), 2.9, (1400, 1100)),
        ("interior", (0, -10.5, 3.7), (0, .15, .95), 8.8, (1800, 1100)),
        ("evening-interior", (0, -6.5, 2.3), (0, .6, 1.05), 8.8, (1800, 900)),
    ]
    for name, position, target, span, resolution in views:
        if view and name != view:
            continue
        cam.location = position
        aim(cam, target)
        camera.ortho_scale = span
        camera.type = "PERSP" if name in {"interior","evening-interior"} else "ORTHO"
        camera.lens = 24 if name == "evening-interior" else 30
        camera.shift_y = -.06 if name == "evening-interior" else 0
        scene.render.resolution_x, scene.render.resolution_y = resolution
        scene.render.filepath = str(preview / (name + ".png"))
        bpy.ops.render.render(write_still=True)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--view", choices=["wide-room", "floor-clearance", "study-detail",
                                          "wood-detail", "fabric-detail", "kitchen-detail", "interior", "evening-interior"])
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--materials", action="store_true")
    parser.add_argument("--quick", action="store_true")
    parser.add_argument("--neutral-lighting", action="store_true")
    # Blender itself supplies unrelated arguments when run with --python.
    args, _ = parser.parse_known_args()
    review(args.view, args.check_only, args.materials, args.quick, args.neutral_lighting)
