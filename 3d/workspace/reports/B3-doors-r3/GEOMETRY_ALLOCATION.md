# Geometry allocation before door revision
2026-11-19. Written before further modelling. R2 is preserved; no limits changed.

## Decoded R2 GLB: exact delivery counts
| Mesh component | Triangles |
|---|---:|
| GEO_Dashboard_Lexus | 8,288 |
| GEO_Seat_Front_Driver | 17,367 |
| GEO_Seat_Front_Passenger | 17,367 |
| GEO_Seat_Stitching_Front | 6,718 |
| GEO_Seat_Stitching_Front_Passenger | 6,718 |
| GEO_SteeringWheel_Lexus | 4,404 |
| GEO_Console_Assembly | 5,398 |
| GEO_Cabin_Expansion | 11,768 |

| Material | Triangles |
|---|---:|
| MAT_Dashboard_Trim | 2,558 |
| MAT_Console_Carbon | 1,624 |
| MAT_Cockpit_Black | 9,548 |
| MAT_Cockpit_Accent | 2,360 |
| MAT_Seat_Primary | 8,772 |
| MAT_Seat_Secondary | 30,318 |
| MAT_Seat_Stitching | 13,436 |
| MAT_Steering_Leather | 3,464 |
| MAT_Console_Black | 3,344 |
| MAT_Console_Metal | 2,604 |

## Authoring component detail
Full per-object/material ledger is in allocation-before.json. Blender source totals precede triangulation/export/Draco filtering; do not substitute them for decoded totals.
| Group | Source triangles |
|---|---:|
| Floor/supports | 572 |
| Rear seating | 3,800 |
| Doors | 7,640 |

## Expensive details and safe opportunities
- Two front seat meshes: 34,734 triangles. Preserve today; future runtime-only simplification should target hidden undersides/back sections while holding silhouette and UV seams.
- Two front stitch meshes: 13,436 triangles (17.2% of R2). Major opportunity: retain silhouette-critical perimeter thread geometry; bake subpixel seam detail into normal/ORM-alpha masks. This requires measured recolour equivalence before promotion; no stitch changes in this task.
- Four R2 speaker grilles use individual bevelled bars and faceted full cylinders. Replace bars with a thin low-poly disc and a material-level perforation representation in the master. Runtime texture-atlas allocation is a separate explicit delivery task; no pretend baked runtime result.
- Door shells are expensive bevelled extrusions with flat interior faces. Spend triangles on curved silhouette and cross-section rings instead of redundant backs or small-radius bevel strips.
- Replace layered handle/armrest blocks with swept sections and continuous transitions; use seam grooves and small stitch bumps rather than many thread objects.
- Consolidation already saves eight primitives without reducing triangle count; it is not a substitute for actual geometry optimisation.

## Proposed complete-cabin allocation — retains the 80,000 limit
This is a planning target requiring future measured reductions; not an approved change to production and not evidence these shapes already fit.
| Region | Target triangles |
|---|---:|
| Both front seats | 32,000 |
| Visible front stitching | 4,000 |
| Dashboard and steering | 9,000 |
| Console | 4,000 |
| Rear seating | 7,000 |
| Four door panels | 8,000 |
| Enclosure, pillars and roof | 6,000 |
| Floor, tunnel and supports | 3,000 |
| Vents and secondary details | 2,000 |
| Reserve | 5,000 |
| Total | 80,000 |

Keep 24 primitive/call proxy and 5,242,880-byte limits. No new runtime budget is requested until tests show that this allocation cannot achieve the required quality. The actual browser call count and hardware performance still need integration testing.

## Master / runtime recommendation
Maintain one authored Blender master with separate component objects, controlled surface modifiers, UV seams and physically plausible look-development materials. Derive a separate triangulated, tangent-checked, KTX2/Draco GLB. Do not use a destructive simplification of the only source. Master procedural microdetail is not a web texture bake; track parity explicitly. Use fixed cameras to compare the master and runtime derivative before claiming parity. The R3 source will preserve editable components, while exported candidates retain current material names and budgets.
