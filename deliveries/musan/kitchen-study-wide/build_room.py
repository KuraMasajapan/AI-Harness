"""Build the widened prototype from the supplied kitchen GLB, not the avatar.

Run with Blender 4.5 LTS Python (bpy==4.5.4), or blender -b --python.
Blender coordinates here are Z-up; exported GLB/placement JSON are Y-up.
"""
import hashlib
import math
import random
import zipfile
from pathlib import Path

import bpy
from mathutils import Matrix, Vector

ROOT = Path(__file__).resolve().parent
WORK = ROOT / "work"
ORIGINAL = ROOT.parent / "Musan_Current_Summary_2026-11-27.zip"
ROOM_SHA256 = "642e40faafc93028afc25b8d91a2d7e8440ca090c6c8facd27845233e109b289"
AVATAR_SHA256 = "a656295b226adb614281acfc2e6f61faeba9f1b66abe28dd6b9cdbd4dd11b84d"


def material(name, color, roughness=0.6, metallic=0, emission=0):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1)
    mat.use_nodes = True
    shader = mat.node_tree.nodes.get("Principled BSDF")
    shader.inputs["Base Color"].default_value = (*color, 1)
    shader.inputs["Roughness"].default_value = roughness
    shader.inputs["Metallic"].default_value = metallic
    if emission:
        shader.inputs["Emission Color"].default_value = (*color, 1)
        shader.inputs["Emission Strength"].default_value = emission
    return mat


def finish(obj, name, mat, zone):
    obj.name = name
    obj.data.materials.append(mat)
    obj["layout_zone"] = zone
    return obj


def box(name, loc, size, mat, zone="architecture", bevel=0.015):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    obj = bpy.context.object
    obj.dimensions = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel:
        modifier = obj.modifiers.new("Soft furniture edges", "BEVEL")
        modifier.width = min(bevel, min(size) / 3)
        modifier.segments = 3
        obj.modifiers.new("Weighted normals", "WEIGHTED_NORMAL")
    return finish(obj, name, mat, zone)


def sphere(name, loc, scale, mat, zone="decoration"):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, location=loc)
    obj = bpy.context.object
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    for polygon in obj.data.polygons:
        polygon.use_smooth = True
    return finish(obj, name, mat, zone)


def cylinder(name, loc, radius, depth, mat, zone="decoration", radius_top=None):
    bpy.ops.mesh.primitive_cone_add(vertices=24, radius1=radius,
                                    radius2=radius if radius_top is None else radius_top,
                                    depth=depth, location=loc)
    return finish(bpy.context.object, name, mat, zone)


def line(name, points, radius, mat):
    curve = bpy.data.curves.new(name, "CURVE")
    curve.dimensions = "3D"
    curve.bevel_depth = radius
    curve.bevel_resolution = 2
    spline = curve.splines.new("POLY")
    spline.points.add(len(points) - 1)
    for point, co in zip(spline.points, points):
        point.co = (*co, 1)
    obj = bpy.data.objects.new(name, curve)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(mat)
    obj["layout_zone"] = "decoration"
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.convert(target="MESH")
    obj.select_set(False)
    return obj


