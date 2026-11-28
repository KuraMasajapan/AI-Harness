"""Build the skinned Tsuki GLB in Blender 4.5."""
import sys
from math import cos, pi, radians, sin
from pathlib import Path

import bpy
import numpy as np
from mathutils import Quaternion, Vector

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from feathers import BOTTOM, EYE_X, EYE_Z, HEIGHT, ring, smooth

WORK = HERE / "work"
EYE_RADIUS = .115
LIDS = (("Upper", 59, 14, 75), ("Lower", -58, 7, -62))
MUSAN_HEIGHT = 1.00521434
HEIGHT_RATIO = .48
TSUKI_HEIGHT = MUSAN_HEIGHT * HEIGHT_RATIO
ANIMATION = (
    (1, 0, 0, 0), (12, -22, 6, 0), (23, -43, -8, 0),
    (26, -47, -10, 1), (29, -47, -10, 1), (33, -46, -8, 0),
    (49, 37, 10, 0), (54, 38, 10, 1), (58, 36, 10, 0), (73, 0, 0, 0),
)
NECK = ("Body", "Neck_01", "Neck_02", "Neck_03", "Head")


def eye_frame(sign):
    center = Vector((sign * EYE_X, -.436, EYE_Z))
    n = Vector((sign * .359, -.933, 0)).normalized()
    u = Vector((-n.y, n.x, 0))
    return center, n, u, Vector((0, 0, 1))


def mesh_bounds(objects):
    depsgraph = bpy.context.evaluated_depsgraph_get()
    points = []
    for obj in objects:
        evaluated = obj.evaluated_get(depsgraph)
        points.extend(tuple(evaluated.matrix_world @ v.co) for v in evaluated.data.vertices)
    coords = np.asarray(points)
    return coords.min(axis=0), coords.max(axis=0)


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
    near_face = (abs(theta) < .65) & (abs(theta) > .12)
    theta = np.sort(np.concatenate((theta, theta[near_face] + pi/steps)))
    # Latitude spacing closes the ends of the sculpt without a pinched pole.
    z = BOTTOM + (HEIGHT - BOTTOM) * (1 - np.cos(np.linspace(0, pi, rows))) / 2
    near_eyes = abs(z[:-1] - EYE_Z) < .145
    z = np.sort(np.concatenate((z, ((z[:-1] + z[1:])/2)[near_eyes])))
    steps, rows = len(theta), len(z)
    x, y = ring(theta[None, :], z[:, None])
    points = [(x[j, i], y[j, i], z[j]) for j in range(rows) for i in range(steps)]
    uv = [((angle + pi)/(2*pi), (value - BOTTOM)/(HEIGHT - BOTTOM)) for value in z for angle in theta]

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


def loft(name, sections, mat, rig, weights, normal=(1, 0, 0), textured=False, steps=18,
         feathered=False):
    centers = [Vector(section[:3]) for section in sections]
    points, uv = [], []
    for i, (_, _, _, width, depth) in enumerate(sections):
        direction = (centers[min(i+1, len(centers)-1)] - centers[max(0, i-1)]).normalized()
        across = Vector(normal)
        across = (across - across.dot(direction) * direction).normalized()
        other = direction.cross(across)
        for k in range(steps):
            angle = 2*pi*k/steps
            puff = 1 + .075 * (sin(6*angle+i*.51) + .33*sin(11*angle-i*.72)) if feathered else 1
            points.append(tuple(centers[i] + puff * (across * (width * cos(angle))
                                + other * (depth * sin(angle)))))
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
        x = sign * .339
        loft("Feathered shank."+suffix, [
            (x*.82, .012, .37, .166, .139), (x*.91, -.012, .270, .154, .120),
            (x, -.082, .168, .154, .126), (x, -.219, .097, .174, .092),
            (x, -.290, .077, .122, .055), (x, -.332, .072, .022, .016),
        ], feather, rig, lambda p: {f"Leg.{suffix}": smooth(.15, .31, p[2]),
                                    f"Ankle.{suffix}": 1-smooth(.15, .31, p[2])},
             textured=True, feathered=True, steps=32)
        for i in range(-1, 2):
            xd = x + sign * i * .178
            y = -.473 + .049 * abs(i) + .015 * i
            loft(f"Toe {i+2}.{suffix}", [
                (x + sign*i*.095, -.177, .124, .088, .081),
                (x + sign*i*.135, -.265, .119, .100, .092),
                (xd, y+.071, .103, .089, .079), (xd, y+.032, .085, .083, .060),
                (xd, y-.008, .065, .060, .046),
                (xd, y-.035, .046, .035, .026), (xd, y-.048, .042, .010, .012),
            ], feather, rig, f"Toes.{suffix}", textured=True, feathered=True, steps=32)
            loft(f"Claw {i+2}.{suffix}", [
                (xd, y-.013, .063, .023, .021), (xd, y-.041, .058, .023, .020),
                (xd + sign*.006, y-.058, .039, .015, .012),
                (xd + sign*.009, y-.066, .013, .002, .002),
            ], horn, rig, f"Toes.{suffix}", steps=12)


