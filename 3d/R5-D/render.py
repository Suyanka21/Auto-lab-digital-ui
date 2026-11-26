"""Render the six R5-D inspection cameras. Never save scene overrides."""
import argparse
from pathlib import Path
import sys

import bpy

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from pair import CAMERAS, CONTEXT, DRIVER, PASSENGER, PREFIX


def diagnostic():
    colours = {
        "Cognac • Yoke": (.08, .36, .73), "Cognac • Lumbar": (.025, .44, .30),
        "Cognac • Waterfall": (.84, .36, .045), "Cognac • surrounds": (.46, .105, .055),
        "Cognac • boxing": (.30, .16, .44), "Cognac • head restraint": (.30, .40, .075),
        "Study • controls": (1., .69, .015), "Shield": (.04, .33, .39),
    }
    temporary, restore = {}, []
    for obj in bpy.data.collections[PASSENGER].all_objects:
        for slot in obj.material_slots:
            name = slot.material.name.removeprefix(PREFIX)
            if obj.name == PREFIX + "Shield • outboard control carrier":
                name = "Shield"
            if name not in colours:
                continue
            if name not in temporary:
                mat = bpy.data.materials.new("Diagnostic / " + name)
                mat.use_nodes = True
                mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (*colours[name], 1)
                temporary[name] = mat
            restore.append((slot, slot.material))
            slot.material = temporary[name]
    return restore


def render(out, views, preview):
    out.mkdir(parents=True, exist_ok=True)
    scene = bpy.context.scene
    for name in views:
        path = out / (name + ".png")
        if path.exists():
            raise FileExistsError(path)
        single = name in ("passenger", "diagnostic")
        bpy.data.collections[DRIVER].hide_render = single
        context = bpy.data.collections[CONTEXT]
        context.hide_render = context.hide_viewport = name != "cabin"
        scene.camera = bpy.data.objects["R5-D / " + name]
        scene.render.resolution_x, scene.render.resolution_y = (1100, 1100) if single else (1360, 960)
        scene.render.resolution_percentage = 38 if preview else 100
        scene.cycles.samples = 4 if preview else 28
        restore = diagnostic() if name == "diagnostic" else []
        scene.render.filepath = str(path)
        bpy.ops.render.render(write_still=True)
        for slot, original in restore:
            slot.material = original


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("out", type=Path)
    parser.add_argument("views", nargs="+", choices=CAMERAS)
    parser.add_argument("--preview", action="store_true")
    args = parser.parse_args(sys.argv[sys.argv.index("--") + 1:])
    render(args.out.resolve(), args.views, args.preview)