def build():
    WORK.mkdir(exist_ok=True)
    with zipfile.ZipFile(ORIGINAL) as archive:
        for filename, expected in [("kitchen-study.glb", ROOM_SHA256),
                                   ("musan-butler-detail-v12.glb", AVATAR_SHA256)]:
            data = archive.read("models/" + filename)
            if hashlib.sha256(data).hexdigest() != expected:
                raise ValueError("Source GLB changed: " + filename)
            (WORK / filename).write_bytes(data)

    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(WORK / "kitchen-study.glb"), loglevel=40)
    originals = list(bpy.context.scene.objects)
    # Architectural planes widen, but no furniture is stretched.
    structure = {"Back wall", "Back skirting", "Right wall", "Right skirting",
                 "Solid wooden plinth"}
    for obj in originals:
        name = obj.name
        if name.startswith("Individual ash floorboard"):
            obj.location.x *= 8.4 / 4.4
            obj.scale.x *= 8.4 / 4.4
            obj.location.y *= 4.6 / 3.4
            obj.scale.y *= 4.6 / 3.4
            obj["layout_zone"] = "architecture"
        elif name in structure:
            obj["layout_zone"] = "architecture"
            if name.startswith("Back"):
                obj.location.x = 0
                obj.location.y += 0.58
                obj.scale.x *= 8.4 / 4.364
            elif name.startswith("Right"):
                obj.location.x += 2
                obj.scale.y *= 4.6 / 3.5
            else:
                obj.scale.x *= 8.5 / 4.5
                obj.scale.y *= 4.65 / 3.55
        elif (name.startswith(("Chair", "Rounded chair", "Slender chair"))):
            # Keep the left dining chair as the desk chair; remove the spare.
            corners = [obj.matrix_world @ Vector(p) for p in obj.bound_box]
            center_x = sum(p.x for p in corners) / 8
            if center_x > 1:
                bpy.data.objects.remove(obj, do_unlink=True)
            else:
                # Existing chair faces +X; turn toward the new left-wall desk.
                transform = (Matrix.Translation((-2.98, -1.15, 0))
                             @ Matrix.Rotation(math.pi, 4, "Z")
                             @ Matrix.Translation((-.38, .25, 0)))
                obj.matrix_world = transform @ obj.matrix_world
                obj["layout_zone"] = "study"
        elif (name.startswith(("Round dining", "Table apron", "Turned table"))
              or name in {"apple", "bread", "mug", "plate"}):
            # Tea table and dishes stay together, tucked into the front-right corner.
            transform = (Matrix.Translation((3.55, -1.55, .023))
                         @ Matrix.Scale(.66, 4)
                         @ Matrix.Translation((-1.1, .25, -.023)))
            obj.matrix_world = transform @ obj.matrix_world
            obj["layout_zone"] = "tea"
        else:
            obj.location += Vector((-1.65, .58, 0))
            obj["layout_zone"] = "kitchen"

    wood = material("Walnut furniture", (.23, .105, .046))
    trim = material("Honey oak trim", (.43, .235, .105))
    panel = material("Warm timber walls", (.53, .325, .175), .85)
    seam = material("Timber seams", (.36, .205, .100), .9)
    cream = material("Ivory woven linen", (.88, .80, .65), .95)
    plum = material("Plum cushion", (.19, .035, .075), .95)
    sage = material("Sage book cloth", (.18, .29, .24))
    brass = material("Desk lamp brass", (.52, .32, .105), .3, .65)
    paper = material("Warm paper", (.86, .81, .67), .9)
    terra = material("Terracotta", (.42, .17, .085))
    leaf = material("Plant leaves", (.12, .24, .10))
    glow = material("Warm lamp and bulbs", (1, .60, .22), .5, emission=2)
    wire = material("String light cable", (.045, .030, .020))
    sky = material("Round window dusk glass", (.39, .57, .65), .85, emission=.15)

    for name in ["Back wall", "Right wall"]:
        bpy.data.objects[name].data.materials.clear()
        bpy.data.objects[name].data.materials.append(panel)
    box("Left wall", (-4.2, 0, 1.13), (.12, 4.6, 2.25), panel)
    box("Left skirting", (-4.12, 0, .13), (.075, 4.6, .18), trim)
    for i in range(28):
        x = -4.05 + i * .3
        box("Back timber joint", (x, 2.233, 1.17), (.008, .009, 2.12), seam,
            bevel=0)
    for side in [-1, 1]:
        for i in range(15):
            box("Side timber joint", (side * 4.133, -2.16 + i * .3, 1.17),
                (.009, .008, 2.12), seam, bevel=0)

    # Bookcase hugs the left wall, without occupying the center.
    for y in [-.18, 1.16]:
        box("Bookcase side", (-3.88, y, .97), (.50, .065, 1.84), wood, "study")
    box("Bookcase back", (-4.10, .49, .97), (.045, 1.4, 1.84), wood, "study")
    for z in [.09, .58, 1.13, 1.84]:
        box("Bookcase shelf", (-3.88, .49, z), (.56, 1.45, .065), trim, "study")
    rng = random.Random(23)
    for row, z in enumerate([.63, 1.18]):
        for i in range(9):
            height = rng.uniform(.28, .46)
            y = -.06 + i * .125
            bookmat = [sage, cream, plum, trim][(i + row) % 4]
            box("Book spine", (-3.80, y, z + height / 2),
                (.30, .09, height), bookmat, "study", .006)
            for offset in [.045, height - .045]:
                box("Book gold band", (-3.645, y, z + offset),
                    (.008, .075, .009), brass, "study", .002)
    # Desk runs along the same wall; the reused chair faces it.
    box("Writing desk top", (-3.64, -1.12, .80), (.86, 1.65, .09), trim, "study")
    for x in [-3.95, -3.33]:
        for y in [-1.80, -.44]:
            box("Writing desk leg", (x, y, .41), (.075, .075, .74), wood, "study")
    box("Desk drawer", (-3.64, -1.12, .665), (.70, 1.37, .17), wood, "study")
    cylinder("Drawer pull", (-3.257, -1.12, .665), .025, .03, brass, "study").rotation_euler[1] = math.pi / 2
    for y in [-1.27, -.98]:
        page = box("Open notebook", (-3.57, y, .86), (.41, .275, .025), paper, "study", .007)
        page.rotation_euler[0] = -.045 if y < -1.1 else .045
    box("Writing pen", (-3.30, -1.08, .876), (.018, .30, .018), wood, "study", .004)
    cylinder("Lamp base", (-3.76, -.52, .88), .12, .04, brass, "study")
    cylinder("Lamp stem", (-3.76, -.52, 1.10), .018, .42, brass, "study")
    cylinder("Lamp shade", (-3.76, -.52, 1.35), .19, .25, cream, "study", .105)
    sphere("Lamp bulb", (-3.76, -.52, 1.26), (.055, .055, .05), glow, "study")

    # Bed has its long edge against the opposite wall.
    box("Bed frame", (3.45, .35, .31), (1.22, 2.20, .26), wood, "bed")
    for x in [2.94, 3.96]:
        for y in [-.64, 1.34]:
            box("Bed post", (x, y, .31), (.10, .10, .54), wood, "bed")
    box("Bed headboard", (3.45, 1.43, .69), (1.28, .10, 1.02), trim, "bed", .055)
    box("Bed footboard", (3.45, -.74, .42), (1.28, .075, .43), trim, "bed", .035)
    box("Soft mattress", (3.45, .32, .51), (1.16, 2.05, .25), cream, "bed", .11)
    box("Ivory duvet", (3.45, .01, .66), (1.18, 1.43, .16), cream, "bed", .07)
    box("Folded bed throw", (3.45, -.40, .765), (1.20, .42, .06), sage, "bed", .025)
    for i in range(16):
        box("Throw fringe", (2.90 + i * .073, -.64, .73), (.018, .12, .018), cream, "bed", .005)
    pillow = box("Ivory pillow", (3.45, 1.03, .76), (.88, .43, .22), cream, "bed", .10)
    pillow.rotation_euler[0] = .18
    cushion = box("Plum pillow", (3.45, .91, .90), (.43, .19, .38), plum, "bed", .075)
    cushion.rotation_euler[0] = -.25
    box("Bedside cabinet", (2.34, 1.25, .36), (.54, .59, .60), wood, "bed")
    box("Bedside top", (2.34, 1.25, .69), (.62, .65, .07), trim, "bed")
    for z in [.76, .81]:
        box("Folded towel", (2.32, 1.27, z), (.32, .34, .045), cream, "bed", .02)
    cylinder("Lavender pot", (3.76, 1.42, 1.28), .11, .17, terra, "bed", .13)
    for i in range(7):
        angle = i * 2.4
        x, y = 3.76 + math.cos(angle) * .07, 1.42 + math.sin(angle) * .07
        cylinder("Lavender stem", (x, y, 1.54), .008, .40, leaf, "bed")
        sphere("Lavender flower", (x, y, 1.74 + .03 * math.sin(i)), (.025, .025, .09), plum, "bed")

    # Round dusk window and warm string lights echo the reference, all local geometry.
    bpy.ops.mesh.primitive_torus_add(major_radius=.64, minor_radius=.055,
                                    major_segments=64, minor_segments=8,
                                    location=(1.10, 2.19, 1.45), rotation=(math.pi / 2, 0, 0))
    finish(bpy.context.object, "Round oak window frame", trim, "decoration")
    disk = cylinder("Round dusk window", (1.10, 2.225, 1.45), .635, .015, sky)
    disk.rotation_euler[0] = math.pi / 2
    points = []
    for i in range(81):
        x = -4.05 + i * 8.1 / 80
        z = 2.15 - .13 * abs(math.sin((x + 4.05) * math.pi / 2.7))
        points.append((x, 2.05, z))
    bpy.ops.object.select_all(action="DESELECT")
    line("Festoon cable", points, .009, wire)
    for i in range(14):
        x = -3.95 + i * .60
        z = 2.15 - .13 * abs(math.sin((x + 4.05) * math.pi / 2.7))
        cylinder("Bulb socket", (x, 2.05, z - .025), .023, .045, wire)
        sphere("String light bulb", (x, 2.05, z - .08), (.038, .038, .052), glow)

    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.export_scene.gltf(filepath=str(WORK / "kitchen-study.glb"),
                              export_format="GLB", use_selection=True,
                              export_apply=True, export_extras=True,
                              export_cameras=False, export_lights=False,
                              export_animations=False)
    print("Room exported. Avatar was copied byte-for-byte, never imported or edited.")


if __name__ == "__main__":
    build()