def hooked_bill(rig, horn, lower, gape):
    # (Half-width, side seam y/z, dorsal y/z, ventral depth), from root to hook.
    sections = (
        (.048, -.672, 2.338, -.699, 2.434, .009),
        (.067, -.720, 2.324, -.731, 2.413, .007),
        (.058, -.735, 2.309, -.745, 2.389, .006),
        (.057, -.742, 2.287, -.759, 2.350, .005),
        (.042, -.746, 2.271, -.760, 2.316, .005),
        (.032, -.756, 2.250, -.782, 2.283, .004),
        (.021, -.755, 2.230, -.786, 2.255, .003),
        (.012, -.748, 2.211, -.772, 2.230, .003),
        (.005, -.738, 2.193, -.752, 2.204, .002),
        (.0008, -.727, 2.179, -.730, 2.183, .0007),
    )
    steps = 48
    points, uvs = [], []
    for j, (width, y, z, top_y, top_z, depth) in enumerate(sections):
        for k in range(steps):
            theta = 2*pi*k/steps
            arc = sin(theta)
            across = cos(theta)
            top = (.54*arc + .46*(1 - ((across*across + .0025)**.5 - .05)/.95125)
                   if arc > 0 else 0)
            points.append((width*across, y + (top_y-y)*top,
                           z + (top_z-z)*top + depth*min(0, arc)))
            uvs.append((k/steps, 1 - j/(len(sections)-1)))
    mesh("Upper mandible", points, quads(len(sections), steps) + caps(len(sections), steps),
         horn, rig, "Head", uvs)
    loft("Lower mandible", [
        (0, -.663, 2.277, .032, .018), (0, -.706, 2.264, .026, .012),
        (0, -.724, 2.251, .014, .006), (0, -.735, 2.238, .006, .004),
        (0, -.739, 2.231, .002, .002),
    ], lower, rig, "Head", steps=36)
    loft("Gape interior", [
        (0, -.683, 2.292, .034, .013), (0, -.720, 2.275, .024, .010),
        (0, -.733, 2.256, .011, .006), (0, -.741, 2.240, .004, .003),
    ], gape, rig, "Head", steps=24)
    loft("Recessed cere", [
        (0, -.659, 2.419, .032, .014), (0, -.700, 2.412, .032, .012),
        (0, -.719, 2.393, .025, .010), (0, -.733, 2.377, .011, .006),
    ], lower, rig, "Head", steps=28)
    for sign, side in ((1, "L"), (-1, "R")):
        loft(f"Naris.{side}", [
            (sign*.023, -.712, 2.406, .001, .001),
            (sign*.028, -.720, 2.399, .004, .002),
            (sign*.031, -.725, 2.392, .002, .001),
        ], gape, rig, "Head", normal=(0, 0, 1), steps=12)


def facial_bristles(rig, tones):
    angles = np.linspace(-.45, .45, 125)
    for sign, side in ((1, "L"), (-1, "R")):
        for row in range(3):
            for i in range(13):
                x = sign*(.019 + .007*i + .012*row)
                z = 2.418 + .62*abs(x) - .042*row + .006*sin(i*2.7 + row + sign)
                width = .0021 + .0010*(1 + cos(i*2.1 + row))
                length = .045 + .010*sin(i*1.67 + row) + .009*row
                sections = []
                for t, offset, taper in ((0, .006, .68), (.28, -.003, 1),
                                         (.61, -.010, .76), (1, -.015, .13)):
                    tx, tz = x*(1 - .47*t), z - t*length
                    xs, ys = ring(angles, tz)
                    y = float(np.interp(tx, xs, ys))
                    sections.append((tx, y+offset, tz, width*taper, width*taper*.58))
                loft(f"Facial bristle {row}-{i}.{side}", sections, tones[(i+row)%len(tones)],
                     rig, "Head", steps=8)


