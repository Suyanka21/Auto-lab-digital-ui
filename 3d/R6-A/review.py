"""Load approved assembly context on demand. All changes are in memory."""
import argparse
from hashlib import sha256
from pathlib import Path
import sys

import bpy

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from bench import CAMERAS, D

PAIR = D.parent / "R5-D/R5-D-front-seat-pair.blend"
PAIR_HASH = "821b2a5695caad7dc71e7e80124c8984f77ac5298f912d4c11c524dae2d1d619"
CONTEXT = ("R5_D_FRONT_SEAT_PAIR", "PLACEMENT ONLY • dashboard and console")


def context():
    if sha256(PAIR.read_bytes()).hexdigest() != PAIR_HASH:
        raise ValueError("Retrieve the approved R5-D source with Git LFS")
    with bpy.data.libraries.load(str(PAIR), link=False) as (source, dest):
        if not set(CONTEXT) <= set(source.collections):
            raise ValueError("Missing positioning references")
        dest.collections = list(CONTEXT)
    for coll in dest.collections:
        bpy.context.scene.collection.children.link(coll)
        coll.hide_viewport = coll.hide_render = False
    bpy.context.view_layer.update()
    return dest.collections


def run(out, views, preview):
    out.mkdir(parents=True, exist_ok=True)
    sc = bpy.context.scene
    stand = bpy.data.objects["Studio stand"]
    refs = []
    for view in views:
        path = out / (view + ".png")
        if path.exists():
            raise FileExistsError(path)
        if view == "cabin" and not refs:
            refs = context()
        for coll in refs:
            coll.hide_render = view != "cabin"
        stand.location.z = -.012 if view == "cabin" else 0
        sc.camera = bpy.data.objects["R6 / " + view]
        sc.render.resolution_percentage = 45 if preview else 100
        sc.cycles.samples = 6 if preview else 32
        sc.render.filepath = str(path)
        bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("out", type=Path)
    p.add_argument("views", nargs="+", choices=CAMERAS)
    p.add_argument("--preview", action="store_true")
    args = p.parse_args(sys.argv[sys.argv.index("--")+1:])
    run(args.out.resolve(), args.views, args.preview)
