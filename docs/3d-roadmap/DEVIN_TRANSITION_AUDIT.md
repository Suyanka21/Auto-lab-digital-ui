# Devin transition audit

Date: 2026-11-15. Author: Devin. Status: audit only. No production model, UI, viewer or asset was changed.

Evidence labels used in all `docs/3d-roadmap/` files:
- **Verified**: I ran the command or read the file at the commit stated.
- **Inherited**: recorded by an earlier agent; I did not re-run it.
- **Inferred**: my reasoning from verified facts; needs confirmation.

## 1. Repositories and exact commits

| Repository | Role | Commit inspected | State |
|---|---|---|---|
| `Suyanka21/AUTOLAB-DIGITAL-SHOWROOM` | Original Next.js engineering repo | `main` = `b5338d3` (merge of PR #6) | Clean. No uncommitted work. |
| `Suyanka21/Auto-lab-digital-ui` | New authoritative Vite showroom | `main` = `9f457a8` (Manus documentation), on top of `3c90ce8` (merge of Codex PR #1) | Clean before this branch. |

Original repo remote branches (verified with `git ls-remote`): `main`, six merged `devin/*` branches (PR #1–#6), `codex/l5-r1-design-refinement` and `pre-phase-6-reconciliation`. Neither of the last two has commits that are absent from `main`. No branch was deleted.

### Work outside any repository (verified on the Devin VM)

| Item | Location | Status |
|---|---|---|
| D0 decision record | `/home/ubuntu/proposal/D0_DECISION_RECORD.md` | Delivered to the owner as an attachment; not committed. Decisions on draw calls, toolchain and vehicle wording remain relevant to 3D work. |
| Editorial Atelier concept bundle | `/home/ubuntu/proposal/concept/` | Delivered as attachments; not committed. Superseded by Astra's approved showroom. |
| Baseline worktree | `/home/ubuntu/v1-work/before` (`9081e79`) | Local comparison worktree for V1. Not pushed; safe to discard later, kept for now. |

## 2. Completed original-repo work and its fate

| PR | Change | Classification for the new repo |
|---|---|---|
| [#1](https://github.com/Suyanka21/AUTOLAB-DIGITAL-SHOWROOM/pull/1) | Gate tests build their own synthetic GLB fixtures | **Pattern worth migrating.** The new repo's asset gate is not runnable yet (section 4). |
| [#2](https://github.com/Suyanka21/AUTOLAB-DIGITAL-SHOWROOM/pull/2) | Removed mock auth, `/dashboard`, `/auth` | Superseded (Next.js shell only). |
| [#3](https://github.com/Suyanka21/AUTOLAB-DIGITAL-SHOWROOM/pull/3) | Removed Executive Fluted from live options | Superseded as UI; the rule "no option without a visible geometry effect" carries over. |
| [#4](https://github.com/Suyanka21/AUTOLAB-DIGITAL-SHOWROOM/pull/4) | Reframed `hero_driver` so seat colour is visible and the dashboard end no longer fills the frame | **Worth migrating as data.** The new repo still has the old preset (section 3). |
| [#5](https://github.com/Suyanka21/AUTOLAB-DIGITAL-SHOWROOM/pull/5) | Reliable Playwright suite, production smoke in CI | Superseded; the new repo has its own 10 Playwright specs. The output-directory rule carries over. |
| [#6](https://github.com/Suyanka21/AUTOLAB-DIGITAL-SHOWROOM/pull/6) | Live `seam_macro` treatment study from the existing canvas | Superseded as UI. The capture technique (one canvas, debounced off-screen view offset) is reusable for a future material close-up if the owner wants one. |

### 3D engineering that exists only in the original repo (verified)

- Blender sources: `blender/*.py` (20 scripts, including `build_front_cabin.py`, `lexus_l4_materials.py`, `lexus_l4ar1_materials.py`, `front_cabin_carbon.py`, `cockpit_surfaces.py`).
- Blender files: `blender/models/front-cabin.blend` and `components/{driver-seat,passenger,dashboard,wheel}.blend`.
- Review evidence: `docs/review/lexus-l2a-*` to `lexus-l4ar1-*`, `front-cabin-2026-11-05`, `live-trim-2026-11-11`.
- Validator and specifications that the new repo's ported `scripts/validate-glb.mjs` still points at: `docs/spike/plan.md`, `docs/quality/performance-requirements.md`, `docs/schemas/scene-manifest.schema.json`, the S-Class manifest.

These must stay referenced by commit (`b5338d3`) until a migration PR copies them deliberately.

## 3. Shared runtime assets (verified)

The three GLBs are byte-identical in both repositories:

| Asset | Bytes | SHA-256 |
|---|---:|---|
| `interior-l4-classic.glb` | 3,650,764 | `e5bdde016348df34889ec4c0ff0e406caad7e368504308bd5a4f5b725a55c056` |
| `interior-l4-diamond.glb` | 3,787,228 | `4c217dd00d86d8bae3925d735beddb63b225d24c5f1bafd60726f501bfcba8ad` |
| `interior-l4-perforated.glb` | 3,509,764 | `d53f55546232db473ecadee08be9bff6454b5d3a510ee30e88415f2477ca9f9e` |

Classic GLB contents (verified by reading the GLB JSON chunk):
- 11 nodes: `GEO_Console_Armrest`, `GEO_Console_Body`, `GEO_Console_Cupholder_Front`, `GEO_Console_Cupholder_Rear`, `GEO_Console_Selector`, `GEO_Dashboard_Lexus`, `GEO_Seat_Front_Driver`, `GEO_Seat_Front_Passenger`, `GEO_Seat_Stitching_Front`, `GEO_Seat_Stitching_Front_Passenger`, `GEO_SteeringWheel_Lexus`.
- 24 primitives (one draw call each), 66,260 triangles (inherited), 9 textures.
- Extensions: `KHR_draco_mesh_compression`, `KHR_texture_basisu`, `KHR_materials_clearcoat`, `KHR_materials_specular`.
- 10 materials. Only 3 carry base/ORM/normal maps (`MAT_Seat_Primary`, `MAT_Seat_Secondary`, `MAT_Console_Carbon`). 2 carry a normal map only (`MAT_Dashboard_Trim`, `MAT_Steering_Leather`). 5 are flat colours with no texture (`MAT_Console_Black`, `MAT_Console_Metal`, `MAT_Cockpit_Black`, `MAT_Cockpit_Accent`, `MAT_Seat_Stitching`).
- No doors, pillars, floor, roof, pedals, screen glass, vents or rear seats.

Camera preset difference (verified in `src/config/lexus-camera-presets.ts`):

| Preset | Original `main` | New repo `main` |
|---|---|---|
| `hero_driver` position | `[1.9, 1.25, 0.2]` (PR #4) | `[1.45, 1.25, 0.95]` (pre-PR #4) |
| `seam_macro`, `cabin_pair`, `driver_cockpit` | same | same |

## 4. New repository baseline (verified on this branch's parent `9f457a8`)

| Check | Result |
|---|---|
| `npm ci` (Node 22.23.2) | pass |
| `npm run typecheck` | pass |
| `npm run lint` | pass |
| `npm test` | 5 files, 39/39 pass |
| `npm run build` | pass (chunk-size warning only) |
| `node scripts/validate-glb.mjs` (no arguments) | **FAIL**: "0 nodes, 0 triangles, 0 draw calls". Its default paths point at original-repo files that were not ported. |
| Playwright `tests/browser/` (10 specs) | Not run in this audit. |

No `AGENTS.md`, Husky or pre-commit configuration exists in the new repo.

## 5. Visual defects and root causes

| # | Defect | Root cause | Evidence |
|---|---|---|---|
| D1 | Grey dashboard end fills the left of Driver Hero | Dashboard outer ends are flat capped surfaces with no door or A-pillar to hide them; camera sat inside that line of sight | Verified in original (PR #4). New repo still uses the old preset; the visual result there is inferred, not rendered. |
| D2 | Seat shading looks faceted | Low seat-shell density for a hero object; normals not baked from a high-poly source | Inherited (`INDEPENDENT_3D_ASSESSMENT.md`) |
| D3 | Console reads as plastic and strongly reflective | `RoomEnvironment` PMREM plus clearcoat on `MAT_Console_Carbon` at roughness 0.28; flat untextured black and metal | Material factors verified; look inherited |
| D4 | Half the cabin has no surface detail | 5 of 10 materials are flat colours with no maps | Verified |
| D5 | Duotone's second colour also covers seat backs, headrests and steering wheel | Material zoning of `MAT_Seat_Secondary` and adapter rule that steering follows the secondary colour | Verified in original during the visual proposal; same bindings documented in the new repo |
| D6 | Trim choices barely change the view | Trim lives on small `MAT_Console_Carbon` areas; at most 2.3 % of pixels change between trims | Measured in original |
| D7 | Ambient lighting reads as a glow on the wheel, not an LED wash | Three small point lights; no emitter geometry or light channel | Verified in `RuntimeViewer.tsx` |
| D8 | Cabin floats in space | No floor, doors, pillars or roof | Verified (node list) |
| D9 | GLB provenance is not reproducible | No committed script names `interior-l4-*`; the master `.blend` README lists slots (`MAT_Trim_Deck_Main`, `EMISSIVE_Ambient_Lighting`, `MAT_Display_Glass`) that are not in the GLB; two scripts hard-code a Windows `toktx.exe`; Blender and KTX are not installed on the VM | Verified |
| D10 | Vehicle data overclaims accuracy | `src/config/vehicles/lexus-rx350-2020.json` sets `evidenceConfidence: "CONFIRMED"` while reference notes call dimensions photo estimates | Verified in both repos |

## 6. Recommendation

Treat the new repo as the only runtime target. Keep the original repo read-only as the source of Blender sources, review evidence and the asset gate until each is migrated by its own small PR. The first engineering step is reproducibility (D9), not new geometry: without it, no improved model can be traced back to a source.
