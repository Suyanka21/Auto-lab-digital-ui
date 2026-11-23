# R4 — front-door master review

**Checkpoint: OWNER REVIEW. Visual acceptance remains OPEN.**

## What was reconstructed

One front-door component was rebuilt in the isolated workspace from the approved primary AI design. The alternate supplied depth context only. Image-space landmarks establish the outline, release centre, speaker centre, upper grip attachment and pocket lip. They are design guides, not manufacturer measurements. Presentation scale is approximately 1.17 m wide and 0.86 m tall; cabin fit is unverified.

The editable master uses section-controlled quad surfaces and variable-section lofts for padded regions and the integrated grip/armrest. Separate release recess walls and back, pocket floor/back/end walls, supported grip return and speaker shoulder communicate construction depth. Bevels and subdivision remain editable. The master contains 48 mesh components and 925,924 evaluated triangles; the detailed breakdown is in COMPONENTS.md. This is intentionally a development master, not an 80k runtime candidate.

## Reference correspondence and remaining discrepancies

| Region | Reconstructed correspondence | Remaining discrepancy |
|---|---|---|
| Silhouette | Taller panel proportions, curved lower edge, primary-reference handing and lower-left speaker | Side curvature and corner radii remain approximations; the AI projection is unknown. |
| Upper assembly | Padded black roll, continuous walnut strip, thin metallic reveal and recessed release housing | Release lever still reads as a simplified shape; bezel junctions and memory controls need closer reference fidelity. |
| Upholstery | Sloping tan insert with a defined perimeter and curved grip flowing into a broad palmrest | Padding is too uniformly smooth; armrest crest, thickness distribution and insert taper differ visibly. |
| Grip support | Visible underside return, rear attachment and an actual opening | Opening shape and support integration are not identical to the reference; abrupt transitions remain. |
| Pocket | Open top with real rear/floor/front/end surfaces, clear of speaker face | Lip height/profile and the interior subdivision differ; cavity depth is inferred. |
| Speaker | Contoured shoulder, thin ring, domed perforated shader over a dark backing | Surround bulge and grille density/readability differ from the reference. |
| Materials | UV-driven leather, satin metal, walnut and structural plastic | Leather grain/stitches are weak at overview; wood is too uniform and bright; some highlights still make upholstery read as moulded plastic. |

No exact geometric match, manufacturing fit or premium visual acceptance is claimed. The original AI image is unchanged and is not pasted onto model surfaces.

## Difference from R3

R3 assembled broad generic patches and rounded members under a nearly exhausted runtime budget. R4 is a separate single-door master with primary-reference proportions, deliberate paired boundary curves, section-based padding, a variable-width grip/palmrest and actual recess/pocket walls. It does not derive a runtime representation or replace R3.

Three construction reviews were performed. Round 1 exposed a pocket wall crossing the speaker and an oversized lower surround. Round 2 corrected those but revealed a twisted leading moulding and poorly attached stitch placement. Round 3 corrected boundary ordering, projected stitches onto evaluated upholstery, reduced bezel width and rounded the armrest termination. Earlier round sources, masters and preview critiques remain in round-1/ and round-2/. Further visual changes await owner review.

## UV and material work

Every mesh has a finite Surface_Metres UV layer and assigned material. Upholstery strips use continuous per-component coordinates; grip sweeps use path-length coordinates; planar trim uses planar coordinates. This is not a verified runtime UV unwrap: distortion, overlaps and bake suitability still need later assessment.

Leather uses metre-scaled procedural grain with subtle colour and roughness variation. Stitch geometry is projected to evaluated target surfaces. Walnut uses UV-driven stretched/warped noise; satin metal uses rough metallic response; the speaker uses a procedural perforation/alpha treatment over separate backing. These are Blender master shaders, **not baked GLB equivalents**. Master material names and proposed role notes do not change runtime slots.

Six realism-layer assessment: silhouette improved but approximate; bevelled edges present; micro-detail exists but lacks convincing final readability; material response remains too uniform in places; fixed soft studio lighting exposes depth; natural upholstery wrinkles/tension variation remain insufficient. Material-lab images are evidence of current response, not proof of acceptance.

## Evidence and validation

- Seven actual Cycles CPU renders: front, three-quarter, grip/release close-up, pocket/speaker close-up, neutral geometry, material presentation and material lab. PNG originals are included.
- Final samples: 64 for overviews/lab, 96 for close-ups; AgX Medium High Contrast, exposure 0, denoising enabled. Exact image sizes are in render-manifest.json.
- Front uses primary 1200:670 aspect and approximate orthographic framing. Three-quarter views expose depth; the AI reference camera is unknown. Comparison crops are resized analytical views, not changes to the source.
- Fresh-open master checks: required components, finite vertex/UV data, UV/material presence and evaluated geometry counts. See master-validation.json for actual results. These checks do not prove manifoldness, collision-free assembly, cabin fit or visual quality.
- preservation-check.json compares all 177 previously snapshotted files, including references, earlier masters/candidates, scripts and baseline assets. Earlier review reports remain retained.
- Runtime GLB gates, browser, GPU and phone performance: **NOT RUN for R4**, because no runtime asset or application integration is authorised. No performance estimates are presented as measurements.
- Existing runtime limits remain 80,000 decoded triangles / 24 primitives / 5,242,880 bytes per complete-cabin GLB. This master must not be loaded into production as-is.

The earlier interrupted final-render attempt produced no final image evidence. The retained final-render.log records the subsequent completed run; preview images are separately labelled.

## Scope protection and next decision

No runtime export, optimisation, other-door replication, seat stitching replacement, new baking pipeline, viewer change, dependency installation, remote write or production promotion was performed. Existing seven bindings and treatment behaviour are untouched. Diamond-only thread-mask behaviour does not justify removing stitch geometry from every treatment.

**Ready for owner inspection, but I do not recommend treating it as visually finished.** Please judge the silhouette, upholstered transitions, supported grip, release housing, pocket/speaker construction and material credibility against the comparison. Approval or correction direction is required before optimisation or any additional cabin work. No human gate is closed.

### Supplemental inspection evidence

The fresh-open audit counts 54,782 base vertices and 958 successfully projected stitches (zero skipped). Evaluated subdivision is dominated by the upholstery insert (172,656 triangles), pocket front wall (166,736), upper roll (123,440), rear armrest support (83,216) and walnut insert (79,568). These counts describe the current editable master; they are not a proposed runtime allocation or an optimisation result.

The skill's advisory raster comparison reports silhouette-mask IoU 0.764 and edge-mask IoU 0.160. These are not fidelity percentages or acceptance scores: the helper resizes both frames to a square and estimates foreground from the border colour, while background, lighting and unknown AI perspective differ. The raw JSON is retained for traceability; visible component discrepancies take precedence.

The final frontal render also exposes a sharp upper-right trim termination and a speaker surround close to the lower edge. Both remain review defects. The source reference is 2752 x 1536 pixels; the 1200 x 670 frame used for landmarks is an analytical resize, not the original image resolution.

Final pocket inspection identifies an additional priority correction: a pinched/folded speaker-to-pocket junction at the upper-right edge of the speaker shoulder. The grille's fine pattern is visible in the full-size close-up, but its overview response remains unlike the reference. The pocket's missing reference-specific interior division is also unresolved.
