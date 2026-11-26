"""Render matched R5-C cameras. All changes to scene, camera and finish are in memory."""
import argparse
from pathlib import Path
import sys

import bpy

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "R5-C"))
from render import rig, camera
from leather import FINISH

OVERVIEWS = ("before", "refined", "plain")
DETAILS = ("lumbar", "cushion", "leather")


def render(out, views):
    scene = bpy.context.scene
    scene.cycles.seed = 11
    scene.cycles.denoising_input_passes = "RGB_ALBEDO_NORMAL"
    scene.cycles.denoising_prefilter = "ACCURATE"
    scene.cycles.pixel_filter_type = "BLACKMAN_HARRIS"
    scene.cycles.filter_width = 1.25
    for view in views:
        saved = []
        if view == "plain":
            for name in ("Yoke", "Lumbar", "Waterfall"):
                mat = bpy.data.materials["Cognac • " + name]
                socket = mat.node_tree.nodes[FINISH].inputs["Perforation"]
                saved.append((socket, socket.default_value))
                socket.default_value = 0
        if view in OVERVIEWS:
            cam = bpy.data.objects["CAM_three-quarter"].copy()
            cam.name = "CAM_" + view
            bpy.data.collections["REVIEW_ONLY"].objects.link(cam)
            rig.render(out, [view], 44, 1536)
        else:
            if view == "lumbar":
                camera(view, *rig.MACROS["channels"])
            elif view == "leather":
                camera(view, (.632, .245, .913), (.73, -.69, .24), .125)
            rig.render(out, [view], 36, 880)
        for socket, value in saved:
            socket.default_value = value


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("out", type=Path)
    parser.add_argument("views", nargs="+", choices=OVERVIEWS + DETAILS)
    args = parser.parse_args(sys.argv[sys.argv.index("--") + 1:])
    render(args.out.resolve(), args.views)
