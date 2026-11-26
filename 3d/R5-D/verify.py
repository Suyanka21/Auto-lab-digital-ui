"""Fresh-open mirror, independent state, and static placement checks in Blender."""
from hashlib import sha256
import json
from pathlib import Path
import sys

import bpy
import numpy as np
from mathutils.bvhtree import BVHTree

sys.dont_write_bytecode = True
D = Path(__file__).resolve().parent
sys.path[:0] = [str(D), str(D.parent / "R5-C")]
from pair import APPROVED, CABIN, CONTEXT, CONTEXT_NAMES, DRIVER, INSERTS, PASSENGER, PREFIX
from check import snapshot
from leather import FINISH, MARGIN

FLIP = np.array([-1., 1., 1.])
LUMBAR = "Back • drawn lumbar insert"
THREAD = "Lumbar • channel topstitch"


def values(items, field, width=1, dtype=np.float32):
    result = np.empty(len(items) * width, dtype=dtype)
    items.foreach_get(field, result)
    return result.reshape(len(items), width)


def check_mesh(a, b):
    assert np.array_equal(values(a.vertices, "co", 3) * FLIP, values(b.vertices, "co", 3))
    # Blender's flip_normals keeps each face's first corner, then reverses the rest.
    take = [loop for p in a.polygons for loop in (p.loop_start, *list(p.loop_indices)[1:][::-1])]
    assert np.array_equal(values(a.loops, "vertex_index", dtype="i")[take],
                          values(b.loops, "vertex_index", dtype="i"))
    assert np.array_equal(values(a.polygons, "material_index", dtype="i"), values(b.polygons, "material_index", dtype="i"))
    np.testing.assert_allclose(values(a.polygons, "normal", 3) * FLIP, values(b.polygons, "normal", 3), atol=2e-4)
    assert a.uv_layers.keys() == b.uv_layers.keys()
    for uv in a.uv_layers:
        assert np.array_equal(values(uv.data, "uv", 2)[take], values(b.uv_layers[uv.name].data, "uv", 2))
    if MARGIN in a.attributes:
        assert np.array_equal(values(a.attributes[MARGIN].data, "value"), values(b.attributes[MARGIN].data, "value"))


def check_mirror():
    driver = bpy.data.collections[DRIVER]
    passenger = bpy.data.collections[PASSENGER]
    assert {PREFIX + o.name for o in driver.all_objects} == set(passenger.all_objects.keys())
    panels = threads = 0
    reflect = np.diag([-1., 1., 1., 1.])
    for a in driver.all_objects:
        b = passenger.all_objects[PREFIX + a.name]
        assert a.type == b.type and a.data != b.data and b.matrix_world.determinant() > 0
        np.testing.assert_allclose(np.array(b.matrix_world), reflect @ a.matrix_world @ reflect, atol=1e-7)
        assert [m.type for m in a.modifiers] == [m.type for m in b.modifiers]
        assert [slot.material.name for slot in a.material_slots] == [
            slot.material.name.removeprefix(PREFIX) for slot in b.material_slots]
        if a.type == "MESH":
            check_mesh(a.data, b.data)
            panels += int(bool(a.get("editable_region")))
        else:
            assert b.type == "CURVE" and b["fitted_to"] == PREFIX + a["fitted_to"]
            assert len(a.data.splines) == len(b.data.splines)
            for s, t in zip(a.data.splines, b.data.splines):
                np.testing.assert_allclose(values(s.points, "co", 4) * [-1, 1, 1, 1],
                                           values(t.points, "co", 4), atol=1e-7)
                np.testing.assert_allclose(values(s.points, "radius"), values(t.points, "radius"), atol=1e-7)
            threads += 1
        if a.data.shape_keys:
            assert a.data.shape_keys != b.data.shape_keys
            for key in a.data.shape_keys.key_blocks:
                other = b.data.shape_keys.key_blocks[key.name]
                np.testing.assert_allclose(values(key.data, "co", 3) * FLIP, values(other.data, "co", 3), atol=1e-7)
    assert (panels, threads) == (14, 7)
    return {"componentsPerSeat": len(driver.all_objects), "panelsPerSeat": panels, "threadObjectsPerSeat": threads}


def check_controls():
    sockets = []
    for prefix, collection in (("", DRIVER), (PREFIX, PASSENGER)):
        for panel, material in zip(("Back • upper centre yoke", LUMBAR, "Cushion • centre waterfall"), INSERTS):
            assigned = bpy.data.objects[prefix + panel].data.materials[0]
            assert assigned.name == prefix + material
            node = assigned.node_tree.nodes[FINISH]
            assert abs(node.inputs["Pitch (m)"].default_value - .004) < 1e-8
            sockets.append(node.inputs["Perforation"])
        for ob in bpy.data.collections[collection].all_objects:
            for slot in ob.material_slots:
                mat = slot.material
                node = mat.node_tree.nodes.get(FINISH) if mat.node_tree else None
                if node and node.inputs["Perforation"].default_value:
                    assert mat.name in {prefix + name for name in INSERTS}
    for i, socket in enumerate(sockets):
        assert socket.default_value == 1.
        socket.default_value = 0.
        assert [s.default_value for s in sockets] == [float(i != j) for j in range(6)]
        socket.default_value = 1.
    for d, p in ((1, 0), (0, .5), (.5, 1), (1, 1)):
        for prefix, v in (("", d), (PREFIX, p)):
            bpy.data.objects[prefix + LUMBAR].data.shape_keys.key_blocks["Drawn lumbar channels"].value = v
        bpy.context.view_layer.update()
        dg = bpy.context.evaluated_depsgraph_get()
        for prefix, v in (("", d), (PREFIX, p)):
            curve = bpy.data.objects[prefix + THREAD].evaluated_get(dg).data
            assert abs(curve.bevel_depth - .00042 * v) < 1e-8
            assert abs(curve.shape_keys.key_blocks["Fitted to draw"].value - v) < 1e-6


