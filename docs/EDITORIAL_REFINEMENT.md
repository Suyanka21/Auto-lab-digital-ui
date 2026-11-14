# Editorial showroom refinement
Owner-authorized implementation; 2026-11-14. Experimental repository only.
## Acceptance
Keep approved ivory/graphite/type tokens, live cabin, no-scroll Studio and contracts intact.
Replace generic landing photography with five original AI-generated material studies.
Magazine cover with finite camera-like image movement, masked word entrances, manual shot selection and pause; no forced wait or extra WebGL.
Tactile material/trim/colour/thread/composition choices, keyboard radio semantics and precise selected states.
Preserve illustrations versus actual 3D distinction; no workshop availability or finished-project claims.
Responsive 320/390/768/1024/1440; reduced-motion, failure recovery, actual browser evidence.
## Research
- https://carlexdesign.com/pages/carlex-dubai/ — directly viewed full-bleed showroom and gallery imagery; apply restrained captions and material-led hierarchy. No assets copied.
- https://www.polestar.com/global/polestar-4-models/polestar-4-coupe/interior/ — upholstery themes paired with named material choices; apply clear relationship between sample and live selection. No assets copied.
- https://us.loropiana.com/en/ — current seasonal/editorial product storytelling; supporting reference, not copied layout.
## Slices
1. Original imagery and cinematic editorial landing; verify navigation/motion/mobile.
2. Tactile selectors; preserve all configuration callbacks, no-scroll stage and keyboard behaviour.
3. Regression verification, screenshots, recording, evidence and owner handoff.
Rollback each slice by its local commit; no dependency or renderer changes.
## Image provenance
Five images generated with built-in image_gen, prompts in evidence/editorial/image-prompts.json.
Generated PNG originals remain in Codex generated_images; WebP encoding only in src/assets/editorial, no geometric evidence or model texture changes.
All images are illustrative AI material studies; samples are not colour-calibrated.
First asset-copy attempt failed on PowerShell directory argument syntax before any asset saved; corrected to an explicit path array.

## Implemented
- Magazine-cover landing: large asymmetric type, masked line entrances, 4.8-second finite image drift, three selectable editorial shots and Pause/Resume. No autoplay video file, extra WebGL context, forced wait, sound or perpetual animation.
- An interactive texture gallery, contrasting trim spread and concise route into the live Studio replace the former catalogue-style landing.
- Studio treatment study plus compact photographic choices; cut-leather colour samples, stitched thread samples, single/two-tone diagrams, trim board and light-wash samples.
- Existing palette, fonts, logo, navigation, selection IDs and callbacks remain. Photo crops are UI illustrations; no image is applied to the 3D model.
- One live viewer remains the centrepiece. Existing six-step rail, Back/Continue/swipe, four numeric camera presets, keyboard radios, disabled duplicate secondary colours, summary and recovery remain.
## Observed verification
- New landing controls: red reproduction 2 failures (missing new presentation), then desktop/mobile 2/2 PASS in 1.1m.
- Initial selector check: 2 failures caused by test-only wrong label Ambient Illumination. Actual step is Ambient Light; corrected, logs retained.
- Visual inspection found old card CSS taking precedence; moved sample CSS after base Studio styles, rebuilt, and rechecked.
- Final normal-build desktop/mobile selector journeys: 2/2 PASS in 1.6m. Screenshots show treatment, two-tone colour, thread, composition, trim and illumination with visible cabin.
- Live material-binding regression, unavailable-WebGL controls/summary and swipe/back/reduced-motion checks: 3/3 PASS in 2.9m.
- Renderer snapshot: 24 draw calls, 66,260 triangles, zero page errors, one canvas. Software Edge/SwiftShader; this is not a hardware GPU benchmark.
- 34 unit tests / 5 files PASS (6.92s). Final normal build PASS (3.53s); diagnostic build PASS (3.71s).
- Final main JS 265.02kB (81.50kB gzip); renderer 1,071.95kB (297.06kB gzip), unchanged in size. Existing >500kB warning remains.
- Five WebP files total 1,356,276 bytes. Source PNGs preserved; hashes in evidence/editorial/asset-manifest.json. No new dependencies or third-party imagery copied.
- Final gallery keyboard and 320/768/1024 viewport check: 1/1 PASS (12.9s), bringing focused browser checks to 8 passing scenarios. Final typecheck and lint PASS.
## Evidence links
- [Desktop cover](evidence/editorial/cover-1440.png) and [mobile cover](evidence/editorial/cover-390.png).
- [Desktop live Studio](evidence/editorial/studio-material-1440.png) and [mobile colour controls](evidence/editorial/studio-colour-390.png).
- [Landing interaction recording](evidence/editorial/presentation-1440.webm) and [live selector recording](evidence/editorial/selectors-1440.webm).
- Actual command logs, failure attempts, asset hashes and scene measurements: `docs/evidence/editorial/`.
## Limits
AI-generated illustrations are not photographs of actual workshop commissions, exact texture/colour matches, product stock or manufacturing approvals. The unchanged model retains its known visual defects. Real phones, Safari and hardware GPU performance were not tested. Seven previously recorded moderate development audit findings remain unresolved. No production-repository modification, push, merge or deployment.
## Change Summary
What was built: cinematic editorial showroom and tactile selectors using five original generated material studies.
Assumptions made: retain the approved Editorial Atelier identity, responsive platforms and working experiment; interpret film-like presentation as lightweight animated stills.
Edge cases handled: reduced motion, immediate Studio access, narrow screens, keyboard radios, disabled duplicate secondary colour, internal panel overflow.
Failure modes covered: existing WebGL fallback leaves controls and specification usable; viewer/loading contracts unchanged.
What was NOT covered: model refinement, commercial approvals, physical-device testing or literal generated video footage.
Confidence level: HIGH for tested functionality; visual judgement remains with the owner.
Reason: original contracts and actual browser material state were tested; screenshots and recordings are retained.
Tests added: presentation controls/reduced motion/navigation, tactile selector journeys and material-gallery keyboard/viewport checks.
Blast radius: experimental presentation components, generated UI images and browser tests only.
