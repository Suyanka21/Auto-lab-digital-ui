from pathlib import Path
import json,hashlib,shutil
from PIL import Image,ImageOps,ImageDraw
r=Path(r'C:\Users\user\Documents\AUTOLAB_3D_WORKSPACE');out=r/'reports/B3-doors-r2'
# Local review comparison only; references never enter production textures or public assets.
items=[('FRONT: approved AI design','references/approved_ai_design/01_FRONT_DOOR_PANELS/PRIMARY/AUTOLAB_SUV_FRONT_DOOR_PANEL_PRIMARY_01.jpg'),('FRONT: candidate geometry / material regions','reports/B3-doors-r2/front-material-regions.png'),('REAR: approved AI design','references/approved_ai_design/02_REAR_DOOR_PANELS/PRIMARY/AUTOLAB_SUV_REAR_DOOR_PANEL_PRIMARY_01.jpg'),('REAR: candidate geometry / material regions','reports/B3-doors-r2/rear-material-regions.png')]
canvas=Image.new('RGB',(1600,1120),'#eeeae3');draw=ImageDraw.Draw(canvas)
for i,(label,path) in enumerate(items):
 x=(i%2)*800;y=(i//2)*550;draw.text((x+20,y+15),label,fill='#111111');im=Image.open(r/path).convert('RGB');im.thumbnail((780,490));canvas.paste(im,(x+(800-im.width)//2,y+45+(490-im.height)//2))
draw.text((20,1100),'LOCAL REVIEW ONLY | AI references are design concepts | Render colours are diagnostic overrides; visual acceptance remains open.',fill='#111111')
canvas.save(out/'door-reference-comparison.jpg',quality=92)
rows=[]
for k in ['classic','diamond','perforated']:
 d=json.loads((out/f'{k}.json').read_text());rows.append(f"| {k.title()} | {d['triangles']:,} | {d['primitives']} | {len(d['materials'])} | {d['bytes']:,} | PASS |")
report='''# Reference-led door milestone — R2
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
'''+ '\n'.join(rows)+'''

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
'''
(out/'REVIEW.md').write_text(report,encoding='utf-8')
(r/'reports/CONFIGURATOR_INTERFACES_R2.md').write_text('''# Future configurator interfaces — proposals only
Updated 2026-11-19. No viewer, shader, UI, camera or runtime contract changes applied.

| Region | Current candidate assignment | Current consequence | Later requirement |
|---|---|---|---|
| Door middle + armrest/pull | MAT_Seat_Secondary | Recolours with secondary seats | If independent door colour is required, approve a dedicated door upholstery slot and adapter input; preserve panel provenance and UVs |
| Door decorative insert | MAT_Console_Carbon | Same finish as dash/console | Existing shared finish preview; separate door finish would require a further explicit contract |
| Door shell/pocket/speaker | MAT_Cockpit_Black | Structural black | Retain fixed finish |
| Upper door padding | MAT_Dashboard_Trim | Fixed leather tint | May be separated later if commercially required |
| Metal handle/rim | MAT_Console_Metal | Existing metallic behaviour | Retain |
| Headliner (not built) | None approved independently | Shared dashboard slot would not be independent | Propose MAT_Headliner, bounded normal/roughness texture and dedicated component; not added |
| Starlights (not built) | None | No independent lighting feature exists | Local roof-space anchor data plus visibility/intensity controls; optional instanced points at integration; no permanent emission bake |

Future starlight interface should distinguish enabled, intensity and optional twinkle, with a quiet reduced-motion state and no new permanent canvas. Roof opening exclusion zones and headliner mounting normals must accompany anchor data. Implementing this requires later viewer approval; no current runtime promise is made.
The bright white showroom belongs to later lighting/environment configuration, not model geometry. Current inspection lights do not establish final viewer appearance.
''',encoding='utf-8')
state=r/'reports/STATE.md';archive=r/'reports/STATE-before-reference-r2.md'
if not archive.exists():shutil.copy2(state,archive)
state.write_text('''# Isolated 3D state
2026-11-19: reference-led door milestone R2 technically passes; full cabin incomplete.
Exclusive workspace AUTOLAB_3D_WORKSPACE; production assets unchanged; no app edits or remote writes.
Design target: coherent customisable AutoLab premium SUV; exact Lexus reconstruction superseded.
Approved AI pack commit 0e68d56c8863b5890fdcd580e570a2910edeaf38 downloaded, 16 images + 3 docs.
All images match Git blob hashes and ledger sizes; 14 manifest SHA256 values mismatch; report retained.
References at references/approved_ai_design; originals and older gallery retained separately.
Previous B3 door failure preserved; eight n-gons reproduced tangent error.
Explicit export triangulation fixes tangents; regression preserves positions and corner UVs.
R2 candidates: 78,028 triangles, 22 primitives, 10 material slots for all treatments.
Bytes: Classic 4,086,128; Diamond 4,222,592; Perforated 3,945,128.
Exports/B3-doors-r2 and working_models/B3-doors-r2.blend; all prior milestones preserved.
Review: reports/B3-doors-r2/REVIEW.md and door-reference-comparison.jpg.
Technical pass only: panels/grilles/padding/material preview remain visually provisional.
Door upholstery shares secondary-seat binding; independent door/headliner/starlights need future interfaces.
Only 1,972 triangles remain; recover low-value detail before enclosure/cockpit additions.
Next: budget-conscious refinement, pillars/roof/rear vents/cockpit; follow new primary references.
No star bake, new material names, manufacturer emblems, production replacement or PR6 promotion.
''',encoding='utf-8')
print('Review report, interface proposal, comparison and state saved. Prior state archived.')
