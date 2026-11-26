# R6-B · Rear-bench upholstery

**Owner review pending.** Start with `sheets/primary.jpg` in the [review packet](R6-B-review.zip), then inspect the two native close-ups. See the [discrepancies and assembly limits](INSPECTION.md). The [editable master](R6-B-rear-bench.blend) is a Blender 5.2.2 LTS file, not a runtime asset.

## Construction

The [approved rear-bench primary](../../AUTOLAB_INTERIOR_3D_REFERENCE_PACK/04_REAR_BENCH/PRIMARY/AUTOLAB_SUV_REAR_BENCH_PRIMARY_01.jpg) governs the seams and padding. It is packed unchanged in the inspection camera's disabled background slot. The [R6-A form](../R6-A/README.md) supplies the positions and section cages. Only the leather materials and stitch technique come from the [approved front seat](../R5-C-refined/README.md); the rear yokes, three lengthwise pads and cushion patterns are new.

In the Outliner, expand **R6_REAR_BENCH_MASTER**:

| Change | Where |
| --- | --- |
| Edit a cover piece | **06 • Rear sewn panels**. Each outer back has 13 mesh pieces including boxing and returns; each of the three cushions has six. Neighbouring cut edges meet without welding. |
| Change colour or turn perforations off | On the chosen `Rear • LH/RH Yoke`, `Lumbar` or `Waterfall` material, edit its **Cognac finish** group inputs. These are six separate material instances. The three lumbar pads on one side share its lumbar material; make a single-user copy to change just one. |
| Edit the pattern | Punched pieces have physical-distance pattern UVs and an unpunched seam-margin attribute. Turning perforation off does not flatten the underlying sewn padding. Plain cheeks, centre saddle, armrest and headrests have no enabled punch. |
| Change or hide thread | **07 • Removable tonal stitching** contains separate curves using one tonal thread material. The armrest seam and pull follow the stowed leaf; there is no folding mechanism. |
| Change the cut or padding while retaining seam fit | Edit the back/cushion stations and loft in [tailor.py](tailor.py) and rebuild in a new destination. Use the hidden **CONSTRUCTION ONLY • approved R6-A cages** collection for comparison. The generated mesh boundaries and most thread curves do not automatically follow later freehand mesh edits. |

The centre front of each cushion is lowered locally rather than moving the base or any seat station. The original rails, feet, receivers, centre reveals and headrest positions are retained. The detailed master, studio and camera setup are separate from the showroom app. The cabin view appends the [approved front pair](../R5-D/README.md) and cockpit only in memory.

## Reproduce and retrieve

Run from repository root with Git LFS, Blender **5.2.2 LTS**, and Python with **Pillow 12.3.0** (lossless WebP enabled). Use an empty evidence directory. Blender's binary serialization is not the rebuild comparison: the verifier hashes evaluated coordinates and triangle indices, including thread geometry. Retrieval checks the exact published file bytes.

```bash
set -eu
B=blender
D=3d/R6-B
W=$(mktemp -d)
H=.agents/skills/autolab-premium-cabin-modeling/scripts
git lfs pull --include='3d/R6-B/*.blend,3d/R6-A/*.blend,3d/R5-C-refined/*.blend,3d/R5-D/*.blend' --exclude=''
sha256sum -c "$D/SHA256SUMS" 3d/R6-A/SHA256SUMS 3d/R5-C-refined/SHA256SUMS 3d/R5-D/SHA256SUMS
M="$W/R6-B-rear-bench.blend"
"$B" -b 3d/R6-A/R6-A-rear-bench.blend -t 2 --python-exit-code 1 -P "$D/tailor.py" -- "$M"
"$B" -b "$M" -t 2 --python-exit-code 1 -P "$D/verify.py" -- "$W/checks.json"
cmp "$D/checks.json" "$W/checks.json"
"$B" -b "$M" -t 2 --python-exit-code 1 -P "$H/audit_master.py" -- --collection R6_REAR_BENCH_MASTER --report "$W/audit.json"
"$B" -b "$M" -t 2 --python-exit-code 1 -P "$D/render.py" -- "$W/raw" three-quarter front backrest armrest cabin construction
python3 "$D/packet.py" build "$W/raw" "$W/audit.json" "$W/review.zip"
```

To test the **published** checkpoint independently, clone `devin/r5-a-front-seat-form` from GitHub into an empty directory with `GIT_LFS_SKIP_SMUDGE=1`; run the LFS pull and checksums above there. Set `M="$D/R6-B-rear-bench.blend"` and run the same fresh-open verifier and master audit without rebuilding. Run `python3 "$D/packet.py" verify "$D/R6-B-review.zip"` in the fresh checkout. Pass `--raw /path/to/original/pngs` to also compare the decoded pixels of all six native views. The two JPEG sheets are labelled, resized comparisons; judge the fine thread and perforation in the lossless WebPs.
