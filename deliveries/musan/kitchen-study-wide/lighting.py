"""Four mobile-minded room lights, shared by the GLB and review renderer.

Blender positions are Z-up. The JSON handoff also provides glTF Y-up positions.
Only the sunset light requests shadows; host renderers choose their own budget.
"""
import json
import math
import struct

import bpy
from mathutils import Vector

from build_room import WORK

LIGHTS=[
    {"name":"Golden string glow left","type":"POINT","position":[-2.65,1.91,2.04],
     "color":[1,.47,.16],"power_watts":52,"radius":.28,"range":4.2,"shadows":False},
    {"name":"Golden string glow right","type":"POINT","position":[2.65,1.91,2.04],
     "color":[1,.47,.16],"power_watts":52,"radius":.28,"range":4.2,"shadows":False},
    {"name":"Amber desk lamp","type":"POINT","position":[-3.76,-.52,1.21],
     "color":[1,.52,.20],"power_watts":24,"radius":.065,"range":2.0,"shadows":False},
    {"name":"Round window sunset","type":"SPOT","position":[1.10,2.08,1.52],
     "target":[-.65,-1.55,.13],"color":[1,.55,.26],"power_watts":180,
     "radius":.30,"range":8.0,"angle_degrees":100,"shadows":True},
]


def add_room_lights():
    for light in LIGHTS:
        data=bpy.data.lights.new(light["name"],light["type"])
        data.energy=light["power_watts"]
        data.color=light["color"]
        data.shadow_soft_size=light["radius"]
        data.use_shadow=light["shadows"]
        data.use_custom_distance=True
        data.cutoff_distance=light["range"]
        if light["type"]=="SPOT":
            data.spot_size=math.radians(light["angle_degrees"])
            data.spot_blend=.80
        obj=bpy.data.objects.new(light["name"],data)
        bpy.context.collection.objects.link(obj)
        obj.location=light["position"]
        obj["runtime_cast_shadow"]=light["shadows"]
        if "target" in light:
            obj.rotation_euler=(Vector(light["target"])-obj.location).to_track_quat("-Z","Y").to_euler()


def write_preset():
    path=WORK/"kitchen-study-materials.glb"
    blob=path.read_bytes()
    length=struct.unpack_from("<I",blob,12)[0]
    doc=json.loads(blob[20:20+length])
    exported=doc["extensions"]["KHR_lights_punctual"]["lights"]
    values=[]
    for source in LIGHTS:
        item=next(item for item in exported if item["name"]==source["name"])
        x,y,z=source["position"]
        values.append({**item,"position_y_up":[x,z,-y],
                       "cast_shadow":source["shadows"],
                       "soft_shadow_radius_source_units":source["radius"]})
        if "target" in source:
            x,y,z=source["target"]
            values[-1]["target_y_up"]=[x,z,-y]
    preset={"coordinate_system":"glTF Y-up; source units, not calibrated meters",
            "embedded_extension":"KHR_lights_punctual",
            "intensity_unit":"candela, copied from the exported GLB",
            "lights":values,
            "review_environment":{"color_linear_rgb":[.14,.08,.035],"strength":.16,
                                  "tone_mapper":"AgX","exposure_ev":.45},
            "review_only_area_fill_blender_watts":[
                {"name":"Large golden key","position_y_up":[-3,7,4],"power_watts":320,
                 "size":5,"color_linear_rgb":[1,.72,.44],"target_y_up":[0,.5,0]},
                {"name":"Low dusk fill","position_y_up":[4,6,1],"power_watts":100,
                 "size":4,"color_linear_rgb":[.65,.72,.85],"target_y_up":[0,.5,0]},
                {"name":"Warm ceiling bounce","position_y_up":[0,6,-1],"power_watts":180,
                 "size":4,"color_linear_rgb":[1,.74,.44],"target_y_up":[0,.5,0]}],
            "host_setup":{"avoid_duplicate_lights":"Import embedded lights OR create these, never both",
                          "shadows":"Prefer only the sunset shadow; disable all on slower phones",
                          "ambient":"Dim warm environment; avoid a bright grey/white default hemisphere",
                          "environment_reflections":"Keep a low-level environment reflection for the metal",
                          "tone_mapping":"Use a filmic tone mapper; avoid clipping amber highlights",
                          "review_lighting":"See render_review.py for additional non-exported area fill"}}
    (WORK/"lighting-evening.json").write_text(json.dumps(preset,indent=2)+"\n")
