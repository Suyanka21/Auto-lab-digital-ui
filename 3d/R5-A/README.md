# R5-A | Shared front-seat form

**For owner review — not approved.** One new driver-side master at the existing station; no old seat topology, passenger variant, upholstery construction, bake, GLB export or browser integration. [Open the editable master](R5-front-seat-master.blend) with Git LFS and Blender **5.2.2 LTS**. It includes the actual primary as a packed, disabled camera guide, never as a surface texture.

| What to inspect | Evidence |
|---|---|
| Primary design versus driver study | [Primary comparison](review/primary-comparison.webp) · [native three-quarter view](review/three-quarter.webp) |
| Shape without perspective or material cues | [Four-view sheet](review/form-inspection.webp) · [front](review/front.webp) · [outboard side](review/side.webp) · [rear](review/rear.webp) · [neutral](review/neutral.webp) |
| Same station in the shipped cockpit | [Comparison](review/placement-comparison.webp) · [before](review/cabin-existing.webp) · [study](review/cabin-r5-a.webp) · [placement measurements](review/placement.json) |
| What was corrected / what remains | [Visual assessment](INSPECTION.md) · [data audit](review/audit.json) · [local construction probes](review/form-checks.json) |

## Construction and evidence authority

The [seat primary](../../AUTOLAB_INTERIOR_3D_REFERENCE_PACK/03_FRONT_SEATS/PRIMARY/AUTOLAB_SUV_FRONT_SEAT_PRIMARY_01.jpg) controls silhouette and proportions. Read down from the broad shoulders: the separate, low-set trapezoid restraint; the backrest's forward return at the lumbar; the dished cushion flowing over a rounded nose; the shield rising into the rear pivot area; the open interval down to the runners. The [alternate](../../AUTOLAB_INTERIOR_3D_REFERENCE_PACK/03_FRONT_SEATS/ALTERNATES/AUTOLAB_SUV_FRONT_SEAT_ALTERNATE_02.jpg) clarifies post spacing and rail depth but its raised headrest and tag were not copied. The [cabin image](../../AUTOLAB_INTERIOR_3D_REFERENCE_PACK/00_MASTER_CABIN/PRIMARY/AUTOLAB_SUV_MASTER_CABIN_3Q_SIDE_VIEW_01.jpg) informs recline, rear cover and console adjacency. All are 2752 × 1536 design images with unknown camera calibration, not orthographic drawings. No branded imagery was applied to the seat.

`R5_FRONT_SEAT_MASTER` contains five collections: main foam, head restraint, carriers, handed shields/controls and mounting envelope. The studio, cameras and lights are outside the master. Most shapes are editable subdivision cages; runner channels and feet use beveled profiles. Only the coarse centre/surround zoning exists. The centre faces correspond to future `MAT_Seat_Primary`, surround and independent headrest to `MAT_Seat_Secondary`; future thread would map to `MAT_Seat_Stitching`. Plastic, control and metal studies are independent. No new live slots and no stitched or perforated geometry. Draft UVs are not a bake layout.

The build uses Blender metres and the shipped driver's lateral centre, **X = +0.425**; **−Y** is forward, **+X** outboard. The rig uses new *inspection* cameras, not new showroom presets. The [R4 benchmark](../handover/APPROVAL.md) remains frozen. The [seat technique note](../../.agents/skills/autolab-premium-cabin-modeling/references/seat-form-study.md) explains the transferable method and failure cases.

## Reproduce outside the repository

From the repository root with Git LFS hydrated, Blender 5.2.2 on `PATH`, Node 22 and the locked npm dependencies installed (`npm ci`), and Python with Pillow (tested 12.3.0). Commands below use Bash. Use an empty inspection directory: builders and review helpers deliberately refuse to overwrite previous evidence.

```bash
set -eu
D=3d/R5-A
H=.agents/skills/autolab-premium-cabin-modeling/scripts
W=$(mktemp -d)
M="$W/R5-front-seat-master.blend"
blender -b --factory-startup --python-exit-code 1 -P "$D/build.py" -- --out "$M"
blender -b "$M" --python-exit-code 1 -P "$H/audit_master.py" -- \
  --collection R5_FRONT_SEAT_MASTER --report "$W/audit.json"
blender -b "$M" --python-exit-code 1 -P "$D/form_checks.py" -- "$W/form-checks.json"
for view in three-quarter front side rear neutral; do
  cam=$view; flags=()
  if [ "$view" = neutral ]; then cam=three-quarter; flags=(--neutral); fi
  blender -b "$M" --python-exit-code 1 -P "$H/render_review.py" -- \
    --camera "CAM_$cam" --samples 32 --threads 2 --width 1040 --height 1040 \
    "${flags[@]}" --out "$W/$view.png"
done
node "$D/read-cabin.mjs" "$W/cabin.json"
blender -b "$M" -t 2 --python-exit-code 1 -P "$D/placement.py" -- "$W/cabin.json" "$W"
python3 "$D/sheets.py" "$W"
```

For the cabin comparison the existing runtime decoder dependencies read the **unchanged Classic GLB**. Only world-space vertices and triangles go into scratch JSON. The Blender importer does not support its required `KHR_texture_basisu`; no texture substitution or GLB rewrite is needed to compare form. The comparison script does not save the assembled scene.

Compare `evaluatedGeometryDigest` in the fresh probe report with the checked-in report. It covers evaluated coordinates, indices and face-material indices on this Blender build; it does not assume two separately serialized `.blend` files are byte-identical. For *retrieval*, check exact bytes from a fresh clone with `git lfs pull` and `sha256sum -c 3d/R5-A/SHA256SUMS` from repository root.

Published review images are compact WebP encodings of the original renders/sheets (Pillow, quality 93, method 6); raw PNG renders are reproducible with the commands above. The complete original review archive was supplied to the owner separately. No visual acceptance is implied by compression or integrity checks.
