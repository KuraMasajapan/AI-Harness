"""Build the skinned Tsuki GLB in Blender 4.5."""
import sys
from math import cos, pi, radians, sin
from pathlib import Path

import bpy
import numpy as np
from mathutils import Quaternion, Vector

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from feathers import BOTTOM, HEIGHT, ring, smooth

WORK = HERE / "work"
EYE_Z = 2.505
EYE_RADIUS = .126
ANIMATION = (
    (1, 0, 0, 0), (12, -22, 6, 0), (23, -43, -8, 0),
    (26, -47, -10, 1), (29, -47, -10, 1), (33, -46, -8, 0),
    (49, 37, 10, 0), (54, 38, 10, 1), (58, 36, 10, 0), (73, 0, 0, 0),
)
NECK = ("Body", "Neck_01", "Neck_02", "Neck_03", "Head")


def eye_frame(sign):
    center = Vector((sign * .268, -.514, EYE_Z))
    n = Vector((sign * .32, -.9474, 0)).normalized()
    u = Vector((-n.y, n.x, 0))
    return center, n, u, Vector((0, 0, 1))


def material(name, color, roughness, image=None):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1)
    mat.use_nodes = True
    node = mat.node_tree.nodes.get("Principled BSDF")
    node.inputs["Base Color"].default_value = (*color, 1)
    node.inputs["Roughness"].default_value = roughness
    if image:
        tex = mat.node_tree.nodes.new("ShaderNodeTexImage")
        tex.image = bpy.data.images.load(str(WORK / image), check_existing=True)
        mat.node_tree.links.new(tex.outputs["Color"], node.inputs["Base Color"])
    return mat


def skeleton():
    rig = bpy.data.objects.new("Tsuki_ROOT", bpy.data.armatures.new("Tsuki · 18 joints"))
    bpy.context.collection.objects.link(rig)
    bpy.context.view_layer.objects.active = rig
    rig.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    bones = rig.data.edit_bones

    def add(name, start, end, parent=None):
        bone = bones.new(name)
        bone.head, bone.tail = start, end
        if parent:
            bone.parent = bones[parent]

    joints = [(0, .12, .18), (0, .055, 1.84), (0, .015, 2.08), (0, -.005, 2.26),
              (0, -.042, 2.43), (0, -.055, 2.95)]
    for i, name in enumerate(NECK):
        add(name, joints[i], joints[i+1], NECK[i-1] if i else None)
    add("Tail", (0, .39, .60), (0, 1.20, .08), "Body")
    for sign, suffix in ((1, "L"), (-1, "R")):
        add(f"Wing.{suffix}", (sign*.56, .10, 1.91), (sign*.59, .58, .66), "Body")
        add(f"Leg.{suffix}", (sign*.30, -.03, .65), (sign*.327, -.034, .194), "Body")
        add(f"Ankle.{suffix}", (sign*.327, -.034, .194), (sign*.329, -.22, .115), f"Leg.{suffix}")
        add(f"Toes.{suffix}", (sign*.329, -.22, .115), (sign*.329, -.44, .065), f"Ankle.{suffix}")
        center, _, axis, _ = eye_frame(sign)
        for name in ("LidUpper", "LidLower"):
            add(f"{name}.{suffix}", center, center + .13 * axis, "Head")
    bpy.ops.object.mode_set(mode="OBJECT")
    assert len(rig.data.bones) == 18
    return rig


def mesh(name, points, faces, mat, rig, weights, uvs=None, flip=False):
    data = bpy.data.meshes.new(name)
    if flip:
        faces = [tuple(reversed(face)) for face in faces]
    data.from_pydata(points, [], faces)
    data.update()
    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(mat)
    for poly in data.polygons:
        poly.use_smooth = True
    if uvs is not None:
        layer = data.uv_layers.new()
        for poly in data.polygons:
            wrap = any(uvs[i][0] == 0 for i in poly.vertices) and any(
                uvs[i][0] > .98 for i in poly.vertices)
            for loop in poly.loop_indices:
                u, v = uvs[data.loops[loop].vertex_index]
                layer.uv[loop].vector = (1 if wrap and u == 0 else u, v)
    groups = {}
    for i, point in enumerate(points):
        item = weights(point) if callable(weights) else {weights: 1}
        for key, value in item.items():
            if value < 1e-5:
                continue
            if key not in groups:
                groups[key] = obj.vertex_groups.new(name=key)
            groups[key].add([i], value, "REPLACE")
    mod = obj.modifiers.new("Tsuki skin", "ARMATURE")
    mod.object = rig
    obj.parent = rig
    return obj


def quads(rows, steps, wrap=True):
    return [(j * steps + i, j * steps + (i+1) % steps, (j+1) * steps + (i+1) % steps,
             (j+1) * steps + i) for j in range(rows-1) for i in range(steps if wrap else steps-1)]


