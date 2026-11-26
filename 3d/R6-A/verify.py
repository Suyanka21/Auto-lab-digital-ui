"""Check evaluated bench forms and static placement from a fresh Blender open."""
from hashlib import sha256
import itertools
import json
from pathlib import Path
import sys

import bpy
import numpy as np

sys.dont_write_bytecode = True
D = Path(__file__).resolve().parent
sys.path.insert(0, str(D))
from bench import CENTER, PRIMARY, ROOT
from review import PAIR_HASH, context

# Use R5-D's evaluated world-space triangulation, including modifiers.
import importlib.util
sys.path.insert(0, str(D.parent / "R5-D"))
spec = importlib.util.spec_from_file_location("pair_checks", D.parent / "R5-D/verify.py")
pair_checks = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pair_checks)
bounds, surface = pair_checks.bounds, pair_checks.surface


def run(out):
    if out.exists():
        raise FileExistsError(out)
    ref = bpy.data.images[PRIMARY.name]
    assert ref.packed_file and bytes(ref.packed_file.data) == PRIMARY.read_bytes()
    bench = bpy.data.collections[ROOT]
    assert len(bench.children) == 5 and all(o.type == "MESH" for o in bench.all_objects)
    pair, cabin = context()
    deps = bpy.context.evaluated_depsgraph_get()
    parts = {o.name: surface(o, deps) for o in bench.all_objects}
    box = {n: bounds(points) for n, (points, _) in parts.items()}
    extent = bounds(np.concatenate(list(box.values())))
    dims = lambda name: box[name][1] - box[name][0]
    def touch(a, b):
        return bool(parts[a][1].overlap(parts[b][1]))

    # Outer foam envelopes reflect across the cabin centreline.
    for stem in ("Headrest", "Backrest", "Cushion", "Pivot cover"):
        left, right = box[stem+" • LH"], box[stem+" • RH"]
        np.testing.assert_allclose(left[:,0], -right[::-1,0], atol=1e-5)
        np.testing.assert_allclose(left[:,1:], right[:,1:], atol=1e-5)
    for tag, station in (("LH",-CENTER), ("centre",0), ("RH",CENTER)):
        head, cushion = "Headrest • "+tag, "Cushion • "+tag
        assert abs(box[head][:,0].mean()-station) < .001
        assert abs(box[cushion][:,0].mean()-station) < .001
        for side in "ab":
            post, guide = "Post • "+tag+" "+side, "Guide • "+tag+" "+side
            assert touch(head,post) and touch(guide,post)
        back = "Centre • lower bolster" if tag=="centre" else "Backrest • "+tag
        assert touch(cushion,back)
        if tag != "centre":
            for name in (back,cushion):
                assert {p.material_index for p in bench.all_objects[name].data.polygons} == {0,1}
    outer = dims("Cushion • LH")
    middle = dims("Cushion • centre")
    assert .5 < middle[0]/outer[0] < .7
    assert .40 < outer[1] < .55 and .10 < outer[2] < .20
    drop = box["Headrest • LH"][1,2] - box["Headrest • centre"][1,2]
    assert .04 < drop < .13
    for stem in ("Cushion","Headrest"):
        across = [box[stem+" • "+tag] for tag in ("LH","centre","RH")]
        assert all(a[1,0] < b[0,0] for a,b in itertools.pairwise(across))

    leaf = "Centre • stowed armrest"
    assert bench.all_objects["Centre • armrest pull"].parent == bench.all_objects[leaf]
    assert "Stowed" in bench.all_objects[leaf]["pose"]
    assert box["Cushion • centre"][1,2] < box[leaf][0,2] < box[leaf][1,2] < box["Headrest • centre"][0,2]
    assert set(n for n in parts if n != leaf and touch(leaf,n)) == {"Centre • armrest pull"}
    for i in range(1,4):
        release, receiver = f"Release • {i}", f"Receiver • {i}"
        assert set(n for n in parts if n != release and touch(release,n)) == {receiver}
        assert box[release][1,2] > box[receiver][1,2]
    for i in range(1,5):
        plinth = "Plinth • " + ("narrow" if i < 3 else "wide")
        assert touch(f"Foot • {i}",plinth)
    for side in ("narrow","wide"):
        assert touch("Rear load face • "+side, "Plinth • "+side)
    assert box["Rear load face • narrow"][1,0] < box["Rear load face • wide"][0,0]

    # Disjoint longitudinal envelopes prove separation of every included
    # triangle. These are static axis gaps, not distances to occupant knees.
    gaps = {}
    for coll in (*pair.children,cabin):
        context_box = bounds(np.concatenate([bounds(surface(o,deps)[0]) for o in coll.all_objects]))
        gap = float(extent[0,1] - context_box[1,1])
        assert gap > 0, (coll.name, gap)
        gaps[coll.name] = round(gap*1000, 2)
    mm = lambda a: (np.asarray(a)*1000).round(2).tolist()
    report = {
        "approvedPairSHA256": PAIR_HASH, "benchMeshes": len(parts),
        "benchBoundsM": extent.round(6).tolist(), "outerCushionWidthDepthHeightMM": mm(outer),
        "centreCushionWidthDepthHeightMM": mm(middle), "armrestWidthMM": mm(dims(leaf)[0]),
        "centreHeadrestTopDropMM": mm(drop), "foreAftEnvelopeGapMM": gaps,
        "visibleReleaseFacesClearOfFoam": 3, "feetMeetingSplitBase": 4,
        "scope": "Static model space. Studio floor, installed fit, occupant clearance and folding travel are unverified.",
        "passed": True,
    }
    out.write_text(json.dumps(report,indent=2)+"\n")
    print(report)


if __name__ == "__main__":
    run(Path(sys.argv[sys.argv.index("--")+1]))
