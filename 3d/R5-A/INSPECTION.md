# R5-A form assessment — owner decision open

**Decision requested:** accept or revise the backrest shoulder/bolster volume, cushion nose and headrest proportions **before** splitting the upholstery into panels. Do not use a seam, texture or lighting change to disguise a form correction.

| Area | What the actual renders show | What remains open |
|---|---|---|
| Shoulders and lumbar | The front is broad rather than shield-shaped. Side and neutral views show real thickness, a forward lumbar roll and a shoulder return. | The primary breaks more distinctly from the upper shoulder into the lower bolster. Ours is straighter and more uniform through that turn. Unknown lens and recline make the single-image depth ambiguous. |
| Cushion and junction | A continuous front roll meets the dark apron. The pan sinks towards the backrest; the outboard bolster rises beside it. | The reference has a more distinct outer cushion crest. The study's front roll looks heavier and more continuous across its width. The foam junction under the backrest is still a close-fitting blockout, not upholstery construction. |
| Restraint and rear | Separate low headrest and two short posts. The rear carrier follows the back rather than hanging behind it. | The headrest crown reads flatter and its corners squarer than the primary. The carrier is a broad, plain envelope inferred from the cabin image; the primary cannot establish its rear contour. |
| Base | Independent dark shields, round and paddle controls, open runners and bent feet read separately in neutral. | The side field lacks the primary's recessed control surround; the lower apron ends and rail supports are simplified. Attachment and travel are unverified. |

The smooth, unperforated centre is intentional. No upper insert break, flutes, seam gutters, stitches, grain, branded tag or commercial material claim at this gate. The reference comparison mirrors only the **render on the plate** so outboard silhouettes face the same way; the raw PNG and actual driver-side mesh are not reflected.

## Placement: evidence versus inference

The before/after uses the actual shipped Classic cockpit at identical coordinates and camera. Only its driver seat and stitching are hidden in the second frame. The unchanged passenger is **not** a proposed variant. Compared with the original seat bounds, the top of the headrest is within 1 mm, the new foremost point is 18 mm farther forward, and the feet are 66 mm lower. These are differences between two digital models, not measurements of a vehicle.

An evaluated triangle-surface intersection check found no crossing with the **nine** retained cockpit nodes at this static pose. It does not test containment, moving controls, door swing, roof/headroom, occupant comfort, or whether feet meet a floor. The reference camera is uncalibrated; neither installation depth nor anchorage is known. A floor/rail mounting-plane height and a measured cushion width and backrest height would reduce the main uncertainties.

## Review and validation record

Three geometry passes, all in the Devin VM with Blender 5.2.2 LTS. No external model or texture. The tool interface did not offer a per-task Astra 6.2 selector.

1. **Pilot:** three-quarter plus orthographic side/rear exposed a pinched cushion nose and a fork of exposed rear cover at shoulder height. Front and rear of the side shields also terminated abruptly.
2. **Section revision:** a sagittal section running over the nose removed the pinch. Coordinated cross-sections gave the front apron and side shields a continuous outline. The camera was backed off for foot clearance; the lighting stayed fixed. The open rear shell's thickened rim still caught an irregular bright edge, and the cushion end cap inherited the centre study colour.
3. **Published form:** rebuilt the rear cover with sampled inner and outer skins and a rounded return; assigned the cap to the surround and broadened the shoulder return. The side, rear and neutral views no longer show the pilot's fork or nose pinch. The remaining differences are identified above, not treated as accepted. Five isolated views rendered in about 152 seconds combined; placement views use the separate, fixed doorway camera.

**Data checks:** 26 editable meshes, 3,705 cage vertices, 89,920 evaluated triangles, one packed reference, no missing materials/UV layers or non-finite geometry in the master audit. The evaluated count is for the detailed Blender source, not a runtime allocation. Ten local checks passed: nine-point sampled cover offset, four post contacts, three control contacts and two dual-zone checks. A clean rebuild reproduced the same evaluated geometry digest and probe results. Future runtime work must budget the entire cabin; no optimisation, bake or export has begun.

**Protected baseline:** frozen R4 SHA-256 `15bb8cecfdc0fff9d011bb159792a2076d24bfa67318a4f9198f992b64ec85e2`. No diff to the archived workspace, app, viewer, shaders, cameras, dependencies or shipped assets. Typecheck, lint, 58 unit tests, production build and all three baseline asset gates passed. No browser or device performance claim.
