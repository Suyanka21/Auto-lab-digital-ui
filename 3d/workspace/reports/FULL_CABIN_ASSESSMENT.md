# Full-cabin assessment and canonical construction sequence
2026-11-18. Assessment complete; candidate geometry not yet authored.

## Evidence hierarchy
Primary: the actual 35 gallery photos plus corrected second-round documents from the new repository. Contact sheet inspected, not a claim that every fine detail was inspected at full resolution. Gallery 03 is promotional, 01/02/04/09/10/12/13/14 largely exterior/mechanical; do not count all 35 as cabin photos. Gallery 17 shows a roof opening; exact trim/roof option and dimensions remain provisional. PR5 correctly excludes four pressroom exterior photos from interior evidence. Gallery 11's identification plate merits separate source verification, not invented VIN/options conclusions.
Supporting only: earlier procedural-building and Dilum/Sanjaya reports. Their creator claims do not prove a hidden workflow. PR6 provides a displacement experiment, not an accepted front seat or a new baseline; it alters only driver/backrest stitching, leaving passenger mismatch and UV-stretch risks.
References are internal modelling aids, not cleared commercial imagery. Reproduce no badges, logos, wordmarks, screen art or steering emblem. Use neutral, original screen graphics and a neutral wheel centre.

## Current baseline, measured from GLB metadata
All three treatments: 11 mesh nodes, 10 material slots, 24 primitives and 66,260 triangles. Required extensions: KHR_draco_mesh_compression and KHR_texture_basisu. Bytes: Classic 3,650,764; Diamond 3,787,228; Perforated 3,509,764. Full hashes in baseline-inspection.json and download-inventory.json.
These are parsed accessor counts, not a decoded geometry/visual validation. Budgets remain 80,000 triangles, 24 calls and 5,242,880 bytes. Only 13,740 triangles remain; no primitive-count headroom. Do not silently relax them. Node/mesh merging is a possible optimisation, not proof of meeting the budget; it must preserve spatial/material contracts and be measured on exported candidates.

## Connected-cabin construction order
1. Establish candidate scope/manifest and a single metric coordinate frame. Retain baseline seats/console as placement anchors without claiming their dimensions are OEM. Map floor height, sill, tunnel, seating rows, door apertures and roof envelope together. Mark all photo-derived proportions provisional.
2. Complete major geometry: floor/carpet/footwells and tunnel; rear bench/headrests; four door cards; A/B/C pillars and roof/headliner with gallery-supported sunroof; rear vent housing and visible lower-cabin connections. Assemble as one coherent interior. Resolve seat-to-floor, dash-to-door, pillar-to-roof, console-to-rear-vent junctions before small details. No folding/kinematics claim.
3. Correct dashboard/console geometry and finish zoning: display hood, tiered passenger dash, climate/audio stack, glovebox/end cap, shifter boot, Remote Touchpad, drive-mode control, switch pod, cupholders and rear console. Refine steering bezels with unbranded hub. Preserve camera coordinates/orbit limits; use separate offline inspection views for newly added rear/roof zones.
4. Only after structural review: correct both front seats together, panel boundaries, channel seams, perforation and stitching; then refine leather, wood/metal/carbon, baked textures and reflections. PR6 may inform this, never supersede the full cabin priority.
5. Candidate-only KTX2/Draco export, gate and baseline comparison, low-resolution review renders. Preserve original production bytes. Document measured triangle/primitive/size changes and request a budget decision only if consolidation cannot meet limits. No device or browser performance claim without later integration evidence.

## Component reference map
| Component | Primary gallery | Limits |
|---|---|---|
| Front seats/headrests | 08,23,29,30 | Exact seam depths, foam dimensions, rails and upholstery grade unverified |
| Rear bench/headrests | 15,25,26,31,32 | Armrest/folding internals and measurements unverified |
| Front/rear doors | 24,23,25,31,32 | Hidden sections, exact audio trim and dimensions unverified |
| Dashboard/display | 07,16,18,20,33,35 | Display package, depth, HUD and dimensions unverified |
| Console/shifter | 07,19,33,34 | Depth/boot/hidden storage dimensions unverified |
| Steering controls | 21,22,33 | Neutral hub; do not reproduce emblem |
| Roof/pillars/sunroof | 17,15,23,25,29 | Roof dimensions, unseen rear junctions provisional |
| Floor/footwells/tunnel | 07,23,29,31,34 | Mats obscure geometry; no service/structural claims |
| Rear vents/controls | 31 | Controls below vents need closer inspection |

## Dashboard selection diagnosis and integration contract
Actual shipped GEO_Dashboard_Lexus has MAT_Dashboard_Trim, MAT_Console_Carbon, MAT_Cockpit_Black and MAT_Cockpit_Accent primitives. Thus missing carbon material on the entire dashboard is NOT supported by metadata. RuntimeViewer applies finish previews to MAT_Console_Carbon (shared by dashboard and console); configuration-adapter supplies fixed #2A2B2E to MAT_Dashboard_Trim. Seat colour controls deliberately do not recolour the upper dash. The reported invisible dashboard change may involve face coverage, occlusion, UVs or the distinction between fixed leather and decorative inserts; current browser reproduction is NOT TESTED under the no-app boundary.
Candidate requirement: assign visible passenger/central decorative trim faces to MAT_Console_Carbon, retain upper leather and vent/control faces on correct fixed slots, and record per-face/material coverage with offline material-ID views. Use one shared trim material across dashboard/console and test selection later in integration. Do not rename the slot merely because wood uses it. Do not recolour all dashboard surfaces to hide the defect.
Seven live colour/material bindings remain the legacy seven; the actual GLB has ten slots including console materials. Preserve all ten names and existing three-treatment contract. New parts need explicit mapping, not new UI controls. Preserve ORM alpha as the Diamond thread mask, UV0/tangent alignment, linear data maps and sRGB base maps. KTX2 UASTC quality2/RDO1.1/zstd9/mipmaps, Draco EDGEBREAKER speeds5, quantization position16/normal10/UV14/colour10/generic12 are recorded source settings, not newly executed output.

## Outstanding before build/acceptance
Isolated Node gate dependencies and path-safe candidate finalizer still need preparation; no npm dependency tree was downloaded. Gate requires a full-cabin candidate manifest and mutation checks before acceptance. Exact donor measurements/options remain open but do not prevent clearly labelled visible-geometry reconstruction. No replacement GLB, human visual acceptance, real-phone metric or finished-cabin claim is made at this checkpoint.
