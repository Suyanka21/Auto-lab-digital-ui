# Reference and geometry discipline

## Read the construction, not just the colour

Identify silhouette extrema, principal panel breaks, attachment locations, opening outlines, thickness changes and material boundaries. Record reference filename, source dimensions, analytical resize, landmarks and uncertain depth. Use a camera guide/background, not a photograph pasted onto the mesh. Keep original images unchanged.

A primary and an alternate can show conflicting headrest positions, buttons or panel divisions. Keep primary visible design and record the conflict. Use the whole-cabin image for adjacency; it does not override a component primary. Hidden clips, hinge mechanisms and safety hardware are not licensed inventions from a single image.

## Surface choices demonstrated by R4

- **Padded panels:** paired perimeter curves and intermediate cross-sections define the crown and perimeter roll. Keep a flattened central region where the reference calls for it. Increase curvature near seams deliberately, not by inflating the entire panel.
- **Grip/armrest:** an asymmetric rounded section can separate sloping top, flatter front and under-return. Orient the section with the path tangent through the rise and bend. R4's globally vertical sections made a diagonal grip look like a thin ribbon; correcting orientation improved it without extra subdivision.
- **Openings:** represent the recess back, sidewalls and floor; leave a real view/clearance gap. R4 checked selected rays through the handle and pocket, plus the lip/grille mesh pair. These local checks do not prove every junction safe.
- **Adjacent components:** share boundary samples or intentionally offset them. The original shoulder/pocket pinch needed replacement of the intersecting profiles. Covering it with another lip would retain the fault.
- **Trim:** build a recess and a lever with thickness, rather than a flat lever silhouette. Bound bezel insets by local curvature to prevent corner foldovers. Small bevels improve edge response but do not correct the wrong outline.
- **Stitches:** project short stitch segments onto evaluated upholstery; report skipped projections. Keep seams attached after surface edits. Do not place a repeated decoration across unrelated panel boundaries.

Use local/world transforms consistently in raycasts and overlap checks. R4's image-space mapping was a door-specific construction convenience; future curved shell/seat topology needs appropriate surface parameterisation.

## Apply the method across the cabin

| Component | First forms to resolve | Common failure to avoid |
|---|---|---|
| Front seats / rear bench | Cushion/backrest crowns, bolster transitions, headrest attachments and seam zones | Quilting or perforation over inaccurate foam geometry; copying front-seat proportions to a bench |
| Dashboard / console | Tiering, recessed controls, display housing, boots and trim interruptions | Raised boxes on a slab; confusing active screen area with outer housing |
| Doors | Silhouette, upholstered insert, grip support, pocket depth and speaker seating | Inflated cylindrical armrests and intersecting pocket/speaker surfaces |
| Shell / pillars / roof | Shared envelope, aperture edges, pillars-to-headliner and dash-to-door junctions | Independently modelled parts that cannot meet in assembly |
| Starlight headliner | Headliner shape, roof openings and an explicit point/anchor layout | Baking permanent glowing dots and claiming runtime controls exist |

Validate shell proportions against the approved assembly image and available supporting photographs. Preserve uncertainty; do not claim measured fit. Keep starlight geometry/data separate until a runtime interface is authorised.