def face(rig, amber, lid, dark, horn, lower, gape, bristle_tones):
    hooked_bill(rig, horn, lower, gape)
    facial_bristles(rig, bristle_tones)
    for sign, suffix in ((1, "L"), (-1, "R")):
        p, n, u, up = eye_frame(sign)
        points, uvs = [], []
        for j in range(18):
            a = .001 + j * (pi-.002)/17
            for i in range(48):
                phi = 2*pi*i/48
                offset = sin(a) * (u*cos(phi) + up*sin(phi))
                inset = .011 * (1 - smooth(.18, .66, sin(a))) if a < pi/2 else 0
                points.append(tuple(p + n * (EYE_RADIUS*cos(a) - inset) + EYE_RADIUS*offset))
                uvs.append((.5 + .5*sin(a)*cos(phi), .5 + .5*sin(a)*sin(phi)))
        mesh("Amber eye."+suffix, points, quads(18, 48) + caps(18, 48),
             amber, rig, "Head", uvs, flip=True)
        for piece, rotation, corner, _ in LIDS:
            vertical = 1 if piece == "Upper" else -1
            bone = f"Lid{piece}.{suffix}"
            radius = EYE_RADIUS + (.0022 if vertical == 1 else .0017)

            def surface(rows, edge):
                points = []
                for j in range(rows):
                    for i in range(45):
                        horizontal = radians(-89.9 + i*179.8/44)
                        start = rotation + corner*sin(horizontal)**2
                        sweep = start + (vertical*177 - start)*j/(rows-1)
                        angle = radians(start - .25 + j*3.1/(rows-1) if edge else sweep)
                        shell = u*sin(horizontal) + (n*cos(angle) + up*sin(angle))*cos(horizontal)
                        points.append(tuple(p + (radius + (.00035 if edge else 0))*shell))
                return points

            mesh(f"{piece} lid.{suffix}", surface(22, False), quads(22, 45, wrap=False),
                 lid, rig, bone, flip=vertical == -1)
            if vertical == 1:
                mesh(f"{piece} lid edge.{suffix}", surface(3, True), quads(3, 45, wrap=False),
                     dark, rig, bone)


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
            for piece, _, _, turn in LIDS:
                bone = rig.pose.bones[f"Lid{piece}.{suffix}"]
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
    ivory = material("Soft ivory feathers", (.82, .795, .731), .9, "toe-feather.jpg")
    feet(rig, ivory, material("Charcoal horn claws", (.052, .036, .026), .48))
    amber = material("Amber iris, diffuse body and corneal sheen", (.30, .135, .033), .37, "iris.png")
    eye_shader = amber.node_tree.nodes.get("Principled BSDF")
    eye_shader.inputs["IOR"].default_value = 1.376
    eye_shader.inputs["Specular IOR Level"].default_value = .13
    eye_shader.inputs["Coat Weight"].default_value = .11
    eye_shader.inputs["Coat Roughness"].default_value = .43
    face(rig, amber,
         material("Ivory lids", (.79, .758, .697), .8),
         material("Dark eyelid rims", (.011, .008, .007), .63),
         material("Slate keratin bill", (.055, .067, .084), .46, "bill-keratin.jpg"),
         material("Lower bill and cere", (.039, .049, .063), .51),
         material("Gape and naris", (.003, .002, .002), .73),
         (material("Pale bristle feather", (.78, .765, .723), .86),
          material("Soft bristle feather", (.63, .615, .575), .89),
          material("Ivory bristle feather", (.73, .71, .663), .86)))
    animate(rig)
    low, high = mesh_bounds(ob for ob in rig.children if ob.type == "MESH")
    scale = TSUKI_HEIGHT / (high[2] - low[2])
    rig.scale = (scale,) * 3
    rig.location.z = -low[2] * scale
    output = WORK / "tsuki.glb"
    bpy.ops.export_scene.gltf(filepath=str(output), export_format="GLB", export_animations=True,
                             export_yup=True, export_all_influences=False)
    print(f"Exported {output.stat().st_size:,} bytes; {len(rig.data.bones)} bones")


if __name__ == "__main__":
    build()
