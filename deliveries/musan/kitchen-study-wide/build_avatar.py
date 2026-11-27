"""Refine the supplied v12 avatar against the owner's four reference sheets.

Local procedural work only; the reference images are not uploaded or baked in.
Blender coordinates: Z up, face toward -Y. Exported GLB: glTF Y up.
"""
import hashlib
import json
import math
import random
import zipfile

import bpy
import bmesh
import numpy as np
from mathutils import Vector

from build_room import ROOT, WORK, ORIGINAL, AVATAR_SHA256

NAME = "musan-butler-refined-v13.glb"


def surface(name, vertices, faces, mat):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    mesh.materials.append(mat)
    for p in mesh.polygons:
        p.use_smooth = True
    return obj


def oval(name, position, scale, mat, power=1):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=40, ring_count=20, location=position)
    obj = bpy.context.object
    obj.name = name
    if power != 1:
        for v in obj.data.vertices:
            v.co = [math.copysign(abs(c)**power, c) for c in v.co]
    obj.scale = scale
    obj.data.materials.append(mat)
    for p in obj.data.polygons:
        p.use_smooth = True
    return obj


def cord(name, points, radius, mat):
    curve = bpy.data.curves.new(name, "CURVE")
    curve.dimensions, curve.resolution_u = "3D", 8
    curve.bevel_depth, curve.bevel_resolution = radius, 2
    spline = curve.splines.new("BEZIER")
    spline.bezier_points.add(len(points)-1)
    for point, co in zip(spline.bezier_points, points):
        point.co = co
        point.handle_left_type = point.handle_right_type = "AUTO"
    obj = bpy.data.objects.new(name, curve)
    bpy.context.collection.objects.link(obj)
    curve.materials.append(mat)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.convert(target="MESH")
    obj.select_set(False)
    return obj


def smoothstep(a, b, x):
    t = min(1, max(0, (x-a)/(b-a)))
    return t*t*(3-2*t)


def reshape(p):
    """Narrow shoulders/belly, reduce depth, square the dome, raise service arm.

    Shared deformation is applied in world space to *all* retained parts so
    garments and original face features continue to follow the body.
    """
    x, y, z = p
    head = smoothstep(.55, .66, z)
    nx = .276 * math.copysign((abs(x)/.276)**.85, x)
    x = x*.79*(1-head) + nx*head
    y *= .76 + .03*head
    if z > .80:
        z = .80 + .20*((z-.80)/.20)**.77
    # Bend the service-side forearm forward/up instead of hanging the towel
    # from a straight wrist. Keep the shoulder and torso transition smooth.
    arm = smoothstep(.215, .275, -x) * (1-smoothstep(.52, .60, z))
    rise = max(0, .60-z)
    y -= .37*rise*arm
    z += .48*rise*arm
    x += .090*min(1, rise/.35)*arm
    return Vector((x, y, z))


def contact(obj, x, z, back=False):
    origin = Vector((x, 2 if back else -2, z))
    direction = Vector((0, -1 if back else 1, 0))
    hit, p, _, _ = obj.ray_cast(obj.matrix_world.inverted() @ origin,
                               obj.matrix_world.inverted().to_3x3() @ direction)
    assert hit, (obj.name, x, z)
    return (obj.matrix_world @ p).y


def join_group(name, objects, semantic):
    bpy.ops.object.select_all(action="DESELECT")
    for obj in objects:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = objects[0]
    bpy.ops.object.join()
    obj = bpy.context.object
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    obj.name = name
    obj["part"] = semantic
    obj["construction"] = "One mesh; layered material islands, not a watertight cloth simulation mesh"
    obj.select_set(False)
    return obj


