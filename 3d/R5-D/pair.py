"""Build a standalone Blender 5.2.2 pair from the approved driver and decoded cabin."""
from hashlib import sha256
import json
from pathlib import Path
import sys

import bpy
from mathutils import Matrix, Vector

APPROVED = "c2674a427043db534e2408c447a7800dc3718a36aa40d33fff6ed7a3695c00f8"
CABIN = "e5bdde016348df34889ec4c0ff0e406caad7e368504308bd5a4f5b725a55c056"
DRIVER = "R5_FRONT_SEAT_MASTER"
PASSENGER = "R5_D_PASSENGER"
PAIR = "R5_D_FRONT_SEAT_PAIR"
CONTEXT = "PLACEMENT ONLY • dashboard and console"
PREFIX = "P • "
INSERTS = ("Cognac • Yoke", "Cognac • Lumbar", "Cognac • Waterfall")
MIRROR = Matrix.Diagonal(Vector((-1, 1, 1, 1)))
CONTEXT_NAMES = {"GEO_Dashboard_Lexus", "GEO_Console_Body", "GEO_Console_Armrest",
                 "GEO_Console_Selector", "GEO_Console_Cupholder_Front", "GEO_Console_Cupholder_Rear"}


def collection(name, parent):
    result = bpy.data.collections.new(name)
    parent.children.link(result)
    return result


def mirror_seat(driver, passenger):
    inserts = {name: bpy.data.materials[name].copy() for name in INSERTS}
    for name, material in inserts.items():
        material.name = PREFIX + name
    # Keep the local frames right-handed. Reflect the data and conjugate the
    # object transform so every world point maps to (-x, y, z).
    keys = {}
    for group in driver.children:
        dest = collection(PREFIX + group.name, passenger)
        for original in group.objects:
            obj = original.copy()
            obj.name = PREFIX + original.name
            obj.data = original.data.copy()
            obj.data.name = obj.name
            dest.objects.link(obj)
            obj.matrix_world = MIRROR @ original.matrix_world @ MIRROR
            obj.data.transform(MIRROR, shape_keys=True)
            if obj.type == "MESH":
                obj.data.flip_normals()  # Reverse face loops and their corner UVs together.
                obj.data.update()
            if obj.data.shape_keys:
                keys[original.data.shape_keys] = obj.data.shape_keys
            if "fitted_to" in obj:
                obj["fitted_to"] = PREFIX + original["fitted_to"]
            for slot in obj.material_slots:
                if slot.material.name in inserts:
                    slot.material = inserts[slot.material.name]
    # Blender copies driver variables verbatim. Rebind both the thread shape
    # and its bevel radius to the passenger's own lumbar shape key.
    for obj in passenger.all_objects:
        for data in (obj.data, obj.data.shape_keys):
            if data and data.animation_data:
                for fcurve in data.animation_data.drivers:
                    for var in fcurve.driver.variables:
                        for target in var.targets:
                            if target.id in keys:
                                target.id = keys[target.id]


def add_context(decoded, scene):
    if decoded["hash"] != CABIN:
        raise ValueError("Run the hash-guarded R5-A production cabin reader")
    context = collection(CONTEXT, scene.collection)
    material = bpy.data.materials.new("Placement reference • slate")
    material.use_nodes = True
    material.diffuse_color = (.10, .15, .19, 1)
    shader = material.node_tree.nodes["Principled BSDF"]
    shader.inputs["Base Color"].default_value = material.diffuse_color
    shader.inputs["Roughness"].default_value = .64
    for node in decoded["nodes"]:
        if node["name"] in CONTEXT_NAMES:
            mesh = bpy.data.meshes.new(node["name"])
            mesh.from_pydata(node["vertices"], [], node["faces"])
            mesh.update()
            obj = bpy.data.objects.new(node["name"], mesh)
            context.objects.link(obj)
            mesh.materials.append(material)
            for face in mesh.polygons:
                face.use_smooth = True
    if set(context.objects.keys()) != CONTEXT_NAMES:
        raise ValueError("Expected dashboard and five centre console components")
    context["production_glb_sha256"] = CABIN
    context.hide_render = context.hide_viewport = True


# Orthographic width in metres. Model space is X lateral, -Y forward, Z up.
CAMERAS = {
    "pair": ((.012, .061, .771), (-1.22, -3.5, 1.1), 2.12),
    "front": ((0, .06, .775), (0, -3, 0), 1.75),
    "rear": ((0, .06, .775), (0, 3, 0), 1.75),
    "passenger": ((-.421, .056, .765), (-2.18, -2.28, .77), 1.36),
    "diagnostic": ((-.421, .056, .765), (-2.18, -2.28, .77), 1.36),
    "cabin": ((-.045, -.267, .716), (-1.8, 1.05, 2.65), 2.89),
}


def studio(scene):
    rig = bpy.data.collections["REVIEW_ONLY"]
    for name, (target, direction, width) in CAMERAS.items():
        cam = bpy.data.objects.new("R5-D / " + name, bpy.data.cameras.new("R5-D / " + name))
        rig.objects.link(cam)
        cam.location = Vector(target) + Vector(direction)
        cam.rotation_euler = (-Vector(direction)).to_track_quat("-Z", "Y").to_euler()
        cam.data.type = "ORTHO"
        cam.data.ortho_scale = width
    scene.camera = rig.objects["R5-D / pair"]
    scene.render.resolution_x, scene.render.resolution_y = 1360, 960
    scene.cycles.seed = 11
    scene.cycles.samples = 28
    scene.cycles.denoising_input_passes = "RGB_ALBEDO_NORMAL"
    scene.cycles.denoising_prefilter = "ACCURATE"
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type == "VIEW_3D":
                view = area.spaces.active.region_3d
                view.view_distance = 2.6
                view.view_location = CAMERAS["pair"][0]
                view.view_rotation = scene.camera.rotation_euler.to_quaternion()


def build(cabin, out):
    if out.exists() or out.suffix != ".blend":
        raise ValueError("Choose an unused .blend destination")
    if sha256(Path(bpy.data.filepath).read_bytes()).hexdigest() != APPROVED:
        raise ValueError("Open the approved R5-C-refined master")
    scene = bpy.context.scene
    pair = collection(PAIR, scene.collection)
    driver = bpy.data.collections[DRIVER]
    pair.children.link(driver)
    scene.collection.children.unlink(driver)
    driver["phase"] = "Owner-approved R5-C-refined driver"
    mirror_seat(driver, collection(PASSENGER, pair))
    add_context(json.loads(cabin.read_text()), scene)
    pair["driver_source_sha256"] = APPROVED
    pair["placement"] = "Provisional production stations. Floor mounts unresolved."
    studio(scene)
    bpy.context.view_layer.update()
    bpy.ops.wm.save_as_mainfile(filepath=str(out), compress=True)


if __name__ == "__main__":
    build(*(Path(arg).resolve() for arg in sys.argv[sys.argv.index("--") + 1:]))
