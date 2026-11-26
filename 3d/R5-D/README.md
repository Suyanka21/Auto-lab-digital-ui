# R5-D front-seat pair

The owner visually approved the [R5-C-refined driver](../R5-C-refined/SHA256SUMS) on 2026-11-26. Its slightly dark, regular perforation remains an accepted material observation. The [editable assembly](R5-D-front-seat-pair.blend) contains that driver's geometry and one handed passenger derivative. The [review packet](R5-D-review.zip) contains six native Cycles views, a pair and placement sheet, a labelled diagnostic, [inspection findings](INSPECTION.md), and the integrity reports.

## Editing the assembly

Expand **R5_D_FRONT_SEAT_PAIR** in the Outliner. The original driver group is **R5_FRONT_SEAT_MASTER** and the passenger group is **R5_D_PASSENGER**. Each contains 14 panel meshes, separate head restraint, controls, carriers, mounting components and seven thread curves. Passenger objects have the **P •** prefix. Both seats retain the modifier stacks and editable control geometry of the benchmark.

The passenger reflects across the cabin centre plane, X = 0. The builder reflects mesh and curve coordinates and both ends of each shape key, then reverses polygon winding and the associated face-corner UV ordering. Object frames retain positive determinant. The two seats share the leather shader groups and plain materials. The passenger has separate **Cognac • Yoke**, **Cognac • Lumbar** and **Cognac • Waterfall** material instances with the **P •** prefix. In each instance, edit **Perforation** on the **Editable region finish** node. The 4 mm staggered field and seam margins come from the approved master. Adjust **Drawn lumbar channels** on either seat's lumbar insert; only its own channel stitching follows.

Show **PLACEMENT ONLY • dashboard and console** in the viewport or enable its render toggle to inspect both seats in context. This collection holds the production dashboard and five console meshes in their original world coordinates, with a single slate study material. The visible studio ground is a render stand. There is no mounting floor datum beyond the provisional rail comparison.

## Reproduce

Run from repo root with Blender 5.2.2 LTS, Node 22 with the locked npm dependencies, and Python with Pillow 12.3.0 and WebP support. The cabin reader decodes the hash-checked production Classic GLB into scratch JSON. The builder opens the approved source, requires a fresh output path and saves a self-contained pair.

```bash
set -eu
D=3d/R5-D
B=blender
S=3d/R5-C-refined/R5-front-seat-refined.blend
H=.agents/skills/autolab-premium-cabin-modeling/scripts
W=$(mktemp -d)
M="$W/R5-D-front-seat-pair.blend"
git lfs pull --include='3d/R5-C-refined/*.blend,3d/R5-D/*.blend' --exclude=''
sha256sum -c 3d/R5-C-refined/SHA256SUMS "$D/SHA256SUMS"
npm ci
node 3d/R5-A/read-cabin.mjs "$W/cabin.json"
"$B" -b "$S" -t 2 --python-exit-code 1 -P "$D/pair.py" -- "$W/cabin.json" "$M"
"$B" -b "$M" -t 2 --python-exit-code 1 -P "$D/verify.py" -- "$S" "$W/cabin.json" "$W/checks.json"
cmp "$D/checks.json" "$W/checks.json"
"$B" -b "$M" -t 2 --python-exit-code 1 -P "$H/audit_master.py" -- --collection R5_D_FRONT_SEAT_PAIR --report "$W/audit.json"
"$B" -b "$M" -t 2 --python-exit-code 1 -P "$D/render.py" -- "$W/raw" pair front rear passenger diagnostic cabin
python3 "$D/packet.py" "$W/raw" "$W/audit.json" "$W/checks.json" "$D/INSPECTION.md" "$W/R5-D-review.zip"
```

The six fixed cameras use the original three studio lights, AgX Medium High Contrast and CPU Cycles at 28 maximum samples, seed 11 and albedo/normal-guided denoising. The passenger detail and diagnostic are 1100 pixels square. The pair and placement views are 1360 × 960. All six WebPs preserve the original PNG RGB pixels. The sheets resize the views and add captions outside them.

## Verify a download

Clone `devin/r5-a-front-seat-form` into a new directory. Run the Git LFS pull and manifest verification above. Run the same verifier against the downloaded master by setting `M="$D/R5-D-front-seat-pair.blend"` and compare the fresh report to [the recorded checks](checks.json). Unzip the packet into a new directory and run `sha256sum -c SHA256SUMS` there to verify each member.
