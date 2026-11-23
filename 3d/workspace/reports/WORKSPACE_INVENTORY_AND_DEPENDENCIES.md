# Initial workspace inventory and dependencies
2026-11-18. Workspace: C:/Users/user/Documents/AUTOLAB_3D_WORKSPACE.

## Remote state verified
- New repository main: 0b91e7331ef67178b47cbc4dd799cfc6fed71e56.
- Original repository main: b5338d324275ca473349e68194be3ac943ba7687.
- New PRs 1-5 merged. PR6 open, head ba211706377cfaa4c27b6b1265bd096e86ba722e; candidate assets NOT adopted.
- Original PR6 is a different, merged live stitch-study UI change. PR numbers must remain repository-qualified.
- GitHub CLI unavailable; direct GitHub API/raw access succeeded. No clone or repository history downloaded.

## Selected inventory
137 remote source/reference files, 25,933,050 bytes, before local reports/contact sheet. Exact paths, pins, bytes and SHA256: download-inventory.json. Initial 124 downloads were also verified against Git blob hashes.
Includes three shipped GLBs; three fa3d62a historical input GLBs; six Blender modules and craft_kit; preparation/finalization scripts; current validator/comparison scripts; current manifests/material/camera/runtime contracts; all 35 gallery JPEGs; reference-library Markdown/CSV/JSON including second-round research; roadmap/reconciliation documents; PR6 report and code only.
Excluded app shell/components, npm dependencies, build output, deployment configuration, full history, old .blend outputs, duplicate reference images, brochures/PDF binaries and PR6 candidates. Viewer source is reference-only; it cannot run as an application here.

## Tool probes (actual)
- Blender executable: C:/Program Files/Blender Foundation/Blender 5.2/blender.exe.
- Headless bpy PASS: Blender 5.2.2 LTS, hash d13f752e3b9c, NumPy 2.3.4, background=true.
- toktx executable: C:/Program Files/KTX-Software/bin/toktx.exe; version 4.4.2.
- Node v22.23.2; Python 3.12.6. Pillow generated an internal contact sheet.
- No expensive geometry build, render or bake performed; no hardware GPU performance claim.

## Recovered chain and dependencies
prepare-front-cabin.mjs -> build_front_cabin.py -> finalize-front-cabin.mjs.
Preparation originally uses git show fa3d62a; the three exact historical inputs are now local so a safe adapter can read files without any Git checkout. Blender imports front_cabin_constants, front_cabin_carbon, cockpit_surfaces, lexus_l2b_cockpit, lexus_l2b_constants and craft_kit; these modules are present. ROOT/OUT paths must be isolated before execution.
Finalization uses @gltf-transform/core/extensions 4.5.1, draco3dgltf 1.5.9, gltf-validator 2.0.0-dev.3.10 and ajv 8.20.0. No node_modules was downloaded or installed, respecting the brief. The archived gate expects repository-relative manifests/schema/package files; it is NOT yet runnable as an independent gate. A minimal dependency runtime and path adaptation remain necessary before any compressed candidate is accepted. Existing reports of gate PASS are historical, not new executions here.
Finalizer currently copies into public/assets/3d. It is quarantined source: replace promotion with exports/candidates-only output and hash guards before running. Do not blindly replay the old report's full-repository archive/npm-ci commands.

## Safety and next work
Baseline headers/hash/material metadata checked by inspect_baseline.py; see baseline-inspection.json. This is NOT Draco decode or Khronos validation. No production files were edited. Generated candidates must have separate names and a candidate manifest; the old exact-node gate will correctly reject a full cabin until an explicit candidate scope is added.
For future transfer, GitHub Git Data API can publish selected files without a full clone, subject to authenticated write access (not tested today). Use a separate branch/PR; no production replacement, automatic merge or reference-photo redistribution.
