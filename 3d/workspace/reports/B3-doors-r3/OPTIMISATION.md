# R3 measured allocation and optimisation strategy

## Delivered candidate
R3: 79,004 decoded triangles, 22 primitives, 10 materials. R2: 78,028 triangles. Net increase: 976. Only 996 triangles remain below 80,000; the complete cabin still does not fit without further reductions.

| Component | Decoded triangles |
|---|---:|
| GEO_Dashboard_Lexus | 8,288 |
| GEO_Seat_Front_Driver | 17,367 |
| GEO_Seat_Front_Passenger | 17,367 |
| GEO_Seat_Stitching_Front | 6,718 |
| GEO_Seat_Stitching_Front_Passenger | 6,718 |
| GEO_SteeringWheel_Lexus | 4,404 |
| GEO_Console_Assembly | 5,398 |
| GEO_Cabin_Expansion | 12,744 |

| Material | Decoded triangles |
|---|---:|
| MAT_Dashboard_Trim | 2,426 |
| MAT_Console_Carbon | 1,492 |
| MAT_Cockpit_Black | 8,016 |
| MAT_Cockpit_Accent | 2,360 |
| MAT_Seat_Primary | 8,772 |
| MAT_Seat_Secondary | 32,210 |
| MAT_Seat_Stitching | 13,436 |
| MAT_Steering_Leather | 3,464 |
| MAT_Console_Black | 3,344 |
| MAT_Console_Metal | 3,484 |

## Source allocation before compression
Full per-object/material rows: component-material-triangles.csv and allocation-after.json. These counts precede export filtering and are not delivery totals.
| Group | R2 | R3 |
|---|---:|---:|
| Floor/supports | 572 | 572 |
| Rear seating | 3,800 | 3,800 |
| Doors | 7,640 | 8,436 |

## Optimisation performed
- Removed modelled speaker bars; thin face and rim retain the outline. Grille microdetail is procedural in the master only.
- Removed a redundant interior surface ring and reduced tiny seam/reveal tube sections after an initial 82,844-triangle build exceeded the cap. That attempt stopped before final export.
- Spent remaining triangles on contour and variable-section transitions. No decimation of front seats, dashboard, steering or console was performed.

## Proposed next optimisation (requires subsequent scoped work)
1. Keep this door candidate on hold for visual review. Do not consume the 996-triangle reserve with another construction milestone.
2. Treat front stitch meshes (13,436 triangles) as the first savings investigation. Bake fine/subpixel thread into normal and recolour masks while retaining silhouette-critical perimeter thread. Verify the existing live thread shader before promotion.
3. Reduce invisible front-seat backs/undersides and tiny console bevels while protecting UV borders, upholstery pattern scale and hero-view silhouettes.
4. Bake grille, fine seams, small labels and plastic grain into an explicitly planned atlas. Preserve original runtime slots and prove the added texture payload stays under the existing byte limit.
5. Use fixed-camera master/runtime comparison plus runtime measurements before claiming visual or performance equivalence.

## Complete-cabin proposal
The unchanged 80,000-triangle allocation proposed BEFORE modelling is in GEOMETRY_ALLOCATION.md: front seats 32k; front stitching 4k; dashboard/steering 9k; console 4k; rear seats 7k; doors 8k; enclosure/pillars/roof 6k; floor/tunnel 3k; secondary vents/details 2k; reserve 5k. These targets are not demonstrated results.

## Separate master and runtime
Recommend maintaining the editable, component-separated Blender source and a distinct look-development master, then deriving an optimized triangulated GLB. R3 provides both source and render master; it is not a finished high-resolution production master. Procedural shader fidelity is currently ahead of the runtime derivative for grille/wood; parity is explicitly unproven. Keep the 80,000 / 24 primitive proxy / 5,242,880-byte limits unchanged.
