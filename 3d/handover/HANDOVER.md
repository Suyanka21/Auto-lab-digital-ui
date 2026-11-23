# Project handover

## Objective and repository state

Build a coherent premium five-seat SUV cabin for the existing real-time AutoLab configurator, using the approved bespoke AI designs and the accepted R4 modelling quality. This is not a static-render-only project. Publication starts from `cd0760e` on `chore/autolab-r4-devin-handover`; the reference pack was merged through PR #7, so no separate reference merge is needed. Main and other development branches were not modified. No dependency on an unmerged Devin plan or candidate is introduced.

## Reference authority

`AUTOLAB_INTERIOR_3D_REFERENCE_PACK/REFERENCE_MANIFEST.md` names 16 approved AI design images. The component PRIMARY controls visible design. ALTERNATES and SECONDARY images inform depth/assembly without overriding the primary. `00_MASTER_CABIN/PRIMARY/` governs overall adjacency; `06_CABIN_SHELL/` is structural context; `99_EXCLUDED/SHOWROOM_CONCEPTS/` is not cabin geometry.

The front-door benchmark uses `01_FRONT_DOOR_PANELS/PRIMARY/AUTOLAB_SUV_FRONT_DOOR_PANEL_PRIMARY_01.jpg`; its alternate is in the sibling `ALTERNATES/` directory. Seats, rear bench, dashboard/console and starlight primaries remain at `03_FRONT_SEATS/PRIMARY/`, `04_REAR_BENCH/PRIMARY/`, `05_DASHBOARD_AND_CONSOLE/PRIMARY/`, `07_STARLIGHT_HEADLINER/PRIMARY/`. The rear-door primary is at `02_REAR_DOOR_PANELS/PRIMARY/`.

`AUTOLAB_2020_LEXUS_RX350_REFERENCE_LIBRARY/00_GALLERY_ORIGINALS/` retains the 35-photo supporting gallery and `SECOND_RESEARCH_ROUND/` its corrected research. Not all 35 images show the interior. These photographs support component interpretation; they do not override the subsequently approved bespoke AI design or establish exact measurements. Do not reproduce vehicle emblems or brand screen art.

The inherited AI reference manifest has 14 previously documented checksum inconsistencies. Images and that historical manifest are preserved; `reference-hashes.json` records the actual files at this publication. Do not treat its prose ledger as cryptographic proof or silently replace references to make hashes match.

## Completed and incomplete work

| Milestone | Actual state |
|---|---|
| Live front-cabin app | Existing three-treatment real-time implementation; untouched by this handover |
| A-frame, B1 floor, B2 rear | Historical candidate masters/exports and evidence retained; not the new visual benchmark |
| B3 doors R2 | Technically passing rollback, 78,028 triangles; visually superseded |
| B3 doors R3 | 79,004 triangles / 22 primitives; only 996 triangles of full-cabin budget remain; not a sustainable complete-cabin solution |
| Original R4 | Detailed single front-door reconstruction; 925,924 evaluated triangles; retained as editable history |
| Refined R4 | Owner-approved visual benchmark; 719,424 evaluated master triangles; no runtime export |
| Remaining components | No R4-quality final approval implied for other doors, seats, bench, dash/console, shell, pillars or roof |
| Headliner/starlights | Design reference exists; independent live headliner/starlight contracts are proposals, not implemented controls |
| Full-cabin runtime | Optimisation, bake strategy, complete assembly fit, browser and real-device acceptance remain open |

## Recommended continuation

This is a recommended order for the next authorised work, not permission to execute it during the handover:

1. Review R4 and the whole-cabin primary; record assembly coordinates and required junctions. Use retained A/B masters only as provisional placement evidence.
2. Bring the remaining door cards to the approved benchmark from their own primaries, with correct handedness and control differences; do not blindly mirror driver controls.
3. Resolve connected floor/tunnel, cabin shell, pillars and roof envelope against all door apertures before fine surface detail.
4. Bring front seats and rear bench to their respective primaries, checking seat-to-floor, row spacing and door clearance as one assembly.
5. Reconstruct/refine dashboard and console from their primary, preserving connections to doors and the rear vent region.
6. Finish headliner/roof openings and a separate starlight anchor design. Resolve any new configuration interface before claiming live controls.
7. Review the coherent master assembly; only then author a separately budgeted runtime derivative, bake, validate and perform authorised browser/device integration.

If the owner gives a different next component, follow that instruction while retaining assembly checks. Do not reuse the old runtime-first allocation to constrain each master.

## Structure and history

- `.agents/skills/autolab-premium-cabin-modeling/`: portable instructions and tested helpers.
- `3d/workspace/working_models/`: approved and archived editable masters.
- `3d/workspace/build_pipeline/`: original scripts, local isolated scripts, pinned historical inputs and package lockfiles.
- `3d/workspace/reports/`: raw review evidence, render/build logs and dated decisions, including R4 pilot/round history.
- `3d/workspace/exports/`: earlier candidate GLBs, never live assets.
- `3d/handover/workspace-inventory.json`: every original workspace file, hash, inclusion decision and canonical repository location.

Binary duplicates are represented by inventory aliases, often pointing to the existing root reference libraries or public baseline. Restore a complete scratch workspace using `workspace_transfer.py --restore ...` before running archived scripts or HTML galleries. This avoids storing duplicate references while retaining their original required paths.

## Restrictions and unresolved matters

The reference scale, hidden construction, upholstery foam thickness, final fit, UV distortion, baked shader equivalence and real-device performance remain unverified. The window switches and minor details are accepted visual-example limitations. Do not claim the detailed master is a finished vehicle or browser-ready model. No automatic production promotion, new material slots, camera-coordinate changes, deployment, merge or local deletion is authorised.
