# Reference-led door milestone — R2
2026-11-19. Local construction checkpoint; full cabin NOT complete; no visual acceptance granted.

## Updated direction
Build a recognisable, convincing, customisable premium five-seat SUV for AutoLab. The approved AI pack defines visible design; the older Lexus gallery is contextual only. Manufacturer dimensions, switch replication and hidden mechanisms are not targets. Bright white showroom is a later viewer requirement, not cabin geometry.

## Reference retrieval
All 16 JPEGs and three documentation files retrieved only from `AUTOLAB_INTERIOR_3D_REFERENCE_PACK/` at commit `0e68d56c8863b5890fdcd580e570a2910edeaf38`, branch `chore/organise-autolab-interior-references`.
Location: `references/approved_ai_design/`; directory hierarchy and filenames retained. All images opened for the contact sheet; both door primaries inspected enlarged. Alternates inspected on the contact sheet for supplementary depth only. No primary replaced by an alternate.
All 16 downloads match pinned Git blob SHA1 values; all 16 sizes match the ledger. **14 manifest SHA256 entries do not match actual file hashes**; only the two rear-door entries match. Actual and claimed SHA256 values are recorded in `reports/approved-ai-reference-retrieval.json`. The upstream manifest is preserved unchanged. This is a manifest discrepancy, not a fabricated verification pass.

Door design sources:
- `01_FRONT_DOOR_PANELS/PRIMARY/AUTOLAB_SUV_FRONT_DOOR_PANEL_PRIMARY_01.jpg`
- `02_REAR_DOOR_PANELS/PRIMARY/AUTOLAB_SUV_REAR_DOOR_PANEL_PRIMARY_01.jpg`
- Corresponding `ALTERNATES/` images used only for armrest/pocket depth interpretation.

## Local state and preservation
Confirmed prior rear milestone: 70,568 triangles / 21 primitives. Prior door export: 73,484 triangles / 22 primitives; failed four tangent requirements. All earlier GLBs, Blender sources, scripts and reports retained. New files use R2 names. Production SHA256 checks pass after export and regression testing. No application execution, application edits, dependency-tree clone, push, merge or PR6 promotion.

## Tangent failure and correction
Preserved failed asset lacks tangents for MAT_Dashboard_Trim, MAT_Seat_Secondary, MAT_Seat_Primary and MAT_Console_Carbon. Focused Blender regression reproduced `Tangent space can only be computed for tris/quads` on a mesh containing eight n-gons. Explicit triangulation followed by `calc_tangents` succeeds. Vertex positions and UV corner pairs remain unchanged in the regression; 21,864 tangent loops computed. Custom-normal preservation is requested on the triangulation modifier. Baseline attributes are not edited; do not interpret this as bit-exact post-Draco normals.
The final R2 GLBs pass the candidate contract, including tangent presence on every normal-mapped primitive, UVs, finite attributes, indexed triangles, material contracts, envelope and budgets. Khronos reports zero errors; inherited KTX2 support warnings remain. Draco is independently decoded by glTF Transform. This is an offline candidate gate, not the original unmodified production node-manifest gate or browser validation.

## Candidate statistics
| Treatment | Triangles | Primitives* | Materials | Bytes | Structural result |
|---|---:|---:|---:|---:|---|
| Classic | 78,028 | 22 | 10 | 4,086,128 | PASS |
| Diamond | 78,028 | 22 | 10 | 4,222,592 | PASS |
| Perforated | 78,028 | 22 | 10 | 3,945,128 | PASS |

*Primitive count is a draw-call proxy, not GPU-measured renderer statistics. Limits remain 80,000 triangles, 24 primitives and 5,242,880 bytes. Remaining triangle headroom: **1,972**. No limit was relaxed. The geometry census before export is 78,272 triangles; exported/decoded files contain 78,028. Use decoded counts for delivery statistics.

## Visual changes
- Replaced rectangular shell blocks with shaped panel outlines; rear doors have a distinct tapered wheel-arch edge.
- Added padded upper sections, bounded middle upholstery and a separate decorative insert/frame.
- Added substantial curved upholstered grab handles and broad armrests.
- Built storage floors, lips and ends as an open pocket rather than a solid block.
- Added speaker rims/grille ribs; driver has four window switches, other doors one.
- Preserved all ten material names and the seven existing live bindings.

## Honest visual assessment
Technical PASS is not visual approval. The new doors are recognisable coordinated construction models, but still below the polished reference: broad panels are too flat, trim surrounds are heavy, speaker rings/ribs are faceted and schematic, padding transitions and stitching are incomplete. The rear bench remains the earlier coarse foundation, not the new 60/40 reference design. Existing dashboard/front-seat defects remain.
The first texture preview is dark/metallic-looking and does not demonstrate finished leather. A review-only missing vertex-colour fallback correction was tested but did not resolve the full appearance discrepancy. `*-material-regions.png` explicitly overrides base colours to reveal upholstery/trim/plastic zoning; these are diagnostic images, NOT proof of final material fidelity or browser appearance. No such override was written into the GLBs. Context render shows the assembled frame/floor/seating/doors. Comparison sheet uses diagnostic renders, labelled accordingly.

## Integration limitations and next work
Door upholstery currently uses MAT_Seat_Secondary: independent from trim/plastic, but linked to seat-secondary colour in the existing runtime. Dedicated independent door colour needs an approved material/control extension later. No unsupported claim of independently working door UI.
Before further detail, recover triangle headroom from low-value grille/trim subdivisions and measure the revised export; do not silently exceed limits. Pillars, roof/headliner, rear vents and cockpit corrections remain. Keep component source objects separate for editing; exported expansion is batched by material.
Prepare headliner geometry as a separately addressable component and starlight placement data around the roof opening. Do not bake stars into the roof map. A separate headliner material/control and switchable starlight intensity/visibility interface are proposed only; not implemented. Current shared dashboard material cannot provide independent headliner customization. See `CONFIGURATOR_INTERFACES_R2.md`.

## Evidence and reproduction
- `build_pipeline/isolated/build_cabin_r2.py`, `doors_r2.py`: reference-led source; previous builder preserved.
- `working_models/B3-doors-r2.blend`: editable individual components and packed imported images.
- `working_models/B3-doors-r2-review.blend`: review-only white vertex attributes; not GLB source.
- `exports/B3-doors-r2/{classic,diamond,perforated}.glb`: passing candidates.
- Per-treatment JSON in this directory; `reports/reference-r2/tangent-regression.json`, `tangent-before.json`, `regression-tests.json`.
- Build using Blender 5.2.2 `--python-exit-code 1 --python build_pipeline/isolated/build_cabin_r2.py -- B3-doors-r2`; then `node build_pipeline/isolated/finalize_r2.mjs B3-doors-r2`.
- Run `node build_pipeline/isolated/test_r2.mjs` for contract/path/budget rejection checks.

Not tested: browser appearance, device/GPU performance, independent new controls, full cabin completeness, human visual acceptance. No production replacement is authorized by this report.
