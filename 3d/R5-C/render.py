"""Fixed Cycles inspection rig; presentation camera changes the angle, not the light."""
import argparse
import importlib.util
from pathlib import Path
import sys

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
    "needlework": (960, 48), "regions": (900, 24), "plain-control": (1100, 48),
}


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
    camera("presentation", (.425,.066,.774), (1.52,-2.84,.66), 1.204)
    # Outboard upper wing / boxing seam; close enough to resolve individual stitches.
    camera("needlework", (.632,.245,.913), (.73,-.69,.24), .125)
    camera("plain-control", *rig.MACROS["channels"])
    for name in names:
        orig = []
        if name == "plain-control":
            for mat in bpy.data.materials:
                node = mat.node_tree.nodes.get(FINISH) if mat.node_tree else None
                if node and node.inputs["Perforation"].default_value:
                    sock = node.inputs["Perforation"]
                    orig.append((sock, sock.default_value))
                    sock.default_value = 0
        detail = bpy.data.collections["06 • Removable topstitch"]
        detail.hide_render = name=="regions"
        size, samples = VIEWS[name]
        rig.render(out,[name],samples,size)
        detail.hide_render = False
        for sock, val in orig:
            sock.default_value = val


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("out", type=Path)
    parser.add_argument("views", nargs="+", choices=VIEWS)
    a = parser.parse_args(sys.argv[sys.argv.index("--")+1:])
    run(a.out.resolve(), a.views)
