# R4 refined — front-door review

**Status: focused refinement delivered for owner review. Final visual acceptance remains OPEN.**

The modelling direction was approved; this task authorises targeted refinement of the existing R4 front door only. The saved starting master, earlier R2/R3 work, original scripts and approved AI images remain protected. No runtime export or application work is included.

## What changed

| Area | R4 issue | Refined construction |
|---|---|---|
| Armrest | Inflated rounded cross-section and raised crest | Asymmetric cross-sections provide a sloping top deck, flatter front face and controlled thickness. The rising section follows the grab's path; the broad lower return retains an opening. |
| Pocket / speaker | Overlapping lip and pinched shoulder; overly broad opening | Intersecting surfaces were replaced. A smooth shoulder envelope and matching wall boundary remove the fold. The narrower opening has separate back, floor and side surfaces; a broad sloping right panel follows the corresponding reference region, with its exact shape still approximate. |
| Release / upper trim | Flat lever silhouette, uneven bezel and sharp terminal tip | A sloping scooped lever has real thickness and a stepped root. The bezel has a flatter satin face with a curvature-limited inset. The exposed carrier tip is tucked beneath the retained padded roll. |
| Leather / seams | Orange, uniformly smooth response; inconsistent support | Muted tan colour, controlled roughness variation and fine grain. Submillimetre local tension at the grab attachment; stitch rows reprojected onto the changed upholstery. |
| Wood / metal | Bright regular walnut and chrome-like highlights | Darker walnut with more grain warp and reduced coat; rougher satin metal. No reference pixels are used as surface textures. |
| Grille | Fine pattern lost at overview scale | Staggered round-hole alpha pattern over the existing acoustic backing. Provisional 2.4 mm pitch improves sampling at final resolution without modelling individual holes. |

This was a modification of the saved master, not a scene rebuild. The original carrier, upper roll, fascia, insert, controls, wood mesh, speaker face and review rig were retained; the carrier tip and insert received small local edits. The new checkpoint records exactly which base meshes are unchanged in master-metrics.json.

## Review evidence

- reference-comparison.jpg — approved primary AI image versus the refined frontal render.
- before-after.jpg — original R4 and refined front views using the same camera, framing and studio lighting.
- detail-before-after.jpg — original R4 versus refined handle and pocket close-ups using the same cameras.
- inspection-contact-sheet.jpg — seven actual refined inspection/presentation renders.
- PNG originals: front-reference, three-quarter, handle-release-closeup, pocket-speaker-closeup, release-trim-closeup, neutral-geometry, realistic-material; material-lab is supplemental.

All modelling evidence comes from Blender. Neutral geometry is diagnostic only; it is not evidence of material realism. Comparison sheets resize the images for display without retouching geometry, shading or defects. The primary AI image remains unchanged.

## Remaining limitations

- The grab attachment, armrest face thickness and lower return are closer in arrangement but remain interpretations of a single design image. They are not exact manufacturing geometry.
- The reference contains richer upholstery tension, more irregular wood grain and more nuanced control/lever details. The procedural master remains more uniform in places.
- Hidden pocket construction is inferred. The visible opening is modelled, but mounting hardware, manufacturing clearances and fit to the full cabin are unverified.
- Grille texture can alias or lose contrast when images are reduced; review the original close-up as well as the overview.
- The primary image has an unknown projection. Existing orthographic comparison framing is retained for honest before/after judgement; perspective mismatch is not treated as a geometry measurement.
- Presentation scale remains provisional (approximately 1.17 m by 0.86 m). The 2.4 mm grille pitch and material parameters are modelling choices, not OEM specifications.
- Procedural Blender materials and editable detail are not baked GLB equivalents. Runtime UV distortion, tangents, texture baking, shader compatibility and performance are outside this checkpoint.

## Verification scope

master-validation.json records fresh-open finite-coordinate/UV/material checks, component counts, stitch projections and targeted construction probes. The grip probe samples one selected viewing ray; the lip/grille check tests that particular pair. Neither proves global watertightness, collision-free assembly or visual acceptance.

preservation-check.json compares every file captured before refinement, including the original R4 checkpoint and earlier candidates, scripts, reports and reference assets. package-validation.json checks images, local links and the concise handoff. Actual final sample settings and dimensions are in render-manifest.json. Full command evidence is retained in build.log, master-validation.log and final-render.log.

Original R4 remains 925,924 evaluated triangles. The fresh-open refined master has 48 mesh components, 50,916 base vertices and 719,424 evaluated triangles. Lower subdivision on replaced surfaces is an authoring choice, not a runtime optimisation result. Complete-cabin runtime limits remain 80,000 decoded triangles / 24 primitives / 5,242,880 bytes per GLB.

No GLB gate, browser, phone or GPU performance test applies to this master-only delivery. No such results are claimed. No human gate has been closed.

## Inspection and stop condition

The two pilot directories preserve the bounded correction process: the first preview exposed an overly thin grab; the second prompted cross-section alignment, bezel-corner correction and grille sampling adjustment. These were checks within the authorised refinement, not a new cabin phase.

Please judge the refined silhouette, armrest/handle integration, pocket/speaker junction, release housing and material credibility against the supplied comparisons. The final image inspection notes are in INSPECTION.md. This checkpoint is presented for your decision; it does not record your acceptance.

No rear doors, other cabin components, runtime optimisation, new dependencies, modelling-skill package, workspace transfer, push or merge was undertaken.


## Advisory image comparison

The realistic-3d-craft helper was run against the final front render and unchanged primary image. reference-signals.json records silhouette-mask IoU 0.774, strong-edge IoU 0.155 and luminance-histogram overlap 0.781. These are raw image signals, not percentages of accuracy or acceptance criteria. Border-based foreground segmentation, different backgrounds/lighting, unknown AI projection and the helper's 512-square resize confound interpretation. The low edge overlap supports continued visual scrutiny; it does not identify an exact modelling error by itself.
