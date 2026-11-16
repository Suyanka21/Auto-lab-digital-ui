# First implementation experiment (proposal — not started)

Needs owner approval. Depends on 3D-0 ([PR #3](https://github.com/Suyanka21/Auto-lab-digital-ui/pull/3)) being accepted.

## Experiment: re-zone the driver front seat to the photographed RX 350 seat

**Component and scope:** `GEO_Seat_Front_Driver` and its stitching mesh `GEO_Seat_Stitching_Front` only. The passenger seat, dashboard, console, steering wheel, cameras, UI and the other primitives stay untouched. The output is a scratch candidate GLB set, not a production replacement.

**Gallery evidence:** 08 and 30 (side and three-quarter of the inserts and bolsters), 23 and 29 (seat against door and console, power-switch shield), 07 and 34 (seat from the centre), 27 (perforation close-up).

**Assets and scripts affected (scratch copies only):** the build chain recorded in `docs/3d-roadmap/3D-0_REPRODUCIBILITY_REPORT.md` — `scripts/prepare-front-cabin.mjs`, `blender/build_front_cabin.py` (Blender 5.2.2), `scripts/finalize-front-cabin.mjs` (KTX 4.4.2, Draco) — plus the gate `scripts/validate-glb.mjs` and `scripts/compare-glb.mjs`.

**Modelling approach:**
1. In Blender, lower and soften the outboard and inboard backrest bolsters and the cushion side bolsters to the comfort profile in 08/30.
2. Move seam loops so the centre insert boundaries match the photos (backrest insert and cushion insert as separate zones with vertical channels).
3. Assign insert faces to `MAT_Seat_Primary` and bolster faces to `MAT_Seat_Secondary`; keep existing names.
4. Re-fit stitching UVs to the new seams so the roughness-alpha thread mask still lines up.
5. Perforation stays in texture (existing Perforated treatment), not geometry.
6. Shape is judged against photos only; no dimensions are taken from photos. If the owner supplies two measured seat dimensions, use them as the scale check.

**Expected visual result:** at Driver Hero and Stitch Detail the driver seat reads as the RX 350 comfort seat with clearly separate inserts and bolsters, so Classic, Diamond and Perforated, and Duotone, land on the zones a customer would see in the real car.

**Performance constraints:** no new primitive or material (draw calls stay 24); triangle increase ≤ 4,000 (model stays ≤ 70,260 of 80,000); each GLB ≤ 5 MB; same KTX2 and Draco settings.

**Validation and acceptance:**
- `npm run asset:gate` passes on all three candidates for budgets and material contract (the pinned-hash test is expected to fail and shows the change).
- `scripts/compare-glb.mjs` shows differences only in the driver-seat and driver-stitching primitives.
- Unit tests, typecheck, lint and build pass with the candidate loaded locally.
- Fixed-camera renders (Driver Hero, Stitch Detail) for all three treatments beside Gallery 08 and 30, for owner review. The agent does not self-certify visual acceptance.

**Rollback:** production GLBs are never overwritten in the experiment. Rejecting it means deleting the scratch output; the pinned hashes keep production unchanged.

**Why this first:** it scored highest in `COMPONENT_GAP_ASSESSMENT.md` (15/15). It is the customer's main decision surface, the evidence is the strongest in the gallery, it fits the existing draw-call budget, and the result can be checked directly against photos. Doors, floor, roof and rear seats each need new draw calls and so a budget decision first. The dash end-cap colour is cheaper but a smaller visible gain; it is a good second experiment.
