# 3D-1 — Driver-seat experiment (candidate only, awaiting owner review)

Date: 2026-11-17. Scope: `GEO_Seat_Front_Driver` and `GEO_Seat_Stitching_Front` only. Production GLBs, viewer, cameras, shaders and UI are unchanged. The candidates are scratch files and are not committed.

## 1. Result in one paragraph

The driver backrest outline is reshaped from a "shield" (widest at about 70 % height, then a sharp taper to a narrow neck) to near-parallel sides with broad, rounded shoulders, as photographed in Gallery 08 and 30. The bolster crest is softened by 15 %. The change is visible at Driver Hero and small at Stitch Detail, because that camera looks at the cushion, which is not edited. The geometry is a visual reconstruction from photographs. No seat dimension was supplied and no dimensional accuracy is claimed. **This is not a visual sign-off; the owner judges the renders.**

## 2. What was changed

One smooth displacement field (`scripts/experiments/3d-1-driver-seat/seat-profile.mjs`) moves backrest vertices and the stitches that sit on the backrest. Normals and tangents are transformed with the same field.

| Item | Production | Candidate |
|---|---|---|
| Backrest half-width at 0.86 m height | 0.286 m | 0.268 m |
| Backrest half-width at 1.00 m height | 0.226 m | 0.248 m |
| Bolster crest above the insert plane | up to 0.039 m | 15 % lower |
| Largest vertex move: bolster / insert / stitching | — | see `docs/evidence/3d-1/build.json` |
| Cushion, headrest, posts, plinth, switches | — | not moved |

The heights and widths are coordinates of the existing model, not vehicle measurements.

## 3. What was kept (verified)

- Triangles: 66,260 before and after (increase 0 of the 4,000 allowed; limit 80,000).
- Draw calls: 24 (limit 24). No new primitive or material.
- File size: classic 3,651,324 B, diamond 3,787,788 B, perforated 3,510,324 B (each 560 B larger than production; limit 5 MB).
- Material names and bindings, textures (KTX2), Draco settings: unchanged.
- UVs, indices and vertex colours of the edited primitives are identical, so the roughness-alpha thread mask still lines up. `tests/driver-seat-experiment.test.ts` checks this by hash for all three treatments.
- `scripts/compare-glb.mjs` reports geometry differences only in `GEO_Seat_Front_Driver#0`, `GEO_Seat_Front_Driver#1` and `GEO_Seat_Stitching_Front#0`, and no transform, material or texture difference (`docs/evidence/3d-1/compare-*.json`). Its `uvNotEquivalent` list names the same three because that check hashes UVs together with positions.
- `scripts/validate-glb.mjs` passes on all three candidates (`docs/evidence/3d-1/gate-*.json`).
- Production GLB SHA-256 values are unchanged; `tests/front-cabin-gate.test.ts` still pins them.

## 4. How to rebuild and review

```bash
node scripts/experiments/3d-1-driver-seat/build-candidates.mjs      # writes reports/3d-1/candidates/ (git-ignored)
for k in classic diamond perforated; do
  node scripts/validate-glb.mjs --asset reports/3d-1/candidates/interior-l4-$k.glb --report reports/3d-1/candidates/gate-$k.json
  node scripts/compare-glb.mjs public/assets/3d/lexus-rx350/interior-l4-$k.glb reports/3d-1/candidates/interior-l4-$k.glb
done
# Renders: build the app, copy dist/ to a scratch folder, overwrite the three GLBs in the copy, serve it, then
node docs/evidence/3d-1/capture-seat.mjs http://127.0.0.1:4174/ <outDir>
```

Tools: Node 22.23.2, `@gltf-transform/core` 4.5.1, `draco3dgltf` 1.5.9. Blender 5.2.2 was used only for diagnostic views, not to produce the candidates.

## 5. Evidence (`docs/evidence/3d-1/`)

- `before-after-{black,stone}-{driver-hero,stitch-detail}.jpg`: rows are Classic, Diamond, Perforated; left is production, right is candidate. Captured from the real viewer at 1440 × 900 with the existing camera presets. Thread is the existing "Light Ivory" option, the nearest to the photographed light-grey stitch. "Warm Stone" is included because the form is easier to read on a light hide.
- `driver-hero-before-after-vs-08-30.jpg`: production and candidate above Gallery 08 and 30. Gallery photographs are internal modelling references only.
- Rendered-pixel change, Classic in Warm Stone: Driver Hero 2.1 % of the stage, Stitch Detail 1.1 %.

## 6. Deviations from `FIRST_IMPLEMENTATION_EXPERIMENT.md`

1. **Scripted reshaping, not Blender modelling.** The seat is deformed on the decoded production GLB. This keeps every other part structurally identical and avoids re-running the full build, which mirrors the passenger seat from the driver seat and would have changed it.
2. **No faces moved between insert and bolster.** The insert uses a baked texture atlas per treatment (quilting, perforation, thread mask) with no bake source. Moving faces into it needs new UVs and re-baked textures, which is outside "no texture-pipeline change".
3. **No vertical channel seams.** The photographed insert has two stitched channels. Adding them needs either a re-baked atlas or new thread geometry that would cross the Diamond quilting.
4. **Cushion and headrest unchanged.** The photographs did not show a clear error that could be fixed without dimensions.
5. **Insert edge.** Up to 8 mm of movement at the insert's outer edge with fixed UVs, so the pattern stretches slightly there.
6. **Driver and passenger now differ.** The passenger seat is out of scope and keeps the old outline; both are visible together at Driver Hero and Cabin Pair.
7. **Stitch colour.** The model's thread colour comes from the customer's choice at runtime; no default was changed.

## 7. Correction to the gallery assessment

`COMPONENT_GAP_ASSESSMENT.md` described the model seats as sport buckets. Measured on the mesh, the bolsters stand about 0.04 m above the insert and the insert, arch seam and cushion seams are already separate zones. The sporty look came mainly from the backrest outline, which is what this experiment changes.

## 8. Rollback and next step

Nothing in production changes with this PR. Rejecting the experiment means closing the PR. If the owner accepts the look, promotion is a separate PR that copies the three candidates into `public/`, updates the pinned hashes and applies the same reshaping to the passenger seat.
