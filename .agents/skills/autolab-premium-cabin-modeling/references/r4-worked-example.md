# R4 worked example

Repository evidence: `3d/workspace/working_models/R4-front-door-refined.blend`, `3d/workspace/reports/R4-front-door-refined/`, and `3d/workspace/build_pipeline/isolated/{build_front_door_r4,refine_front_door_r4}.py`. Restore aliases with the handover helper before running archived scripts. If this skill is moved alone, these are example provenance paths, not mandatory runtime imports.

## What actually produced the result

The original builder uses `linkmesh`, `curvepoints`, `slab`, section/sweep helpers and explicit component collections. It records landmarks and review cameras in `master-metrics.json`. The primary is a packed camera guide, not a texture pasted onto the geometry.

The refinement opens the saved original master and imports only function definitions from the original builder via Python AST. It does not run that builder's factory reset. It replaces selected grip, pocket, release and seal components, keeping unaffected parts. `master-metrics.json` identifies retained base geometry and replacements.

The armrest uses rounded **asymmetric** cross-sections for its top-back, top-front, lower-front and lower-back. Orienting these sections along the rising grip path corrected the ribbon-like result of globally vertical sections. Local compression and reprojected stitch rows follow the upholstery. The pocket/speaker problem was solved by replacing incompatible boundary surfaces with a smooth shoulder envelope and matching wall, not by adding a cover patch.

The front-view analytical frame is 1200 x 670, with `MM=.00146` and an image-to-world mapping in the builder. These are provisional **door-specific** values. Do not use them as a cabin scale, seat width, measurement method or manufacturing specification. The original image is 2752 x 1536; its projection is unknown.

## Counts and preserved evidence

Original R4: 48 mesh components / 54,782 base vertices / 925,924 evaluated triangles. Refined: 48 / 50,916 / 719,424. The decrease came from controlled surface/modifier choices, not a production optimisation claim. The complete-cabin runtime ceiling is a separate constraint.

Original R4 rounds and refinement pilots are preserved in the inventory. Final evidence includes front, three-quarter, grip/armrest, pocket/speaker, release/wood, neutral and material views plus a supplemental material lab. A 345-file hash check protected earlier work. Fresh-open checks and selected opening/overlap probes passed; they do not prove all geometry collision-free.

The owner subsequently approved the refined file as a **visual benchmark**. Controls, lower support, trim corners, pocket sculpting and uniform materials remain documented imperfections. The lesson is disciplined reference comparison and editable corrections, not a claim that every R4 technique or shape is perfect.

## Reuse boundary

Use the same questions on a seat, bench, console or headliner: what defines the silhouette, how does padding meet a rigid boundary, where is real depth required, which surface owns each material, and what evidence will reveal a wrong junction? Select topology and UV methods for that component. Do not run the door builder to create unrelated geometry or rename R4 master materials into live slots without an integration plan.