def add_fur(body):
    """A deterministic, bounded number of short tapered fibre triangles."""
    rng = random.Random(13)
    body.data.calc_loop_triangles()
    tris, weights = [], []
    for tri in body.data.loop_triangles:
        if tri.material_index == 0:
            continue
        p = [body.matrix_world @ body.data.vertices[i].co for i in tri.vertices]
        c = sum(p, Vector())/3
        if .28 < c.z < .59 and abs(c.x) < .26 and c.y > -.15:
            continue  # hidden beneath the suit
        tris.append(p)
        weights.append((p[1]-p[0]).cross(p[2]-p[0]).length/2)
    vertices, faces = [], []
    for a, b, c in rng.choices(tris, weights=weights, k=24000):
        u, v = rng.random(), rng.random()
        if u+v > 1:
            u, v = 1-u, 1-v
        p = a+(b-a)*u+(c-a)*v
        n = (b-a).cross(c-a).normalized()
        tangent = n.cross(Vector((0, 0, 1)))
        if tangent.length < .01:
            tangent = n.cross(Vector((0, 1, 0)))
        tangent.normalize()
        length = rng.uniform(.005, .010)
        width = rng.uniform(.00025, .00055)
        tip = p+n*length+Vector((0, 0, -.002))
        k = len(vertices)
        vertices.extend((p-tangent*width, p+tangent*width, tip))
        faces.append((k, k+1, k+2))
    fur = bpy.data.materials["Matte cream fibre"]
    fur.node_tree.nodes.get("Principled BSDF").inputs["Base Color"].default_value = (.86, .68, .44, 1)
    fur.use_backface_culling = False
    return surface("Short warm plush pile", vertices, faces, fur)


