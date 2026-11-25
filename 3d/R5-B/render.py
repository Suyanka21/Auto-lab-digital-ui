"""Read only: reproduce review cameras and panel IDs, never save the scene."""
import argparse
from pathlib import Path
import sys

import bpy
from mathutils import Vector


MACROS = {
    "bolster": ((.566,.218,.842),(.63,-1.31,.25),.475),
    "channels": ((.425,.171,.694),(-.22,-1.52,.42),.423),
    "cushion": ((.425,-.079,.480),(.44,-.75,.66),.600),
}
COLOURS = {
    "upper": (.14,.38,.57), "lumbar": (.08,.44,.38), "pan": (.72,.36,.08),
    "bolster": (.47,.18,.10), "boxing": (.27,.19,.37), "return": (.27,.19,.37),
}


def render(out, views, samples, size):
    scene = bpy.context.scene
    rig = bpy.data.collections["REVIEW_ONLY"]
    if any((out/(name+".png")).exists() for name in views):
        raise FileExistsError("Choose a fresh directory for this pass")
    for name in views:
        if name in MACROS:
            pos, ray, width = MACROS[name]
            data = bpy.data.cameras.new(name)
            data.type, data.ortho_scale = "ORTHO", width
            cam = bpy.data.objects.new("CAM_"+name,data)
            rig.objects.link(cam)
            cam.location = Vector(pos)+Vector(ray)
            cam.rotation_euler = (-Vector(ray)).to_track_quat('-Z','Y').to_euler()
        else:
            cam = bpy.data.objects["CAM_"+("three-quarter" if name=="regions" else name)]
        scene.camera = cam
        old = []
        if name=="regions":
            mats = {}
            for tag,col in COLOURS.items():
                mat = bpy.data.materials.new("REVIEW_ONLY • "+tag)
                mat.use_nodes = True
                mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (*col,1)
                mats[tag] = mat
            for obj in bpy.data.collections["01 • Tailored upholstery panels"].objects:
                old.append((obj,obj.data.materials[0]))
                obj.data.materials[0] = mats[obj["editable_region"]]
        scene.render.engine, scene.cycles.device = 'CYCLES','CPU'
        scene.cycles.samples, scene.cycles.use_denoising = samples, True
        scene.render.resolution_percentage = 100
        scene.render.resolution_x = scene.render.resolution_y = size
        scene.render.image_settings.file_format = 'PNG'
        scene.render.filepath = str(out/(name+".png"))
        bpy.ops.render.render(write_still=True)
        for obj,mat in old:
            obj.data.materials[0] = mat


if __name__ == "__main__":
    p=argparse.ArgumentParser()
    p.add_argument("out",type=Path)
    p.add_argument("views",nargs="+",choices=["front","side","three-quarter","regions",*MACROS])
    p.add_argument("--samples",type=int,default=36)
    p.add_argument("--size",type=int,default=1100)
    a=p.parse_args(sys.argv[sys.argv.index("--")+1:])
    render(a.out.resolve(),a.views,a.samples,a.size)
