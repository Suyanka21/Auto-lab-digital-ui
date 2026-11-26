"""Fresh-open comparison against the frozen R5-C. Never save either file."""
from hashlib import sha256
import json
from pathlib import Path
import sys

import bpy
import numpy as np

sys.dont_write_bytecode = True
D = Path(__file__).resolve().parent
sys.path[:0] = [str(D), str(D.parent / "R5-C")]
from check import snapshot
from form import PANELS, grid, normals, read_co
from leather import FINISH
from refine import BASE_HASH, DRAW, DRAW_THREAD, HEAD, LUMBAR, PAN


def panel_faces():
    return {ob.name: sha256(np.array([l.vertex_index for l in ob.data.loops], "i4").tobytes()
                + np.array([p.loop_total for p in ob.data.polygons], "i4").tobytes()).hexdigest()
            for ob in bpy.data.collections[PANELS].objects}


def studio():
    scene = bpy.context.scene
    rig = bpy.data.collections["REVIEW_ONLY"]
    bg = scene.world.node_tree.nodes["Background"]
    return (scene.view_settings.view_transform, scene.view_settings.look, scene.view_settings.exposure,
            scene.view_settings.gamma, tuple(bg.inputs[0].default_value), bg.inputs[1].default_value,
            {o.name: (np.asarray(o.matrix_world).tolist(), o.data.lens) for o in rig.objects if o.type == "CAMERA"},
            {o.name: (np.asarray(o.matrix_world).tolist(), o.data.energy, o.data.size, tuple(o.data.color))
             for o in rig.objects if o.type == "LIGHT"})


def validate(base, out):
    if out.exists() or sha256(base.read_bytes()).hexdigest() != BASE_HASH:
        raise ValueError("Use the frozen R5-C and an unused report path")
    refined = Path(bpy.data.filepath)
    bpy.ops.wm.open_mainfile(filepath=str(base.resolve()))
    original, _, original_edges, original_bounds, _ = snapshot()
    faces, lights = panel_faces(), studio()
    foundation, _ = grid(bpy.data.objects[LUMBAR])
    bpy.ops.wm.open_mainfile(filepath=str(refined))
    geometry, _, edges, bounds, tris = snapshot()
    changed = sorted(n for n in original if original[n] != geometry[n])
    new = set(geometry) - set(original)
    ob = bpy.data.objects[LUMBAR]
    shaped, _ = grid(ob, shaped=True)
    amount = ((shaped-foundation)*normals(foundation)).sum(axis=-1)
    valleys = []
    for i in (1, 2, 3):
        row = amount[len(amount)*i//4]
        valleys.append(int(sum((row[1:-1] < -.003) & (row[1:-1] < row[:-2]) & (row[1:-1] < row[2:]))))
    key = ob.data.shape_keys.key_blocks[DRAW]
    assert key.value == 1
    thread = bpy.data.objects[DRAW_THREAD]
    for v in (0., .5, 1.):
        key.value = v
        bpy.context.view_layer.update()
        deps = bpy.context.evaluated_depsgraph_get()
        curve = thread.evaluated_get(deps).data
        assert abs(curve.bevel_depth - v*.00042) < 1e-8
        assert abs(curve.shape_keys.key_blocks["Fitted to draw"].value - v) < 1e-6
        actual = read_co(ob.evaluated_get(deps).data.vertices).reshape(shaped.shape)
        assert np.allclose(actual, (1-v)*foundation + v*shaped, rtol=0, atol=2e-7)
    materials = {slot.material for o in bpy.data.collections["R5_FRONT_SEAT_MASTER"].all_objects
                 for slot in o.material_slots}
    enabled = {}
    for mat in materials:
        node = mat.node_tree.nodes.get(FINISH) if mat.node_tree else None
        if node and node.inputs["Perforation"].default_value:
            enabled[mat.name] = node.inputs["Perforation"]
    assert set(enabled) == {"Cognac • " + n for n in ("Yoke", "Lumbar", "Waterfall")}
    for name, socket in enabled.items():
        socket.default_value = 0.
        assert all(s.default_value == float(n != name) for n, s in enabled.items())
        socket.default_value = 1.
    checks = {
        "same14PanelMeshesAndFaces": len(faces) == 14 and faces == panel_faces(),
        "fixedWorldSpaceCutEdges": original_edges == edges,
        "onlyIntendedLocalGeometryEdits": set(changed) == {HEAD, HEAD+" • topstitch", LUMBAR, PAN},
        "onlyNewGeometryIsFittedThread": new == {DRAW_THREAD, "Back • upper centre yoke • topstitch"}
            and all(bpy.data.objects[n].type == "CURVE" for n in new),
        "unchangedHeightAndFloorDatum": all(bounds[i][2] == original_bounds[i][2] for i in (0, 1)),
        "sameCamerasLightsAndColourManagement": lights == studio(),
        "fourValleysAtThreeLevels": valleys == [4, 4, 4],
        "originalPlainFoundationAndThreadsFollowDrawKey": True,
        "threeIndependentPunchSwitches": True,
    }
    report = {"passed": all(checks.values()), "checks": checks, "changedExistingGeometry": changed,
              "newObjects": sorted(new), "evaluatedTrianglesIncludingThread": tris,
              "geometryDigest": sha256(json.dumps(geometry, sort_keys=True).encode()).hexdigest(),
              "scope": "Digital master construction. Appearance awaits owner review."}
    out.write_text(json.dumps(report, indent=2) + "\n")
    if not report["passed"]:
        raise AssertionError(checks)
    print(report)


if __name__ == "__main__":
    validate(*(Path(s) for s in sys.argv[sys.argv.index("--")+1:]))
