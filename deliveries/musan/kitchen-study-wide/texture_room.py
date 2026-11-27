"""Apply embedded, mobile-sized PBR materials to the room; never import the avatar.

Original generated textures, no downloaded images/services. Coordinates and
furniture are unchanged. Run build_room.py first, then this file with Python 3.11.
"""
import hashlib
import json
import math

import bpy
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

from build_room import AVATAR_SHA256, WORK, box
from mathutils import Vector

TEXTURES = WORK / "textures"


def smooth_noise(size, seed, frequencies=(2, 4, 8, 16, 32)):
    rng = np.random.default_rng(seed)
    out = np.zeros((size, size))
    for i, frequency in enumerate(frequencies):
        grid = rng.random((frequency, frequency)).astype(np.float32)
        # Wrap the lattice before interpolation so tile boundaries are coherent.
        grid = np.pad(grid, ((0, 1), (0, 1)), mode="wrap")
        expanded = Image.fromarray(grid).resize((size + size // frequency,)*2,
                                               Image.Resampling.BICUBIC)
        out += np.asarray(expanded)[:size, :size] / (1.6 ** i)
    return (out - out.mean()) / max(out.std(), 1e-6)


def save(name, array):
    path = TEXTURES / (name + ".png")
    Image.fromarray(np.uint8(np.clip(array, 0, 1) * 255)).save(path, optimize=True)
    return path


def relief_maps(name, height, roughness, strength):
    dx = (np.roll(height, -1, 1) - np.roll(height, 1, 1)) * strength
    dy = (np.roll(height, -1, 0) - np.roll(height, 1, 0)) * strength
    normals = np.stack((-dx, dy, np.ones_like(height)), axis=2)
    normals /= np.linalg.norm(normals, axis=2, keepdims=True)
    normal = save(name + "-normal", normals * .5 + .5)
    # glTF metallic/roughness: green is roughness, blue metallic (zero here).
    orm = save(name + "-orm", np.stack((np.ones_like(height), roughness,
                                       np.zeros_like(height)), axis=2))
    return normal, orm


def generate_maps():
    TEXTURES.mkdir(exist_ok=True)
    n = 1024
    v, u = np.mgrid[0:1:complex(n), 0:1:complex(n)]
    noise = smooth_noise(n, 46)
    wander = .23 * np.sin(v * 2 * np.pi) + .10 * np.sin(v * 6 * np.pi)
    # Narrow pores, long fibres and occasional oval knots, not uniform stripes.
    warp = u * 30 + wander + .12 * noise
    for x, y, radius in [(.24, .33, .045), (.77, .76, .032)]:
        r = np.sqrt(((u - x) / radius)**2 + ((v - y) / (radius * 2.3))**2)
        warp += .48 * np.exp(-r / 2) * np.sin(r * 2.8)
    pore = np.clip((np.sin(warp * 2 * np.pi) - .65) / .35, 0, 1)
    rng = np.random.default_rng(911)
    fibres = np.zeros((n,n))
    for rows, cols, weight in [(8,128,.6),(24,512,.25),(64,1024,.12)]:
        grid=np.pad(rng.random((rows,cols)).astype(np.float32), ((0,1),(0,1)), mode="wrap")
        long_noise=np.asarray(Image.fromarray(grid).resize((n+n//cols,n+n//rows),
                                                            Image.Resampling.BICUBIC))[:n,:n]
        fibres += (long_noise-.5)*weight
    height = .10 * noise - .12 * pore + .30 * fibres
    modulation = 1 + .065 * noise - .075 * pore + .40 * fibres
    for x,y,radius in [(.24,.33,.045),(.77,.76,.032)]:
        r=np.sqrt(((u-x)/radius)**2+((v-y)/(radius*2.3))**2)
        modulation -= .24*np.exp(-r*r*1.1) + .045*np.sin(r*3)*np.exp(-r/2)
    wood_maps = relief_maps("oak", height, np.clip(.48 + .04*noise + .06*pore, .3, .7), 1.6)
    maps = {}
    for name, rgb in {"wall-oak":(184, 142, 96), "honey-oak":(155, 104, 59),
                      "warm-walnut":(139, 91, 51), "floor-oak":(173, 120, 72)}.items():
        maps[name] = (save(name, modulation[...,None] * np.array(rgb)/255), *wood_maps)

    n = 512
    v, u = np.mgrid[0:1:complex(n), 0:1:complex(n)]
    weave = np.sin(u*2*np.pi*48) * np.sin(v*2*np.pi*48)
    slub = smooth_noise(n, 62, (4, 8, 16, 32))
    fabric_maps = relief_maps("linen", weave*.17 + slub*.035,
                             np.clip(.89 + weave*.035 + slub*.012, .8, 1), .8)
    for name, rgb in {"ivory-linen":(232, 220, 195), "plum-linen":(102, 38, 60),
                      "sage-cloth":(106, 125, 99)}.items():
        maps[name] = (save(name, (1 + .09*weave + .012*slub)[...,None]
                           * np.array(rgb)/255), *fabric_maps)
    stitch=np.cos((u*16+.32*np.cos(v*2*np.pi*16))*2*np.pi)
    knit_maps=relief_maps("knit",stitch*.40+weave*.035,
                          np.clip(.92+stitch*.025, .84,1),1.4)
    maps["ivory-knit"]=(save("ivory-knit",(1+stitch*.12+weave*.025)[...,None]
                               *np.array([218,203,174])/255),*knit_maps)
    paper_noise=np.random.default_rng(92).normal(0,.004,(512,512))
    paper_path=save("paper",(1+paper_noise)[...,None]*np.array([230,222,198])/255)
    page=Image.open(paper_path)
    draw=ImageDraw.Draw(page)
    font=ImageFont.load_default(size=24)
    small=ImageFont.load_default(size=17)
    draw.text((45,48),"Kitchen notes",font=font,fill=(80,75,62))
    for j,line in enumerate(["Tea for two", "Warm the cups", "Fresh water", "Steep 3 minutes", "Serve with bread"]):
        draw.text((45,126+j*48),line,font=small,fill=(104,100,83))
        draw.line([(43,151+j*48),(450,151+j*48)],fill=(198,187,157),width=1)
    page.save(paper_path)
    paper_maps=relief_maps("paper",paper_noise,np.full((512,512),.94),.4)
    maps["paper"]=(paper_path,*paper_maps)
    noise = smooth_noise(n, 73)
    fine = np.random.default_rng(15).normal(0, .035, (n,n))
    stone = np.clip(1 + noise*.045 + fine*.16, .75, 1.15)
    stone_maps = relief_maps("limestone", noise*.1 + fine,
                            np.clip(.63 + noise*.04, .4, .8), .8)
    maps["limestone"] = (save("limestone", stone[...,None] * np.array([202,195,174])/255), *stone_maps)
    brushed=np.asarray(Image.fromarray(np.random.default_rng(8).random((512,8)).astype(np.float32))
                       .resize((512,512), Image.Resampling.BICUBIC))-.5
    metal_maps=relief_maps("brushed-metal", brushed*.025,
                           .25+brushed*.035, .7)
    maps["steel"]=(save("steel", np.repeat((.74+brushed*.014)[...,None],3,axis=2)),*metal_maps)
    maps["brass"]=(save("brass",(1+brushed*.016)[...,None]*np.array([205,159,80])/255),*metal_maps)
    sky=np.zeros((512,512,3))
    t=np.linspace(0,1,512)[:,None,None]
    sky[:]=(1-t)*np.array([109,147,171])[None,None,:]+t*np.array([247,208,148])[None,None,:]
    landscape=Image.fromarray(np.uint8(sky))
    draw=ImageDraw.Draw(landscape)
    for base,amplitude,rgb in [(300,28,(128,144,145)),(355,35,(98,119,113)),
                               (412,24,(63,91,78)),(472,19,(43,68,52))]:
        ridge=[(x,base+amplitude*(math.sin(x*.012+base)+.3*math.sin(x*.037))) for x in range(512)]
        draw.polygon(ridge+[(511,512),(0,512)],fill=rgb)
    landscape.filter(ImageFilter.GaussianBlur(3)).save(TEXTURES/"window-dusk.png")
    return maps


def pbr(name, maps=None, color=(1,1,1), roughness=.5, metallic=0, normal_strength=.3):
    mat = bpy.data.materials.new("PBR " + name)
    mat.use_nodes = True
    nodes, links = mat.node_tree.nodes, mat.node_tree.links
    shader = nodes.get("Principled BSDF")
    shader.inputs["Base Color"].default_value = (*color, 1)
    shader.inputs["Roughness"].default_value = roughness
    shader.inputs["Metallic"].default_value = metallic
    if maps:
        for path, socket in zip(maps, ["Base Color", "Normal", "Roughness"]):
            image = bpy.data.images.load(str(path), check_existing=True)
            if socket != "Base Color":
                image.colorspace_settings.name = "Non-Color"
            tex = nodes.new("ShaderNodeTexImage")
            tex.image = image
            tex.extension = "REPEAT"
            if socket == "Normal":
                normal = nodes.new("ShaderNodeNormalMap")
                normal.inputs["Strength"].default_value = normal_strength
                links.new(tex.outputs["Color"], normal.inputs["Color"])
                links.new(normal.outputs["Normal"], shader.inputs[socket])
            elif socket == "Roughness":
                separate = nodes.new("ShaderNodeSeparateColor")
                links.new(tex.outputs["Color"], separate.inputs["Color"])
                links.new(separate.outputs["Green"], shader.inputs[socket])
            else:
                links.new(tex.outputs["Color"], shader.inputs[socket])
    return mat


def uv_project(obj):
    """Box project in object coordinates with physical grain direction/scale.

    UVs themselves carry repetition: no procedural nodes or texture transforms
    are required at runtime. Per-object offsets avoid identical plank repeats.
    """
    mesh = obj.data
    uv = mesh.uv_layers.active or mesh.uv_layers.new(name="UVMap")
    if obj.get("window_background"):
        for li,loop in enumerate(mesh.loops):
            co=mesh.vertices[loop.vertex_index].co
            uv.data[li].uv=(co.x/1.27+.5,co.y/1.27+.5)
        return
    if obj.name.startswith("Open notebook"):
        bounds=[Vector(p) for p in obj.bound_box]
        lower=[min(p[i] for p in bounds) for i in range(3)]
        upper=[max(p[i] for p in bounds) for i in range(3)]
        for li,loop in enumerate(mesh.loops):
            co=mesh.vertices[loop.vertex_index].co
            uv.data[li].uv=((co.x-lower[0])/(upper[0]-lower[0]),
                            (co.y-lower[1])/(upper[1]-lower[1]))
        return
    dimensions = obj.dimensions
    vertical = ("wall" in obj.name.lower() or "post" in obj.name.lower()
                or "leg" in obj.name.lower() or "side" in obj.name.lower()
                or "back" in obj.name.lower() or "spine" in obj.name.lower())
    grain_axis = 2 if vertical else max(range(3), key=lambda i: dimensions[i])
    offset = int(hashlib.sha256(obj.name.encode()).hexdigest()[:4],16) / 65536
    fabric = any(any(s in m.name for s in ["linen","cloth","knit"]) for m in mesh.materials)
    for polygon in mesh.polygons:
        dominant = max(range(3), key=lambda i: abs(polygon.normal[i]))
        axes = [a for a in range(3) if a != dominant]
        if grain_axis in axes:
            axes = [a for a in axes if a != grain_axis] + [grain_axis]
        # Wood tile covers 0.55 across x 2.6 along grain; cloth 0.3 square.
        scale = (.30,.30) if fabric else (.55,2.6)
        for li in polygon.loop_indices:
            co = mesh.vertices[mesh.loops[li].vertex_index].co
            uv.data[li].uv = (co[axes[0]] * abs(obj.scale[axes[0]]) / scale[0] + offset,
                              co[axes[1]] * abs(obj.scale[axes[1]]) / scale[1] + offset*.7)


def build():
    assert hashlib.sha256((WORK/"musan-butler-detail-v12.glb").read_bytes()).hexdigest() == AVATAR_SHA256
    maps = generate_maps()
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(WORK/"kitchen-study.glb"), loglevel=40)
    palette = {name:pbr(name, images, normal_strength=.4 if "linen" in name else .25)
               for name, images in maps.items()}
    palette.update({
        "brass":pbr("brushed warm brass", maps["brass"], roughness=.27, metallic=.9, normal_strength=.2),
        "steel":pbr("satin stainless steel", maps["steel"], roughness=.24, metallic=.95, normal_strength=.2),
        "enamel":pbr("ivory enamel", color=(.72,.68,.56), roughness=.28),
        "paint":pbr("painted timber", color=(.78,.74,.64), roughness=.43),
        "ceramic":pbr("sage glazed ceramic", color=(.115,.20,.145), roughness=.21),
        "terracotta":pbr("unglazed terracotta", color=(.43,.19,.095), roughness=.86),
        "glass":pbr("blue dusk window glass", color=(.30,.43,.48), roughness=.12),
        "paper":pbr("uncoated paper", maps["paper"], roughness=.94, normal_strength=.08),
    })
    sky_mat=pbr("distant dusk beyond glass",roughness=1)
    shader=sky_mat.node_tree.nodes.get("Principled BSDF")
    tex=sky_mat.node_tree.nodes.new("ShaderNodeTexImage")
    tex.image=bpy.data.images.load(str(TEXTURES/"window-dusk.png"))
    sky_mat.node_tree.links.new(tex.outputs["Color"],shader.inputs["Base Color"])
    sky_mat.node_tree.links.new(tex.outputs["Color"],shader.inputs["Emission Color"])
    shader.inputs["Emission Strength"].default_value=.18
    shader.inputs["Specular IOR Level"].default_value=0
    disk=bpy.data.objects.get("Round dusk window")
    disk.data=disk.data.copy()
    disk.data.materials.clear()
    disk.data.materials.append(sky_mat)
    disk["window_background"]=True
    glazing=palette["glass"].copy()
    glazing.name="PBR reflective clear glazing"
    glazing.node_tree.nodes.get("Principled BSDF").inputs["Alpha"].default_value=.16
    glazing.surface_render_method="DITHERED"
    vertices=[(1.10,2.195,1.45)]+[(1.10+.626*math.cos(i*math.tau/64),2.195,
                                           1.45+.626*math.sin(i*math.tau/64)) for i in range(64)]
    faces=[(0,i+1,(i+1)%64+1) for i in range(64)]
    mesh=bpy.data.meshes.new("Single-sided lightweight window glazing")
    mesh.from_pydata(vertices,[],faces)
    obj=bpy.data.objects.new("Round window clear glazing",mesh)
    bpy.context.collection.objects.link(obj)
    obj["layout_zone"]="decoration"
    mesh.materials.append(glazing)
    replacement = {"Warm timber walls":"wall-oak", "Honey oak trim":"honey-oak",
                   "Walnut furniture":"warm-walnut", "Honey ash":"honey-oak",
                   "Ivory woven linen":"ivory-linen", "Plum cushion":"plum-linen",
                   "Sage book cloth":"sage-cloth", "Limestone countertop":"limestone",
                   "Desk lamp brass":"brass", "Aged brass":"brass", "Brushed sink":"steel",
                   "Warm enamel":"enamel", "Ivory painted wood":"paint", "Sage pot":"ceramic",
                   "Terracotta":"terracotta", "Round window dusk glass":"glass",
                   "Window sky":"glass", "Warm paper":"paper"}
    # Correct the stretched, repetitive cross-room strips to staggered boards
    # running into the room, like the supplied reference. Preserve floor height.
    boards = [o for o in bpy.context.scene.objects if o.name.startswith("Individual ash floorboard")]
    floor_top = max((o.matrix_world @ Vector(p)).z for o in boards for p in o.bound_box)
    floor_bottom = min((o.matrix_world @ Vector(p)).z for o in boards for p in o.bound_box)
    for obj in boards:
        bpy.data.objects.remove(obj, do_unlink=True)
    for column in range(30):
        x = -4.2 + (column+.5)*.28
        y = -2.3
        segment = 0
        while y < 2.299:
            length = min((.66 + (column%3)*.37) if segment == 0 else 1.55, 2.3-y)
            board = box("Natural oak floorboard", (x,y+length/2,(floor_top+floor_bottom)/2),
                        (.274,length-.005,floor_top-floor_bottom), palette["floor-oak"],
                        "architecture", .002)
            y += length
            segment += 1

    # A low-poly folded cloth surface instead of an upholstered cuboid. This
    # only changes room bedding; the character is never loaded by this script.
    old_duvet = bpy.data.objects.get("Ivory duvet")
    bpy.data.objects.remove(old_duvet, do_unlink=True)
    vertices, faces = [], []
    nx, ny = 49, 65
    for j in range(ny):
        v = j/(ny-1)
        y = -.78+v*1.57
        for i in range(nx):
            u = i/(nx-1)
            x = -.64+u*1.28
            edge = max(0,(abs(x)-.51)/.13)
            foot = max(0,(-y-.57)/.21)
            z = .755 - .19*edge**1.7 - .16*foot**1.5
            z += .009*math.sin(x*31+y*11) + .007*math.sin(x*17-y*23)
            z += .018*math.exp(-((x-.18-.1*math.sin(y*3))/.045)**2)
            vertices.append((x+3.45,y+.01,z))
            if i<nx-1 and j<ny-1:
                a=j*nx+i
                faces.append((a,a+1,a+nx+1,a+nx))
    mesh=bpy.data.meshes.new("Draped woven duvet")
    mesh.from_pydata(vertices, [], faces)
    obj=bpy.data.objects.new("Ivory duvet - soft folds",mesh)
    bpy.context.collection.objects.link(obj)
    obj["layout_zone"]="bed"
    mesh.materials.append(palette["ivory-linen"])
    for polygon in mesh.polygons:
        polygon.use_smooth=True
    solid=obj.modifiers.new("Hem thickness", "SOLIDIFY")
    solid.thickness=.012
    for name in ["Ivory pillow", "Plum pillow"]:
        old=bpy.data.objects.get(name)
        matrix=old.matrix_world.copy()
        bounds=[Vector(p) for p in old.bound_box]
        lower=Vector([min(p[i] for p in bounds) for i in range(3)])
        upper=Vector([max(p[i] for p in bounds) for i in range(3)])
        half=(upper-lower)/2
        center=(upper+lower)/2
        bpy.data.objects.remove(old,do_unlink=True)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=48,ring_count=24)
        obj=bpy.context.object
        obj.name=name+" - soft cushion"
        obj.matrix_world=matrix
        obj["layout_zone"]="bed"
        for vertex in obj.data.vertices:
            vertex.co=Vector([center[i]+math.copysign(abs(vertex.co[i])**.44,vertex.co[i])*half[i]
                              for i in range(3)])
        for polygon in obj.data.polygons:
            polygon.use_smooth=True
        obj.data.materials.append(palette["ivory-linen" if name.startswith("Ivory") else "plum-linen"])
    assignments = {}
    for obj in bpy.context.scene.objects:
        if obj.type != "MESH":
            continue
        # glTF importer can share meshes. Each object needs its own UV offsets.
        obj.data = obj.data.copy()
        for slot in obj.material_slots:
            old = slot.material.name
            key = "floor-oak" if old.startswith("Ash plank") else replacement.get(old)
            if obj.name.startswith(("Folded bed throw", "Throw fringe")):
                key = "ivory-knit"
            if key:
                slot.material = palette[key]
                assignments[key] = assignments.get(key,0)+1
        # Preserve the source atlas UVs on untouched food/dishes.
        if any(m.name.startswith("PBR ") for m in obj.data.materials):
            uv_project(obj)
    # Bake room-only modifiers before batching. Join by material AND zone so
    # the floor-clearance check remains meaningful and runtime draw calls fall.
    depsgraph=bpy.context.evaluated_depsgraph_get()
    groups={}
    for obj in list(bpy.context.scene.objects):
        if obj.type!="MESH":
            continue
        if obj.modifiers:
            obj.data=bpy.data.meshes.new_from_object(obj.evaluated_get(depsgraph))
            obj.modifiers.clear()
        if len(obj.data.materials)==1:
            key=(obj.get("layout_zone"),obj.data.materials[0].name)
            groups.setdefault(key,[]).append(obj)
    for (zone,matname),objects in groups.items():
        if len(objects)<2:
            continue
        bpy.ops.object.select_all(action="DESELECT")
        for obj in objects:
            obj.select_set(True)
        bpy.context.view_layer.objects.active=objects[0]
        bpy.ops.object.join()
        obj=bpy.context.object
        obj.name=zone+" - "+matname
        obj["layout_zone"]=zone
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.export_scene.gltf(filepath=str(WORK/"kitchen-study-materials.glb"),
                              export_format="GLB", use_selection=True, export_apply=True,
                              export_extras=True, export_cameras=False, export_lights=False,
                              export_animations=False)
    (WORK/"material-assignments.json").write_text(json.dumps(assignments, indent=2)+"\n")
    print(json.dumps(assignments, indent=2))


if __name__ == "__main__":
    build()