def caps(rows, steps):
    return [tuple(reversed(range(steps))), tuple(range((rows-1) * steps, rows * steps))]


def plumage(rig, mat):
    steps, rows = 124, 132
    theta = -pi + np.arange(steps) * 2 * pi / steps
    # Latitude spacing closes the ends of the sculpt without a pinched pole.
    z = BOTTOM + (HEIGHT - BOTTOM) * (1 - np.cos(np.linspace(0, pi, rows))) / 2
    x, y = ring(theta[None, :], z[:, None])
    points = [(x[j, i], y[j, i], z[j]) for j in range(rows) for i in range(steps)]
    uv = [(i / steps, (value - BOTTOM) / (HEIGHT - BOTTOM)) for value in z for i in range(steps)]

    def weights(point):
        x, y, z = point
        transitions = [smooth(1.68, 2.01, z), smooth(1.98, 2.19, z), smooth(2.10, 2.32, z),
                       smooth(2.22, 2.43, z)]
        neck = [a - b for a, b in zip([1]+transitions, transitions+[0])]
        wing = (.88 * smooth(.46, .79, abs(x)) * smooth(.26, .58, z) *
                (1 - smooth(1.72, 2.02, z)) * smooth(-.53, -.25, y))
        return {**{bone: float(w * (1-wing)) for bone, w in zip(NECK, neck)},
                "Wing.L" if x > 0 else "Wing.R": float(wing)}

    return mesh("Continuous plumage sculpt", points, quads(rows, steps) + caps(rows, steps),
                mat, rig, weights, uv)


def loft(name, sections, mat, rig, weights, normal=(1, 0, 0), textured=False, steps=18):
    centers = [Vector(section[:3]) for section in sections]
    points, uv = [], []
    for i, (_, _, _, width, depth) in enumerate(sections):
        direction = (centers[min(i+1, len(centers)-1)] - centers[max(0, i-1)]).normalized()
        across = Vector(normal)
        across = (across - across.dot(direction) * direction).normalized()
        other = direction.cross(across)
        points.extend(tuple(centers[i] + across * (width * cos(2*pi*k/steps))
                            + other * (depth * sin(2*pi*k/steps))) for k in range(steps))
        if textured:
            uv.extend((.5 + .48*cos(2*pi*k/steps), 1 - i/(len(sections)-1)) for k in range(steps))
    return mesh(name, points, quads(len(sections), steps) + caps(len(sections), steps), mat, rig,
                weights, uv if textured else None)


def flight_feathers(rig, mat):
    for i in range(-3, 4):
        x = i * .083
        delay = abs(i) * .027
        loft(f"Tail feather {i+4}", [
            (x*.8, .36, .66, .052, .030), (x, .64, .46, .069, .034),
            (x, .86, .27+delay*.5, .073, .030), (x*.91, 1.00, .14+delay, .067, .021),
            (x*.84, 1.10-delay, .067+delay, .043, .011),
            (x*.80, 1.13-delay, .041+delay, .008, .003),
        ], mat, rig, "Tail", textured=True)
    for sign, suffix in ((1, "L"), (-1, "R")):
        for i in range(4):
            x = sign*(.285 + i*.095)
            loft(f"Folded primary {i+1}.{suffix}", [
                (x*.98, .46, .98-i*.035, .068, .072), (x, .70, .64-i*.028, .082, .058),
                (x*.94, .88-i*.044, .39+i*.060, .081, .046),
                (x*.87, 1.11-i*.066, .245+i*.052, .055, .022),
                (x*.84, 1.19-i*.066, .209+i*.048, .011, .005),
            ], mat, rig, "Wing."+suffix, textured=True)


def feet(rig, feather, horn):
    for sign, suffix in ((1, "L"), (-1, "R")):
        x = sign * .327
        loft("Feathered shank."+suffix, [
            (x*.82, .007, .35, .157, .136), (x*.91, -.009, .253, .131, .112),
            (x, -.064, .142, .121, .097), (x, -.201, .082, .154, .069),
            (x, -.276, .066, .102, .035), (x, -.298, .063, .018, .013),
        ], feather, rig, lambda p: {f"Leg.{suffix}": smooth(.15, .31, p[2]),
                                    f"Ankle.{suffix}": 1-smooth(.15, .31, p[2])})
        for i in range(-1, 2):
            xd = x + sign * i * .154
            y = -.435 + .045 * abs(i) + .012 * i
            loft(f"Toe {i+2}.{suffix}", [
                (x + sign*i*.09, -.181, .094, .071, .064),
                (x + sign*i*.123, -.286, .092, .087, .069),
                (xd, y+.044, .072, .068, .053), (xd, y-.017, .055, .043, .038),
                (xd, y-.027, .057, .015, .016),
            ], feather, rig, f"Toes.{suffix}")
            loft(f"Claw {i+2}.{suffix}", [
                (xd, y+.004, .065, .025, .023), (xd, y-.028, .061, .022, .02),
                (xd + sign*.009, y-.055, .039, .013, .011),
                (xd + sign*.012, y-.06, .017, .002, .002),
            ], horn, rig, f"Toes.{suffix}", steps=12)


