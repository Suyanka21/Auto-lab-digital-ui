# R3 door-panel owner review
2026-11-20. Technical PASS; visual acceptance OPEN. Stop at doors.

## Start here
- [Reference comparison](reference-comparison.jpg)
- [All inspection renders](inspection-contact-sheet.jpg)
- [Preserved R2 versus R3](r2-r3-comparison.jpg) (different legacy lighting; shape comparison only)
- [Interactive local review index](index.html)
- [Specific visual discrepancies](VISUAL_DISCREPANCIES.md)
- [Allocation before modelling](GEOMETRY_ALLOCATION.md)
- [Measured revised allocation and strategy](OPTIMISATION.md)
- [Per-component and material CSV](component-material-triangles.csv)
- [Validation results and commands](VALIDATION.md)

## What changed
Four door panels rebuilt with rounded shells, padded upper surfaces, recessed release/trim regions, sculpted leather inserts, swept pull/palmrest construction, curved bin faces and thin speaker discs. Reversed open faces were corrected. No production assets, viewer code, original baseline meshes or material contracts were edited.

Classic, Diamond and Perforated each pass offline checks at **79,004 triangles / 22 primitives / 10 materials**. Bytes: **4,102,316 / 4,238,780 / 3,961,316** respectively. Only **996 triangles remain**; the remaining cabin cannot be completed in this headroom. Proposed full-cabin redistribution retains 80,000 triangles and is not yet achieved.

## Material evidence boundary
These are actual Blender geometry renders under neutral studio lighting. The source and separate MASTER look-development file are supplied. Procedural tan leather, illustrative walnut and grille detail in the master do not establish equivalent appearance in the GLBs. Runtime candidates keep original KTX2 textures/carbon trim and material names. Speaker microperforation and wood have not been baked into them. Diagnostic colours are shown separately and prove only region separation.

## Remaining visible issues
The pocket opening is still too shallow visually; the armrest is soft and its under-grip opening/support is less resolved than the primary design. Upper-roll ends, rear silhouette, inset seams, release recess and fine material character need review. R3 improves R2 but does not fully match the primary reference. See the feature-by-feature discrepancy table.

## Owner review checkpoint
- [ ] Judge front and rear silhouette against the primary design.
- [ ] Review pull attachments, under-grip clearance, armrest support and pocket depth.
- [ ] Review upper padding, trim recesses and insert seam boundaries.
- [ ] Review the proposed master/runtime optimisation workflow and full-cabin allocation.
- [ ] Decide whether these door forms need another revision before any next milestone.

No box is pre-approved. Pillars/roof are on hold. Runtime material parity, browser/phone performance and complete-cabin acceptance remain unverified.

## Files and rollback
- Editable component source: `../../working_models/B3-doors-r3.blend`
- Separate shaded master: `../../working_models/B3-doors-r3-master.blend`
- Runtime candidates: `../../exports/B3-doors-r3/{classic,diamond,perforated}.glb`
- Reproducible scripts: `../../build_pipeline/isolated/*r3*`
- R2 rollback: `../../exports/B3-doors-r2/` and `../../working_models/B3-doors-r2.blend`.

SHA256 verification confirms all seven protected R2 files unchanged. Baseline hash guard passes. No push, deployment, production replacement or human-gate closure occurred.
