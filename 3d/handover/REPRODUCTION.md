# Reproduction and review commands

Run from the repository root after `git lfs pull`. Use a verified Blender 5.2.2 LTS executable. Commands below use POSIX shell notation for Devin; on Windows substitute the actual quoted executable and Python path. Never run archived build/finalize scripts against production directories.

## Inspect the frozen master without changing it

```sh
blender -b 3d/workspace/working_models/R4-front-door-refined.blend --python-exit-code 1 --python .agents/skills/autolab-premium-cabin-modeling/scripts/audit_master.py -- --collection R4_FRONT_DOOR_MASTER --report /tmp/r4-audit.json
blender -b 3d/workspace/working_models/R4-front-door-refined.blend --python-exit-code 1 --python .agents/skills/autolab-premium-cabin-modeling/scripts/render_review.py -- --camera CAM_front-reference --out /tmp/r4-front.png --samples 64 --width 1440 --height 804
python3 .agents/skills/autolab-premium-cabin-modeling/scripts/compose_comparison.py AUTOLAB_INTERIOR_3D_REFERENCE_PACK/01_FRONT_DOOR_PANELS/PRIMARY/AUTOLAB_SUV_FRONT_DOOR_PANEL_PRIMARY_01.jpg /tmp/r4-front.png --out /tmp/r4-comparison.jpg
```

Other cameras: `CAM_three-quarter`, `CAM_handle-release-closeup`, `CAM_pocket-speaker-closeup`, `CAM_release-trim-closeup`, `CAM_neutral-geometry`, `CAM_realistic-material`. Use 1440x1000 for these; 96 samples for close-ups. Add `--neutral` to the portable renderer for clay inspection; that camera name alone does not override materials. No command above saves the Blender file.

## Rebuild from original first-party scripts

The inventory deduplicates bytes while preserving original path mappings. Restore all essential aliases into a **new empty scratch directory outside the repository**:

```sh
REPO="$PWD"
python3 3d/handover/scripts/workspace_transfer.py --restore /tmp/autolab-r4-rebuild --report /tmp/restore-check.json
cd /tmp/autolab-r4-rebuild
blender -b --python-exit-code 1 --python build_pipeline/isolated/build_front_door_r4.py
blender -b --python-exit-code 1 --python build_pipeline/isolated/refine_front_door_r4.py
blender -b --python-exit-code 1 --python build_pipeline/isolated/audit_front_door_refined.py
```

The original script creates the base master; the refinement opens it and imports only its function definitions. Rebuilding overwrites scratch masters only. The expected structural results are 48 meshes / 925,924 evaluated triangles for original R4 and 48 / 719,424 for refined. Newly saved .blend bytes may differ because of embedded paths or save metadata; they do not replace the frozen approved file/hash.

From scratch, the archived renderer can reproduce all final views:

```sh
blender -b --python-exit-code 1 --python build_pipeline/isolated/render_front_door_refined.py -- final front-reference three-quarter handle-release-closeup pocket-speaker-closeup release-trim-closeup neutral-geometry realistic-material material-lab
```

It retains historical overwrite behaviour, so use scratch only. Its raw `samples` field reflects the last view; actual close-ups use 96, overviews/lab 64. The published final manifest records per-view settings and the original interrupted/resumed batches.

Historical `package_front_door*.py` expects Windows Arial and every old preservation-snapshot file, including omitted intermediates; it is **not the portable handover entrypoint**. Use the new portable comparison helper, provided final sheets and frozen reports. Restored R4 HTML galleries have their relative assets; old broader reports can refer to unavailable runtime intermediates and are retained as history.

## Test helper failure behaviour

```sh
blender -b --python-exit-code 1 --python 3d/handover/tests/test_master_audit.py -- /tmp/helper-tests.json
```

This creates disposable cubes in memory. A valid mesh passes; missing UV/material, empty and absent collections fail. Low-sample smoke renders demonstrate script execution only, not visual quality. Existing final 64/96-sample renders remain the review evidence.

## Later runtime work

R4 has no runtime GLB. Do not run the quarantined original finalizers, some of which copy to `public/assets/3d`. Re-read current runtime contracts, author candidate-only output paths, preserve source hashes and test a separately approved optimisation/baking/export process. No KTX2/browser/device equivalence is claimed by this master reproduction.
