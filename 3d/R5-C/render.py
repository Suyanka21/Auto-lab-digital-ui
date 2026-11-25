"""Fixed Cycles inspection rig; presentation camera changes the angle, not the light."""
import argparse
import importlib.util
from pathlib import Path
import sys
sys.dont_write_bytecode = True

import bpy
from mathutils import Vector

D = Path(__file__).resolve().parent
sys.path.insert(0, str(D))
from leather import FINISH

spec = importlib.util.spec_from_file_location("r5b_review", D.parent/"R5-B/render.py")
rig = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rig)

# More pixels on the overview prevent fine punches from vanishing in denoising.
VIEWS = {
    "presentation": (1536, 52), "three-quarter": (1200, 44),
    "bolster": (1100, 48), "channels": (1100, 48), "cushion": (1100, 48),
    "needlework": (960, 48), "material-map": (1000, 26), "plain-control": (1100, 48),
}

ID_COLOURS = {
    "Cognac • Yoke": (.09,.29,.57), "Cognac • Lumbar": (.045,.40,.30),
    "Cognac • Waterfall": (.71,.35,.056), "Cognac • surrounds": (.47,.12,.07),
    "Cognac • boxing": (.25,.17,.38), "Cognac • head restraint": (.24,.34,.09),
    "Cognac • recessed turn": (.026,.029,.031), "Topstitch • warm tonal thread": (.88,.67,.27),
}


def material_map():
    original, mats = [], {}
    for ob in bpy.data.collections["R5_FRONT_SEAT_MASTER"].all_objects:
        for slot in ob.material_slots:
            source = slot.material
            if source.name not in ID_COLOURS: continue
            if source.name not in mats:
                m = bpy.data.materials.new("Review ID / "+source.name)
                m.use_nodes = True
                m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (*ID_COLOURS[source.name],1)
                mats[source.name] = m
            original.append((slot,source))
            slot.material = mats[source.name]
    return original


def camera(name, target, direction, width):
    data = bpy.data.cameras.new(name)
    data.type, data.ortho_scale = "ORTHO", width
    cam = bpy.data.objects.new("CAM_"+name, data)
    bpy.data.collections["REVIEW_ONLY"].objects.link(cam)
    cam.location = Vector(target)+Vector(direction)
    cam.rotation_euler = (-Vector(direction)).to_track_quat("-Z","Y").to_euler()
    return cam


def run(out, names):
    if any((out/(n+".png")).exists() for n in names): raise FileExistsError("Use an unused view path")
    camera("presentation", (.425,.066,.774), (1.52,-2.84,.66), 1.37)
    # Outboard upper wing / boxing seam; close enough to resolve individual stitches.
    camera("needlework", (.632,.245,.913), (.73,-.69,.24), .125)
    camera("plain-control", *rig.MACROS["channels"])
    cam = bpy.data.objects["CAM_three-quarter"].copy()
    cam.name = "CAM_material-map"
    bpy.data.collections["REVIEW_ONLY"].objects.link(cam)
    for name in names:
        orig = []
        if name == "plain-control":
            for mat in bpy.data.materials:
                node = mat.node_tree.nodes.get(FINISH) if mat.node_tree else None
                if node and node.inputs["Perforation"].default_value:
                    sock = node.inputs["Perforation"]
                    orig.append((sock, sock.default_value))
                    sock.default_value = 0
        slots = material_map() if name=="material-map" else []
        size, samples = VIEWS[name]
        rig.render(out,[name],samples,size)
        for slot, original in slots:
            slot.material = original
        for sock, val in orig:
            sock.default_value = val


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("out", type=Path)
    parser.add_argument("views", nargs="+", choices=VIEWS)
    a = parser.parse_args(sys.argv[sys.argv.index("--")+1:])
    run(a.out.resolve(), a.views)