def face(rig, amber, lid, dark, horn):
    loft("Hooked beak", [
        (0, -.644, 2.382, .044, .020), (0, -.694, 2.351, .060, .033),
        (0, -.734, 2.308, .055, .043), (0, -.749, 2.261, .037, .024),
        (0, -.740, 2.212, .023, .017), (0, -.719, 2.169, .003, .003),
    ], horn, rig, "Head")

    for sign, suffix in ((1, "L"), (-1, "R")):
        p, n, u, up = eye_frame(sign)
        points, uvs = [], []
        for j in range(18):
            a = .001 + j * (pi-.002)/17
            for i in range(48):
                phi = 2*pi*i/48
                offset = sin(a) * (u*cos(phi) + up*sin(phi)*.91)
                points.append(tuple(p + EYE_RADIUS * (n*cos(a) + offset)))
                uvs.append((.5 + .5*sin(a)*cos(phi), .5 + .5*sin(a)*sin(phi)))
        mesh("Amber eye."+suffix, points, quads(18, 48) + caps(18, 48),
             amber, rig, "Head", uvs, flip=True)
        for piece, vertical, rotation in (("Upper", 1, 49), ("Lower", -1, -46)):
            bone = f"Lid{piece}.{suffix}"
            radius = .1278 if vertical == 1 else .1273

            def surface(rows, edge):
                points = []
                for j in range(rows):
                    for i in range(45):
                        horizontal = radians(-89.9 + i*179.8/44)
                        start = rotation - 14*sin(horizontal)**2
                        sweep = start + (vertical*177 - start)*j/(rows-1)
                        angle = radians(start + vertical*(-.3+j*.54) if edge else sweep)
                        shell = u*sin(horizontal) + (n*cos(angle) + up*sin(angle))*cos(horizontal)
                        points.append(tuple(p + (radius + (.00035 if edge else 0))*shell))
                return points

            mesh(f"{piece} lid.{suffix}", surface(22, False), quads(22, 45, wrap=False),
                 lid, rig, bone, flip=vertical == -1)
            mesh(f"{piece} lid edge.{suffix}", surface(3, True), quads(3, 45, wrap=False),
                 dark, rig, bone, flip=vertical == -1)


def animate(rig):
    scene = bpy.context.scene
    scene.render.fps = 24
    scene.frame_end = ANIMATION[-1][0]
    for frame, yaw, pitch, blink in ANIMATION:
        for name, scale in zip(NECK[1:], (.14, .21, .26, .39)):
            bone = rig.pose.bones[name]
            basis = bone.bone.matrix_local.to_3x3().inverted()
            bone.rotation_mode = "QUATERNION"
            bone.rotation_quaternion = (Quaternion(basis @ Vector((0, 0, 1)), radians(yaw*scale)) @
                                        Quaternion(basis @ Vector((1, 0, 0)), radians(pitch*scale)))
            bone.keyframe_insert(data_path="rotation_quaternion", frame=frame, group=name)
        for suffix in ("L", "R"):
            for name, turn in (("LidUpper", 50), ("LidLower", -47)):
                bone = rig.pose.bones[f"{name}.{suffix}"]
                bone.rotation_mode = "QUATERNION"
                bone.rotation_quaternion = Quaternion((0, 1, 0), radians(turn*blink))
                bone.keyframe_insert(data_path="rotation_quaternion", frame=frame, group=bone.name)
    rig.animation_data.action.name = "Tsuki • head turn, tilt & blink"
    scene.frame_set(1)


def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    rig = skeleton()
    plumage(rig, material("Reference plumage", (.85, .82, .75), .84, "plumage.jpg"))
    flight_feathers(rig, material("Flight feather markings", (.85, .82, .75), .87, "tail.jpg"))
    ivory = material("Soft ivory feathers", (.82, .795, .731), .8)
    feet(rig, ivory, material("Ash horn claws", (.151, .12, .086), .55))
    face(rig, material("Amber iris", (.30, .135, .033), .19, "iris.png"),
         material("Ivory lids", (.79, .758, .697), .8),
         material("Fine umber lid edges", (.071, .055, .041), .73),
         material("Black keratin bill", (.021, .017, .015), .36))
    animate(rig)
    output = WORK / "tsuki.glb"
    bpy.ops.export_scene.gltf(filepath=str(output), export_format="GLB", export_animations=True,
                             export_yup=True, export_all_influences=False)
    print(f"Exported {output.stat().st_size:,} bytes; {len(rig.data.bones)} bones")


if __name__ == "__main__":
    build()
