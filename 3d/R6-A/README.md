# R6-A rear-bench form

Open [the editable bench](R6-A-rear-bench.blend) in Blender 5.2.2 LTS. Expand **R6_REAR_BENCH_MASTER** for the three positions, centre back and armrest, head restraints, split base and receivers. The visible shapes use editable section cages with live subdivision or bevels. The outer cushions and backrests have separate face assignments for centre and surrounding upholstery. Headrests, armrest, load faces, structural graphite, metal and buckle releases have their own materials. R6-A uses plain form materials. Stitch courses, perforation and final panel tailoring await form approval.

The centre armrest is stowed. Its pull is parented to the leaf, whose local X axis passes through the lower end. The two rear load faces divide beside the centre section. The master represents the visible split and attachment regions in the static pose. Anchorage, folding trajectories and latch hardware are unresolved.

## References and placement

The [rear-bench primary](../../AUTOLAB_INTERIOR_3D_REFERENCE_PACK/04_REAR_BENCH/PRIMARY/AUTOLAB_SUV_REAR_BENCH_PRIMARY_01.jpg) governs the outer shoulders, broad cushions, headrest arrangement and stowed armrest. A copy is packed in the three-quarter camera's disabled background slot. The [alternate](../../AUTOLAB_INTERIOR_3D_REFERENCE_PACK/04_REAR_BENCH/ALTERNATES/) informed side depth. The [master cabin references](../../AUTOLAB_INTERIOR_3D_REFERENCE_PACK/00_MASTER_CABIN/) informed row spacing and seat-height relationships. Dimensions are inferred in metres with X lateral, −Y forward and Z up.

The cabin render and verifier load the two front seats, dashboard and console from the hash-checked [approved R5-D master](../R5-D/README.md) in memory. To inspect this context interactively, open the R6-A master and run the following in Blender's Python Console from a repo checkout with the R5-D LFS file retrieved.

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(bpy.data.filepath).parent))
from review import context
context()
bpy.context.scene.camera = bpy.data.objects["R6 / cabin"]
```

## Reproduce the checkpoint

Run from repo root. Use Blender 5.2.2 LTS and Python with Pillow 12.3.0 and WebP support.

```bash
set -eu
D=3d/R6-A
W=$(mktemp -d)
B=blender
H=.agents/skills/autolab-premium-cabin-modeling/scripts
M="$W/R6-A-rear-bench.blend"
git lfs pull --include='3d/R6-A/*.blend,3d/R5-D/*.blend,3d/R5-C-refined/*.blend' --exclude=''
sha256sum -c "$D/SHA256SUMS" 3d/R5-D/SHA256SUMS 3d/R5-C-refined/SHA256SUMS
"$B" -b --factory-startup -t 2 --python-exit-code 1 -P "$D/bench.py" -- "$M"
"$B" -b "$M" -t 2 --python-exit-code 1 -P "$D/verify.py" -- "$W/checks.json"
cmp "$D/checks.json" "$W/checks.json"
"$B" -b "$M" -t 2 --python-exit-code 1 -P "$H/audit_master.py" -- --collection R6_REAR_BENCH_MASTER --report "$W/audit.json"
"$B" -b "$M" -t 2 --python-exit-code 1 -P "$D/review.py" -- "$W/raw" front three-quarter side rear cabin
python3 "$D/packet.py" "$W/raw" "$W/audit.json" "$W/review.zip"
```

For independent retrieval, clone branch `devin/r5-a-front-seat-form` into a fresh directory with `GIT_LFS_SKIP_SMUDGE=1`. Run the LFS pull and checksums above, then run the verifier and audit on the retrieved master by setting `M="$D/R6-A-rear-bench.blend"`. Extract [the review packet](R6-A-review.zip) into an empty directory and run `sha256sum -c SHA256SUMS` there. Five lossless WebPs preserve the native 1400 × 960 RGB renders. The two labelled JPEG sheets contain resized copies for comparison.