def surface(obj, deps):
    ev = obj.evaluated_get(deps)
    mesh = ev.to_mesh()
    try:
        mesh.calc_loop_triangles()
        m = np.asarray(ev.matrix_world)
        pts = values(mesh.vertices, "co", 3) @ m[:3, :3].T + m[:3, 3]
        faces = values(mesh.loop_triangles, "vertices", 3, "i")
        return pts, BVHTree.FromPolygons(pts, faces, all_triangles=True)
    finally:
        ev.to_mesh_clear()


def bounds(points):
    return np.stack([points.min(axis=0), points.max(axis=0)])


def placement(decoded):
    refs = bpy.data.collections[CONTEXT]
    assert decoded["hash"] == refs["production_glb_sha256"] == CABIN
    assert set(refs.objects.keys()) == CONTEXT_NAMES
    refs.hide_viewport = False
    bpy.context.view_layer.update()
    deps = bpy.context.evaluated_depsgraph_get()
    nodes = {n["name"]: n for n in decoded["nodes"]}
    reference = {}
    for o in refs.objects:
        pts, tree = surface(o, deps)
        n = nodes[o.name]
        np.testing.assert_allclose(pts, n["vertices"], atol=1e-7)
        assert np.array_equal(values(o.data.loops, "vertex_index", dtype="i").ravel(), np.ravel(n["faces"]))
        reference[o.name] = (bounds(pts), tree)

    stations, boxes, floor_delta, gaps = {}, {}, {}, {}
    for role, collection, prefix, sign in (("Driver", DRIVER, "", 1), ("Passenger", PASSENGER, PREFIX, -1)):
        old = bounds(np.asarray(nodes["GEO_Seat_Front_" + role]["vertices"]))
        station = old.mean(axis=0)[0]
        parts = {}
        for o in bpy.data.collections[collection].all_objects:
            pts, tree = surface(o, deps)
            parts[o.name.removeprefix(prefix)] = bounds(pts)
            for name, (box, target) in reference.items():
                assert not tree.overlap(target), (o.name, name)
                # Nearest evaluated seat vertex to any reference triangle. A
                # sampled distance, not an exact triangle clearance or travel test.
                key = role + (" dashboard" if name.startswith("GEO_Dashboard") else " console")
                best = gaps.get(key, 1.)
                mask = np.all((pts >= box[0] - best) & (pts <= box[1] + best), axis=1)
                for point in pts[mask]:
                    _, _, _, dist = target.find_nearest(point, best)
                    if dist is not None:
                        best = min(best, dist)
                gaps[key] = best
        extent = bounds(np.concatenate(list(parts.values())))
        # Entire outboard carrier and all three controls must clear the seat centre.
        for name in ("Shield • outboard control carrier", "Lumbar dial", "Position paddle", "Recline paddle"):
            assert np.all(sign * (parts[name][:, 0] - station) > 0)
        assert np.all(sign * (parts["Shield • inboard plain"][:, 0] - station) < 0)
        for side in ("outboard", "inboard"):
            assert parts["Foot • " + side + " front"][1, 1] < parts["Foot • " + side + " rear"][0, 1]
        origin = bpy.data.objects[prefix + LUMBAR].matrix_world.translation.x
        assert abs(origin - station) < .0001
        stations[role] = round(station, 5)
        boxes[role] = extent.astype(float).round(6).tolist()
        floor_delta[role] = round(1000 * (extent[0, 2] - old[0, 2]), 2)
    a, b = np.array(boxes["Driver"]), np.array(boxes["Passenger"])
    np.testing.assert_allclose(a[:, 1:], b[:, 1:], atol=2e-6)
    mid_gap = a[0, 0] - b[1, 0]
    assert mid_gap > 0 and all(abs(v + 66) < .1 for v in floor_delta.values())
    return {"productionCentresXMetres": stations, "pairBoundsMetres": boxes,
            "betweenSeatEnvelopeGapMM": round(1000 * mid_gap, 2), "mountVsProductionMM": floor_delta,
            "sampledSeatVertexToReferenceSurfaceMM": {k: round(1000 * v, 2) for k, v in sorted(gaps.items())},
            "staticIntersectionsWithDashboardOrConsole": [],
            "scope": "Static pose only. Floor anchorage, adjustment travel and installed fit remain unverified."}


def check(source, cabin, out):
    if out.exists() or sha256(source.read_bytes()).hexdigest() != APPROVED:
        raise ValueError("Use the approved driver and an unused report path")
    pair_path = bpy.data.filepath
    bpy.ops.wm.open_mainfile(filepath=str(source))
    approved = snapshot()[0]
    bpy.ops.wm.open_mainfile(filepath=pair_path)
    assert snapshot()[0] == approved, "Driver differs from approved evaluated geometry"
    result = {"approvedDriverSHA256": APPROVED, **check_mirror()}
    check_controls()
    result.update(placement(json.loads(cabin.read_text())))
    result["passed"] = True
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(result)


if __name__ == "__main__":
    check(*(Path(arg).resolve() for arg in sys.argv[sys.argv.index("--") + 1:]))