def build():
    WORK.mkdir(exist_ok=True)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    with zipfile.ZipFile(ORIGINAL) as archive:
        original = archive.read("models/musan-butler-detail-v12.glb")
    assert hashlib.sha256(original).hexdigest() == AVATAR_SHA256
    source = WORK / "musan-butler-detail-v12.glb"
    source.write_bytes(original)
    bpy.ops.import_scene.gltf(filepath=str(source), loglevel=40)
    body = next(o for o in bpy.context.scene.objects if o.name.startswith("tripo_node"))
    remove = ("Short plush", "Inset silver", "Integral silver", "Silver microphone",
              "Black ear unit", "Pinched satin", "Wrapped satin", "White towel",
              "Towel double", "Towel hem", "Black tailcoat body", "Flat tailored back collar",
              "Tailored sleeve -1", "Sleeve hem -1", "Ivory cuff -1", "Tailcoat back center seam",
              "Left satin notched lapel", "Right satin notched lapel")
    for obj in list(bpy.context.scene.objects):
        if obj.name.startswith(remove):
            bpy.data.objects.remove(obj, do_unlink=True)
            continue
        if obj == body:
            # Remove the old hanging service hand rather than stretching it
            # into a folded pose. Its cut edge is concealed by the new sleeve.
            mesh = bmesh.new()
            mesh.from_mesh(obj.data)
            faces = [f for f in mesh.faces if all(v.co.x < -.285 and v.co.z < .55 for v in f.verts)]
            bmesh.ops.delete(mesh, geom=faces, context="FACES")
            mesh.to_mesh(obj.data)
            mesh.free()
        inverse = obj.matrix_world.inverted()
        for vertex in obj.data.vertices:
            vertex.co = inverse @ reshape(obj.matrix_world @ vertex.co)
        if obj.name.startswith("Flat tailored back collar"):
            for vertex in obj.data.vertices:
                vertex.co.z -= .024*(1-min(1, abs(vertex.co.x)/.25))
    body.name = "Musan plush body and original face"
    body["part"] = "body"
    # Keep eye spacing/identity but replace the old irregular tessellation.
    eye_mat = bpy.data.materials["Glossy black round eyes"]
    for obj in list(bpy.context.scene.objects):
        if obj.name.startswith("Black button eye"):
            centre = reshape(obj.matrix_world.translation)
            name = obj.name
            bpy.data.objects.remove(obj, do_unlink=True)
            oval(name, centre, (.0175,.0065,.021), eye_mat)
        elif obj.name.startswith("Small smile"):
            for vertex in obj.data.vertices:
                vertex.co.x *= .86
                vertex.co.z = .722 + (vertex.co.z-.722)*1.65
    # Preserve original material boundary/identity, add soft reference blush
    # in vertex colours rather than floating cheek disks.
    colour = body.data.color_attributes.active_color
    skin_indices = {i for p in body.data.polygons if p.material_index == 0 for i in p.vertices}
    for index in skin_indices:
        p = body.matrix_world @ body.data.vertices[index].co
        blush = math.exp(-((abs(p.x)-.126)/.045)**2-((p.z-.731)/.039)**2)*.38
        base = Vector((.85, .64, .39)).lerp(Vector((.90, .25, .21)), blush)
        if colour.domain == "POINT":
            colour.data[index].color = (*base, 1)
    if colour.domain == "CORNER":
        for loop in body.data.loops:
            if loop.vertex_index in skin_indices:
                p = body.matrix_world @ body.data.vertices[loop.vertex_index].co
                blush = math.exp(-((abs(p.x)-.126)/.045)**2-((p.z-.731)/.039)**2)*.38
                colour.data[loop.index].color = (*Vector((.85,.64,.39)).lerp(Vector((.90,.25,.21)),blush),1)
    plush = bpy.data.materials["Cream plush with brushed pile"]
    mix = next(n for n in plush.node_tree.nodes if n.type == "MIX")
    # Original uses a colour Mix node; tint only its uniform colour input.
    for socket in mix.inputs:
        if socket.name == "B" and socket.type == "RGBA":
            socket.default_value = (.76, .57, .34, 1)
    handmat = plush.copy()
    handmat.name = "Warm plush service hand"
    bsdf = handmat.node_tree.nodes.get("Principled BSDF")
    for link in list(handmat.node_tree.links):
        if link.to_node == bsdf and link.to_socket.name == "Base Color":
            handmat.node_tree.links.remove(link)
    bsdf.inputs["Base Color"].default_value = (.76,.57,.34,1)
    hand = oval("Raised service mitten",(-.215,-.207,.428),(.059,.052,.061),handmat)
    body = join_group("Musan plush body and original face",[body,hand],"body")
    add_fur(body)["part"] = "fur"
    # Reduce the dense base a little, preserving the material boundary.
    bpy.context.view_layer.objects.active = body
    decimate = body.modifiers.new("Lightweight base, preserve face boundary", "DECIMATE")
    decimate.ratio = .78
    decimate.delimit = {"MATERIAL"}
    bpy.ops.object.modifier_apply(modifier=decimate.name)

    silver = bpy.data.materials["Pearl silver headset"]
    metal = silver.node_tree.nodes.get("Principled BSDF")
    metal.inputs["Metallic"].default_value = .72
    metal.inputs["Roughness"].default_value = .24
    charcoal = bpy.data.materials["Headset charcoal cushion"]
    satin = bpy.data.materials["Black satin lapels and bow"]
    white = bpy.data.materials["Ivory cotton"]
    gold = bpy.data.materials["Brushed warm gold buttons"]
    coat = bpy.data.materials["Midnight black wool"]
    vest = bpy.data.materials["Charcoal waistcoat"]
    seam = bpy.data.materials["Black tailoring seams"]
    # A continuously curved cutaway shell replaces the cropped v12 jacket.
    vertices,faces = [],[]
    segments = 96
    levels = [(.61,.241,.205),(.56,.252,.220),(.50,.263,.235),
              (.43,.271,.247),(.35,.272,.253),(None,.270,.246)]
    for row,(z,rx,ry) in enumerate(levels):
        opening = .31+.27*row/(len(levels)-1)
        for i in range(segments+1):
            theta = opening+(2*math.pi-2*opening)*i/segments
            angle = min(theta,2*math.pi-theta)
            hem = float(np.interp(angle,[.58,1.03,1.57,2.1,math.pi],[.31,.13,.18,.23,.29]))
            vertices.append((rx*math.sin(theta),-ry*math.cos(theta),z if z is not None else hem))
    for row in range(len(levels)-1):
        for i in range(segments):
            a = row*(segments+1)+i
            faces.append((a,a+1,a+segments+2,a+segments+1))
    shell = surface("Continuous tailored cutaway coat",vertices,[f[::-1] for f in faces],coat)
    shell.modifiers.new("Soft continuous coat curvature","SUBSURF").levels = 2
    shell.modifiers.new("Tailcoat fabric thickness","SOLIDIFY").thickness = .003
    # Collar band, with a lower centre-back arc and no pointed floating ends.
    vertices,faces = [],[]
    for row in range(4):
        t = row/3
        for i in range(65):
            theta = .62+(2*math.pi-1.24)*i/64
            lower = .576-.014*max(0,-math.cos(theta))
            vertices.append(((.242+.017*t)*math.sin(theta),-(.208+.014*t)*math.cos(theta),.613*(1-t)+lower*t))
    for r in range(3):
        for i in range(64):
            a = r*65+i
            faces.append((a,a+1,a+66,a+65))
    collar = surface("Curved shawl back collar",vertices,[f[::-1] for f in faces],coat)
    collar.modifiers.new("Collar cloth thickness","SOLIDIFY").thickness = .003
    # Curved sleeve around the bent service arm; cuff and mitten stay outside
    # the torso rather than exposing the old arm attachment through a slit.
    centres = [(-.225,.015,.555),(-.267,-.007,.507),(-.285,-.045,.460),
               (-.272,-.095,.447),(-.245,-.146,.444),(-.233,-.170,.439)]
    radii = [(.082,.104),(.085,.101),(.083,.091),(.076,.080),(.068,.069),(.063,.064)]
    vertices,faces = [],[]
    count = 32
    for r,(co,(rx,rz)) in enumerate(zip(centres,radii)):
        p = Vector(co)
        tangent = Vector(centres[min(r+1,len(centres)-1)])-Vector(centres[max(0,r-1)])
        tangent.normalize()
        side = Vector((1,0,0))
        up = tangent.cross(side).normalized()
        side = up.cross(tangent).normalized()
        for i in range(count):
            a = i*2*math.pi/count
            vertices.append(p+side*rx*math.cos(a)+up*rz*math.sin(a))
    for r in range(len(centres)-1):
        for i in range(count):
            faces.append((r*count+i,r*count+(i+1)%count,(r+1)*count+(i+1)%count,(r+1)*count+i))
    faces.append(tuple(reversed(range(count))))
    sleeve = surface("Bent service sleeve",vertices,faces,coat)
    sleeve.modifiers.new("Smooth bent sleeve","SUBSURF").levels = 2
    cuffverts = vertices[-count:]+[Vector(p)+tangent*.018 for p in vertices[-count:]]
    cuff = surface("White service cuff",cuffverts,[(i,(i+1)%count,count+(i+1)%count,count+i) for i in range(count)],white)
    cuff.modifiers.new("Cuff thickness","SOLIDIFY").thickness = .002
    # Rounded capsule nestled into one side; no exposed headband or mount.
    hit, point, _, _ = body.ray_cast(Vector((0, -.084, .80)), Vector((1, 0, 0)))
    assert hit
    hx = point.x
    headset = []
    ear = oval("Sculpted single-ear silver capsule", (hx+.004,-.084,.80), (.012,.065,.026), silver, .75)
    ear.rotation_euler.x = .60
    headset.append(ear)
    headset.append(oval("Single inset headset port", (hx+.017,-.075,.809), (.0015,.0031,.0031), charcoal))
    headset.append(cord("Integral curved silver microphone", [(hx,-.133,.761),
                          (hx-.016,-.165,.739),(.174,-.191,.719),(.141,-.205,.711)], .0024,silver))
    tip = oval("Integrated microphone end",(.138,-.207,.711),(.009,.0037,.0037),silver)
    tip.rotation_euler.z = .33
    headset.append(tip)
    join_group("Single-ear headset", headset, "headset")

    # More substantial, curved pinched wings and a wrapped centre knot.
    bow_y = -.238
    for side in (-1, 1):
        vertices, faces = [], []
        rows, segments = 20, 32
        for row in range(rows+1):
            t = row/rows
            h = .009+.026*math.sin(t*math.pi/2)
            for i in range(segments):
                a = i*2*math.pi/segments
                x = side*(.012+.061*t-.004*math.sin(a)**2*t**6)
                y = bow_y+(.006+.006*t)*math.cos(a)
                y += .003*math.exp(-(math.sin(a)/.24)**2)*(1-t)**2
                vertices.append((x,y,.578+h*math.sin(a)))
        for r in range(rows):
            for i in range(segments):
                faces.append((r*segments+i,r*segments+(i+1)%segments,
                              (r+1)*segments+(i+1)%segments,(r+1)*segments+i))
        faces.extend((tuple(reversed(range(segments))),tuple(rows*segments+i for i in range(segments))))
        if side < 0:
            faces = [face[::-1] for face in faces]
        surface("Sculpted satin bow wing",vertices,faces,satin)
    oval("Rounded wrapped bow knot",(0,bow_y-.004,.578),(.014,.011,.019),satin,.56)

    shirt = bpy.data.objects["White shirt front"]
    # A visible placket and fine pin-tucks following the actual shirt surface.
    bpy.context.view_layer.update()
    for x in (-.044,-.026,-.008,.008,.026,.044):
        points = [(x,contact(shirt,x,z)-.0009,z) for z in (.465,.49,.52,.55)]
        cord("Shirt fine pin-tuck",points,.00065,white)
    for obj in list(bpy.context.scene.objects):
        if obj.name.startswith("Black shirt placket button"):
            obj.location.y -= .002
    # A finer repeating floral/damask motif, embedded as a 512px texture.
    size = 512
    y,x = np.mgrid[0:size,0:size]/size*math.pi*2
    u,v = x*4,y*4
    vine = np.exp(-((np.sin(u+.45*np.sin(v)))/.17)**2)
    petals = np.maximum(0,np.cos(2*u)*np.cos(2*v))**5
    motif = np.clip(vine*.48+petals*.7,0,1)
    colours = np.array([.070,.068,.065])+motif[...,None]*.11
    img = bpy.data.images.new("Fine charcoal floral brocade",size,size,alpha=False)
    img.pixels.foreach_set(np.concatenate((colours,np.ones((size,size,1))),axis=-1).astype('f4').ravel())
    img.pack()
    tex = next(n for n in vest.node_tree.nodes if n.type == "TEX_IMAGE" and "damask" in n.image.name.lower())
    tex.image = img
    # Back strip between the gold buttons, laid on the existing coat.
    # Apply the shell once for reliable surface fitting of the back details.
    bpy.context.view_layer.objects.active = shell
    for mod in list(shell.modifiers):
        bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.context.view_layer.update()
    back = shell
    for side in (-1,1):
        contour = [(.072,.607),(.158,.600),(.205,.553),(.175,.525),
                   (.187,.507),(.083,.362),(.116,.501)]
        points = []
        for x,z in contour:
            y = -.260+.40*(z-.36)
            ok,p,_,_ = shell.ray_cast(Vector((side*x,-2,z)),Vector((0,1,0)))
            if ok and p.y < 0:
                y = min(y,p.y-.008)
            points.append((side*x,y,z))
        indices = tuple(range(len(points)))
        lapel = surface("Tailored notched satin lapel",points,[indices[::-1] if side>0 else indices],satin)
        lapel.modifiers.new("Triangulate notched outline","TRIANGULATE")
        lapel.modifiers.new("Satin lapel edge thickness","SOLIDIFY").thickness = .003
        bevel = lapel.modifiers.new("Rounded lapel edge","BEVEL")
        bevel.width,bevel.segments = .0015,2
    for obj in list(bpy.context.scene.objects):
        if obj.name.startswith(("Breast pocket welt","White pocket square")):
            for vertex in obj.data.vertices:
                p = obj.matrix_world @ vertex.co
                if obj.name.startswith(("Breast pocket","White pocket")):
                    p.x += .043
                y = contact(shell,p.x,p.z)
                if y < 0:
                    p.y = min(p.y,y-.006)
                vertex.co = obj.matrix_world.inverted() @ p
    rows = 16
    vertices = [(x,contact(back,x,z,True)+.003,z) for z in np.linspace(.31,.565,rows+1)
                for x in (-.027,.027)]
    strip = surface("Brocade back centre panel",vertices,[(2*r+2,2*r+3,2*r+1,2*r) for r in range(rows)],vest)
    uv = strip.data.uv_layers.new()
    for polygon in strip.data.polygons:
        for li in polygon.loop_indices:
            index = strip.data.loops[li].vertex_index
            uv.data[li].uv = (index%2*.25,index//2/rows*1.6)
    # Gold button rims read at close range without increasing every sphere's
    # density. Existing fronts/back positions remain fitted to the old coat.
    for obj in list(bpy.context.scene.objects):
        if obj.name.startswith(("Gold coat button","Back gold button","Waistcoat button")):
            centre = sum((obj.matrix_world@v.co for v in obj.data.vertices),Vector())/len(obj.data.vertices)
            if obj.name.startswith("Gold coat button"):
                target_x = math.copysign(.18,centre.x)
                obj.location.x += target_x-centre.x
                centre.x = target_x
                target_y = contact(shell,centre.x,centre.z)-.004
                obj.location.y += target_y-centre.y
                centre.y = target_y
            elif obj.name.startswith("Back gold button") and centre.z > .30:
                target_y = contact(shell,centre.x,centre.z,True)+.004
                obj.location.y += target_y-centre.y
                centre.y = target_y
            r = .0057 if obj.name.startswith("Waistcoat") else .0078
            front = centre.y < 0
            bpy.ops.mesh.primitive_torus_add(major_radius=r,minor_radius=.00085,
                major_segments=24,minor_segments=6,location=(centre.x,centre.y+(-.003 if front else .003),centre.z),
                rotation=(math.pi/2,0,0))
            bpy.context.object.name = "Gold engraved button rim"
            bpy.context.object.data.materials.append(gold)
    # All clothing, including collar/bow/buttons, is one mesh with material
    # islands. Towel, body, face and headset deliberately remain outside it.
    excluded = {"body","fur","headset"}
    clothes = [o for o in bpy.context.scene.objects if o.type == "MESH"
               and o.get("part") not in excluded
               and not o.name.startswith(("Black button eye","Small smile"))]
    for obj in clothes:
        bpy.context.view_layer.objects.active = obj
        for mod in list(obj.modifiers):
            bpy.ops.object.modifier_apply(modifier=mod.name)
    join_group("Butler outfit - one piece",clothes,"outfit")

    # One separate, continuous folded towel, shaped over the raised arm.
    before = set(bpy.context.scene.objects)
    towelmat = white.copy()
    towelmat.name = "Ivory terry service towel"
    towelmat.node_tree.nodes.get("Principled BSDF").inputs["Base Color"].default_value = (.92,.90,.84,1)
    normal = next(n for n in towelmat.node_tree.nodes if n.type == "NORMAL_MAP")
    normal.inputs["Strength"].default_value = .85
    rng = np.random.default_rng(13)
    height = rng.random((512,512))
    height = (height+np.roll(height,1,0)+np.roll(height,1,1))/3
    dy,dx = np.gradient(height)
    tangent = np.stack((-dx*2.0,-dy*2.0,np.ones_like(dx)),axis=-1)
    tangent /= np.linalg.norm(tangent,axis=-1,keepdims=True)
    pixels = np.concatenate((tangent*.5+.5,np.ones((512,512,1))),axis=-1)
    terry = bpy.data.images.new("Fine terry loop normal",512,512,alpha=False)
    terry.colorspace_settings.name = "Non-Color"
    terry.pixels.foreach_set(pixels.astype('f4').ravel())
    terry.pack()
    normal_tex = next(link.from_node for link in towelmat.node_tree.links if link.to_node==normal and link.to_socket.name=="Color")
    normal_tex.image = terry
    rows,cols = 48,24
    path = [(-.145,.195),(-.145,.29),(-.15,.40),(-.17,.455),
            (-.20,.479),(-.235,.475),(-.265,.45),(-.28,.40),(-.285,.285),(-.289,.177)]
    # Linear interpolation plus subdivision produces a broad soft U fold.
    vertices = []
    for row in range(rows+1):
        t = row/rows*(len(path)-1)
        j = min(len(path)-2,int(t))
        f = t-j
        y,z = (path[j][a]*(1-f)+path[j+1][a]*f for a in range(2))
        for i in range(cols+1):
            u = i/cols
            corner = .004*(abs(2*u-1)**12)*(abs(2*row/rows-1)**12)
            vertices.append((-.310+(u-.5)*.139,
                y+.0022*math.cos(u*math.pi*6)*math.sin(row/rows*math.pi),z+corner))
    faces = [(r*(cols+1)+c,r*(cols+1)+c+1,(r+1)*(cols+1)+c+1,(r+1)*(cols+1)+c)
             for r in range(rows) for c in range(cols)]
    towel = surface("Continuous draped service towel",vertices,faces,towelmat)
    uv = towel.data.uv_layers.new()
    for poly in towel.data.polygons:
        for li in poly.loop_indices:
            i = towel.data.loops[li].vertex_index
            uv.data[li].uv = (i%(cols+1)/cols,i//(cols+1)/rows*3)
    sub = towel.modifiers.new("Rounded cloth fold","SUBSURF")
    sub.levels = 1
    towel.modifiers.new("Separate cloth thickness","SOLIDIFY").thickness = .0016
    for row in (0,rows):
        pts = [Vector(vertices[row*(cols+1)+i]) for i in range(cols+1)]
        cord("Rounded towel bound edge",pts,.0011,towelmat)
        for i in range(35):
            x = -.375+i*.0037
            yy,zz = path[0 if row==0 else -1]
            offset = .002 if row==0 else -.002
            surface("Towel short hem stitch",[(x,yy+offset,zz+.008),(x+.0021,yy+offset,zz+.008),
                (x+.0021,yy+offset,zz+.0087),(x,yy+offset,zz+.0087)],[(0,1,2,3)],white)
    for col in (0,cols):
        pts = [vertices[r*(cols+1)+col] for r in range(rows+1)]
        cord("Towel long stitched border",pts,.0008,towelmat)
    towelparts = list(set(bpy.context.scene.objects)-before)
    for obj in towelparts:
        bpy.context.view_layer.objects.active = obj
        for mod in list(obj.modifiers):
            bpy.ops.object.modifier_apply(modifier=mod.name)
    join_group("White service towel - separate",towelparts,"towel")
    for obj in bpy.context.scene.objects:
        if obj.name.startswith(("Black button eye","Small smile")):
            obj["part"] = "face"
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.export_scene.gltf(filepath=str(WORK/NAME),export_format="GLB",export_apply=True,
        export_extras=True,export_vertex_color="ACTIVE",export_all_vertex_colors=False)
    stats = {"source_sha256":AVATAR_SHA256,"avatar_file":NAME,
        "avatar_sha256":hashlib.sha256((WORK/NAME).read_bytes()).hexdigest(),
        "bytes":(WORK/NAME).stat().st_size,"references":"Owner-provided headset, bow, outfit and towel sheets",
        "outfit_meshes":1,"separate_towel_meshes":1,
        "rigged":False,"runtime_test":"Not run in Muse or on iPhone"}
    (WORK/"avatar-build.json").write_text(json.dumps(stats,indent=2)+"\n")
    print(json.dumps(stats,indent=2))


if __name__ == "__main__":
    build()
