"""Inspect the actual exported image payloads and PBR channels, not scene nodes."""
import io
import hashlib
import json
import struct

from PIL import Image

from build_room import WORK
from render_review import glb_document


def verify():
    path=WORK/"kitchen-study-materials.glb"
    doc=glb_document(path)
    blob=path.read_bytes()
    json_length=struct.unpack_from("<I",blob,12)[0]
    binary=blob[20+json_length+8:]
    images=[]
    decoded=0
    for item in doc.get("images",[]):
        view=doc["bufferViews"][item["bufferView"]]
        offset=view.get("byteOffset",0)
        img=Image.open(io.BytesIO(binary[offset:offset+view["byteLength"]]))
        img.load()
        assert max(img.size)<=1024,(item.get("name"),img.size)
        decoded += img.width*img.height*4
        images.append(img)
    assert decoded<=64*1024*1024, decoded
    mapped=[]
    for mat in doc["materials"]:
        name=mat.get("name","")
        if not name.startswith("PBR "):
            continue
        pbr=mat["pbrMetallicRoughness"]
        if any(s in name for s in ["oak","walnut","linen","cloth","knit","limestone","steel","brass"]):
            assert "baseColorTexture" in pbr,name
            assert "metallicRoughnessTexture" in pbr,name
            assert "normalTexture" in mat,name
            mapped.append(name)
        if "steel" in name or "brass" in name:
            factor=pbr.get("metallicFactor",1)
            assert factor>=.85,(name,factor)
            texture=doc["textures"][pbr["metallicRoughnessTexture"]["index"]]
            channel=images[texture["source"]].convert("RGB").getchannel("B")
            assert channel.getextrema()[0]>=240,(name,channel.getextrema())
    assert len(mapped)>=10,mapped
    assert not doc.get("animations") and not doc.get("skins")
    report=json.loads((WORK/"verification-materials.json").read_text())
    assert report["room_triangles"]<100000
    assert report["avatar_unchanged"] and not report["furniture_intrusions"]
    report.update({"embedded_images":len(images),"largest_texture_edge":max(max(img.size) for img in images),
                   "decoded_rgba_texture_bytes":decoded,
                   "pbr_materials_with_color_roughness_normal":mapped,
                   "metallic_texture_channels_verified":True,
                   "room_sha256":hashlib.sha256(blob).hexdigest()})
    (WORK/"verification-materials.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,indent=2))


if __name__=="__main__":
    verify()
