# AutoLab AI 3D Generation Technical Guide

**Prepared for:** AUTO LAB™ SERVICES  
**Research subject:** AI-assisted generation of sophisticated interactive 3D experiences  
**Repository context:** [Suyanka21/Auto-lab-digital-ui](https://github.com/Suyanka21/Auto-lab-digital-ui)  
**Author:** Manus AI  
**Research status:** Evidence-led technical guide; no repository files were modified.

## 1. Executive findings

AutoLab should treat AI-assisted 3D development as a controlled engineering pipeline, not as a single prompt that magically produces a finished showroom. The repeatable pattern is:

> brief → scene specification → generated code/assets → runtime scene → screenshot and state inspection → bounded correction → acceptance tests → profiling → export and provenance

The strongest public evidence supports AI as an agentic builder and refiner of code, procedural geometry, materials, scene logic and tool calls. It does not support the assumption that a model independently creates production-ready automotive topology, UVs, PBR maps, shaders, animation, interaction and performance in one pass.

Dilum Sanjaya’s public V8 post is a useful motivating example. Dilum says that he asked GPT-6 Astra to create a highly detailed interactive V8-engine visualization and found the result impressive.[1] That verifies a public creator claim and a publicly attached video. It does **not** reveal the prompt, source code, runtime, geometry method, material definitions, shader graph, animation equations, tool trace or performance measurements. Repost captions add claims about a cross-plane V8, firing-order visualization, RPM controls and part isolation, but those details are secondary commentary and were not independently tested.[2] AutoLab should therefore study the post as evidence of an ambitious creative result, not as a reproducible technical specification.

The most technically inspectable comparable is OpenAI’s published Void Explorer workflow. Its documentation describes a live TypeScript, Vite and Three.js application with procedural geometry, seeded planets, streamed terrain, level of detail, WebGPU/TSL materials, atmospheric and water effects, stateful flight/landing/walking interaction, renderer counters, browser tests and screenshot-based iteration.[3] The important lesson is not the model name. It is the division of responsibility: an AI agent can help create and revise a normal real-time 3D application, while the application still needs scene structure, runtime constraints, tests and human review.

Public Blender-agent work points to a complementary loop: inspect the current scene, plan a bounded operation, generate and execute `bpy` code, capture a viewport image, compare it with the target, then correct the next defect.[4] The author reports better results from screenshot feedback than from blind multi-step execution, but this remains creator-reported evidence rather than an independently reproduced benchmark. Blender is the stronger authoring and inspection environment when topology, UVs, modifiers, baking, rigging or editable source geometry matter. Three.js or React Three Fiber is the stronger delivery environment when the result must run in the browser with live controls, camera states, material selection and application UI.

Image-to-3D systems such as Stable Fast 3D, TripoSR, InstantMesh, TRELLIS and Hunyuan3D demonstrate real mesh-producing workflows, but they solve a different problem from AutoLab’s full cabin. Their outputs require inspection, remeshing, UV review, texture generation or baking, rigging where applicable, and target-runtime profiling.[5] A single image cannot fully specify hidden surfaces, physical dimensions, topology or mechanical relationships.

For AutoLab, the recommended approach is hybrid and staged:

1. Preserve the current Lexus RX viewer contracts and use AI to create **bounded asset or shader changes**, not uncontrolled replacements.
2. Use Blender Python or Geometry Nodes for editable component construction, repeated upholstery detail, stitching guides, panel splits, starlight-fibre placement and offline inspection.
3. Export tested GLB assets into the existing R3F/Three.js viewer.
4. Use runtime shaders and material maps for configurable appearance; avoid adding geometry for every visual detail.
5. Provide screenshots, scene manifests, measurements and renderer counters to the AI after every meaningful change.
6. Reject any result that looks good in one render but fails naming, texture, camera, load, interaction or performance gates.

Astra’s public evidence is strongest for code-driven and tool-assisted 3D systems. Claude Fable’s public material makes broad claims about interactive 3D worlds, simulations and animations, but exposes less reproducible implementation detail.[6] The combined name “GPT-6 Fable” is not established by the authoritative sources reviewed here. AutoLab should refer to OpenAI’s Astra and Anthropic’s Claude Fable as separate products until an authoritative source says otherwise.

## 2. What the public evidence establishes about Dilum Sanjaya

### 2.1 Public identity and source trail

Dilum Sanjaya’s public site identifies him as a software engineer and creative coder and links his YouTube, X, GitHub, CodePen and AI Lab.[7] The AI Lab catalog presents many experiments in science, robotics, engineering, games and interactive applications.[8] His separate Handcrafted page documents manually written Three.js, WebGL, canvas and React work.[9] The distinction matters: a hand-authored Three.js demo is evidence of the creator’s technical interests, but it is not proof that every AI Lab experiment uses the same framework or code pattern.

The public profiles are useful discovery sources. They are not a substitute for source code or a technical build record. In the reviewed pages, no matching public V8 repository, prompt transcript, asset package, renderer diagnostic or reproducible build instruction was found.[1] [7] [8]

### 2.2 The V8 visualization

Dilum’s original X post says:

> “Asked GPT-6 Astra to create a highly detailed, interactive visualization of a V8 engine. The result is pretty impressive.” [1]

The post has an attached video. This establishes four facts: the post is public, Dilum authored it, he attributes the request to GPT-6 Astra, and he presents a video result. It does not establish whether the video shows a live browser or desktop runtime, a pre-rendered animation, a composited recording, or a hybrid.

Secondary reposts describe a more specific feature set: transparent or cross-plane engine components; crankshaft, piston, connecting-rod, camshaft and valve motion; firing order `1-8-4-3-6-5-7-2`; chamber-pressure and valve-timing displays; RPM controls; multiple cameras; cutaways; part isolation; and colour-coded strokes.[2] Those details are plausible for an educational V8 visualizer, but they are claims made by repost channels, not statements in Dilum’s original text. They must not be converted into verified requirements without direct inspection or source release.

If the result is a live 3D application, a technically plausible implementation would require a scene graph, named engine assemblies, parent-child transforms, a crank-angle source of truth, UI event handling, camera state, material state and a render loop. A typical kinematic model would derive piston and connecting-rod positions from crank angle, derive cam/valve timing from phase relationships, and derive cylinder colour or pressure display from a firing-order state machine. This is engineering inference, not a reconstruction of Dilum’s private workflow.

The public evidence does not answer the following questions:

- Which runtime was used: Three.js, React Three Fiber, Babylon.js, Unity, Unreal, custom WebGL/WebGPU, Blender playback or another system?
- Did Astra write procedural geometry, Blender Python, application code, or only orchestrate existing assets?
- Are the engine dimensions educationally or mechanically accurate?
- Are the visible materials authored PBR maps, procedural shaders, environment-lit standard materials, baked renders or composited video layers?
- Are the pressure and timing displays connected to a real simulation, a kinematic visualization or a scripted presentation?
- What are the triangle count, draw calls, texture sizes, shader cost, frame time, memory use, loading time and supported devices?

AutoLab should use the V8 example as a target for **communication quality and system decomposition**, not as proof that a single model can deliver production-ready mechanical engineering content without verification.

### 2.3 Other public Dilum examples

The AI Lab and linked posts provide more useful methodological clues than the V8 post alone:

- A Cell Architecture Studio experiment presents generated biological structures in an interactive application. Dilum says the UI design used GPT Images 2 and the code used Gemini 3.1 Pro, and says he tried Tripo and Hunyuan3D for 3D structures, preferring Tripo subjectively.[10]
- A tank/schematic experiment is described as fully generated with code and easy to replace with another object.[11] This is evidence for a code-defined or parametric scene claim, not proof of specific mesh topology.
- A hexapod simulator is described as using inverse kinematics and gait algorithms written from scratch.[12] Another related post attributes a simulator to Claude Opus and an open-source robot algorithm.[13]
- A warehouse digital twin is described as a game-like industrial management experience built with an Opus model.[14]
- A separate public video describes a character workflow involving image generation, a 3D generation service, Mixamo rigging and React Three Fiber/Three.js animation.[15]

These examples support a recurring pattern: use different tools for concept imagery, 3D asset generation, rigging, application code and runtime presentation. They do not prove that Dilum uses one universal secret prompt or one model-specific pipeline.

### 2.4 What AutoLab should learn from the evidence

The defensible lesson from Dilum’s public work is not “ask a model for an impressive V8.” It is:

- State what the experience must let a person inspect or control.
- Divide the result into named systems: geometry, animation, materials, lighting, camera, UI and validation.
- Choose a representation that remains editable.
- Ask for a working vertical slice before asking for visual abundance.
- Feed screenshots and measured state back into the next instruction.
- Preserve what already works and make changes local and reversible.
- Publish enough provenance that another engineer can tell what was generated, what was imported and what was hand-corrected.

## 3. Astra, Claude Fable and the actual AI-to-3D question

### 3.1 GPT-6 Astra

OpenAI’s public Astra material describes a general agentic model used for coding, computer use, research and professional work. The official material includes a BenchCAD example that reconstructs 3D objects from multi-view renders by generating CAD code, and a Blender-to-Unreal walkthrough in which a house becomes a walkable scene.[6] These are important because they describe executable design or application workflows rather than merely generating a still image.

The Astra developer write-up for Void Explorer is more valuable for AutoLab than the marketing claim itself. It describes a TypeScript/Vite/Three.js application with procedural geometry, more than ten thousand procedurally generated planets, seeded terrain, chunk streaming, quadtree refinement, LODs, Web Workers, local-coordinate precision, atmospheric and water effects, TSL/node materials, interaction states and browser-facing test hooks.[3]

The article also describes explicit verification. A `window.__VOID_EXPLORER__` interface exposes state and counters. Named test scenes and Playwright journeys exercise flight, landing, walking and reboarding. Screenshots and renderer counters are used alongside functional checks. Published timing comparisons are environment-specific headless Chromium/SwiftShader measurements, not universal GPU FPS claims.[3]

The strongest interpretation is therefore:

> Astra is publicly evidenced as an agentic coding and tool-orchestration system that can help build a real-time 3D application. The public evidence does not establish that Astra is a dedicated autonomous mesh generator, topology author, PBR authoring system or substitute for asset engineering.

### 3.2 Claude Fable

Anthropic’s public Fable material describes Claude Fable 5.2 as a model with text/image input, vision, tool use and agentic coding capability. Anthropic says that Fable can build interactive 3D worlds, simulations, animations and educational videos in code, and publishes a customer testimonial about generating 3D scenes from scratch and reconstructing a visual reference.[6]

Those statements are useful capability claims, but the checked official material does not expose a comparable public Fable project with source, mesh export, UVs, materials, shader definitions, renderer diagnostics, interaction tests or performance measurements. The claim is therefore broader and less reproducible than the Astra Void Explorer evidence.

AutoLab should evaluate Fable the same way it should evaluate any model: ask for a bounded artifact, require a trace of files and tool calls, inspect the scene and maps, and run the target acceptance suite. Do not treat a vendor phrase such as “build interactive 3D worlds” as proof that the model directly emits production-ready geometry.

### 3.3 The “GPT-6 Fable” naming problem

The public sources reviewed distinguish OpenAI’s Astra from Anthropic’s Claude Fable. No authoritative source reviewed here establishes “GPT-6 Fable” as an OpenAI model name. It may be a conflation of two separate products or a name used in secondary discussion. AutoLab’s documentation should write “OpenAI GPT-6 Astra” and “Anthropic Claude Fable” separately, with model version and date recorded for every experiment.

## 4. AutoLab’s current technical starting point

The public AutoLab repository is already a real interactive 3D showroom, not a photographic mockup. Its README describes an editorial showroom around a live 3D front cabin, with upholstery, colour, thread, trim, ambient-light and camera controls.[16]

### 4.1 Current runtime architecture

The viewer uses React Three Fiber and Three.js. It loads GLB assets with `useGLTF`, uses `OrbitControls`, creates a `RoomEnvironment` PMREM, applies KTX2/Draco decoding, and keeps the configuration state in React memory.[17] The current code exposes a diagnostic `window.__autolab.snapshot()` hook containing viewer status, asset URL, material state, renderer counters, errors and camera state.[17] This is exactly the sort of observable contract an AI-assisted asset workflow needs.

The current viewer has seven active Lexus material bindings:

- `MAT_Seat_Primary`
- `MAT_Seat_Secondary`
- `MAT_Seat_Stitching`
- `MAT_Steering_Leather`
- `MAT_Dashboard_Trim`
- `MAT_Cockpit_Accent`
- `MAT_Cockpit_Black`

The loader rejects incomplete seat contracts and verifies that primary and secondary seat materials contain base-colour, normal and roughness/ORM textures.[17] This means a visually attractive generated GLB that omits a required map is not an acceptable AutoLab asset.

### 4.2 The thread shader contract

AutoLab’s Diamond treatment does not add individual stitch geometry. The existing `thread-mask.ts` hook patches `MAT_Seat_Primary` using `onBeforeCompile`; it samples the alpha channel of the roughness map and mixes the existing stitching material colour into the seat shader.[18] The program cache key includes `autolab-l4a-thread-v1`.

This is a critical lesson for AI prompting. If a model is asked to “add realistic stitching,” it must not independently invent a new material slot or move the mask to another channel. The task must say that the existing ORM alpha is the thread mask, that the shader hook must remain compatible, and that any change to the sampler or cache key requires a corresponding test and controlled migration.

### 4.3 Asset, decoder, camera and performance contracts

The repository’s 3D compatibility roadmap records the following gates:[19]

- Keep all ten existing material names; never rename existing slots.
- Keep base, ORM and normal maps for seat slots.
- Keep the thread mask in ORM alpha unless the shader and test contract are intentionally migrated.
- Preserve trim UV scale or rebake the KTX2 trim maps.
- Serve Draco and Basis decoders locally rather than switching to an untracked CDN.
- Update asset cache revisions with the asset SHA-256 in the same change.
- Keep all four camera presets valid; orbit distance is bounded from `0.35` to `4` and panning is disabled.
- Current budget: 66,260 triangles per GLB, a hard limit of 80,000; 24 draw calls per GLB; and 3.51–3.79 MB current GLB size with a 5,242,880-byte cap.

Any AI-generated AutoLab asset must be evaluated against those constraints before it is considered a candidate. An owner may approve a budget change, but a model must never silently increase the budget because it produced more detail.

### 4.4 What AutoLab has and lacks

AutoLab already has:

- A working R3F/Three.js browser runtime.
- Three treatment GLBs for Classic, Diamond Quilted and Perforated upholstery.
- Named material bindings and map validation.
- KTX2/Draco decoding.
- A PMREM room environment and controlled lighting.
- Four camera presets and orbit limits.
- Live colour, thread, trim and ambient-light state.
- A shader-based thread mask.
- Diagnostic snapshots and browser validation patterns.

AutoLab still lacks a fully modelled and shared full-cabin assembly for all intended zones. The roadmap explicitly notes that loading front cabin, doors, rear seats and headliner as separate zones will require a design for shared material instances so one colour choice reaches every part.[19] It also notes that new trim zones need an owner decision about whether to reuse `MAT_Console_Carbon` or receive a new slot.

Therefore, the first AI-generated improvement should not be “generate the entire Lexus interior.” It should be one measurable component or one compatible material treatment that can be loaded behind a test-only switch, inspected and rolled back.

## 5. How an AI model turns instructions into a 3D experience

An AI model does not turn language directly into a reliable interactive object through one mysterious operation. It produces intermediate representations. The quality of the result depends on whether those representations are explicit and testable.

### 5.1 The seven-layer specification

Every AutoLab generation request should define these layers:

1. **Purpose and user action.** What the customer should inspect, compare or change.
2. **Scene schema.** Objects, names, hierarchy, transforms, dimensions and relationships.
3. **Geometry representation.** Imported GLB, Blender mesh, Geometry Nodes, procedural Three.js geometry, shader-only detail or a combination.
4. **Surface representation.** Base colour, normal, ORM/roughness, metalness, height, UV set, texel density and colour space.
5. **Presentation.** Camera, environment, lights, shadows, exposure, tone mapping and background.
6. **Interaction and state.** Controls, input events, camera presets, selection, isolation, animation or configuration state.
7. **Acceptance and budgets.** File format, material slots, map presence, triangles, draw calls, payload, frame time, tests and rollback.

A vague prompt says, “Make a realistic Lexus seat.” A useful prompt says what the seat is for, what geometry must be preserved, how the seams are represented, which material slots are permitted, how it will be exported, which cameras must show it, and which checks determine acceptance.

### 5.2 Geometry representation choices

Use primitives and procedural geometry when the form is regular, repeated or parameter-driven: ribs, perforation layouts, starlight fibres, stitching guides, vent slats, button grids, fasteners, piston assemblies or repeated quilting diamonds.

Use Blender Python or Geometry Nodes when geometry must be inspected and edited offline, when modifiers and UV tools matter, or when the asset will be reused across multiple runtimes. Blender’s Python API exposes scene and mesh data through `bpy` and `mathutils`; Geometry Nodes provides a modifier-based graph for meshes, curves, point clouds, volumes and instances.[20]

Use imported GLB/glTF when an authored or scanned asset already contains useful topology, UVs, materials and hierarchy. Ask AI to inspect and modify the asset rather than replace it when the existing geometry is a proven baseline.

Use image-to-3D systems for concept exploration, rough accessory forms and candidate assets. Do not treat their output as an automatic replacement for a measured automotive interior. Hidden surfaces, topology, UVs and dimension accuracy remain uncertain.

Use shader or texture detail instead of geometry when the detail is small relative to the viewing distance: fine grain, perforation impressions, subtle leather pores, weave, micro-scratches and small stitch colour variation. Use geometry when the silhouette, occlusion or parallax must change at the target camera distance.

### 5.3 Mechanical relationships

Mechanical assemblies should be represented by a small number of source parameters and derived transforms. For a V8-style demonstration, use one crank-angle value and derive:

- crankshaft rotation;
- piston height from crank throw and rod length;
- connecting-rod rotation from the piston and crank pin;
- camshaft phase from crank angle;
- valve lift from cam profile;
- cylinder phase from firing-order state;
- chart and colour state from the same cylinder event data.

Do not ask an AI to independently animate each piston, chart and colour. That creates drift. Ask it to create a single state model and make every view subscribe to that model.

For AutoLab, the same principle applies to shared materials. One configuration state should map to named runtime bindings. The repository already uses a configuration adapter as the single place where UI state becomes material values.[19] New AI-generated components should consume that state rather than adding a second configuration store.

### 5.4 Materials and shaders

A convincing material is not a colour swatch. It is a relationship between geometry, UVs, maps, shader semantics and lighting. At minimum, define:

- base colour/albedo and its colour space;
- normal map convention and strength;
- roughness or ORM packing;
- metalness semantics;
- optional height or clearcoat;
- UV set, orientation, scale and texel density;
- mipmap and compression policy;
- environment and light used for validation.

Ubisoft’s CHORD research prototype demonstrates a useful material workflow: a tileable texture is generated or supplied, SVBRDF maps are estimated sequentially, and the result can be upscaled.[21] The project predicts base colour, normal, height, roughness and metalness, but explicitly describes itself as an R&D/artist-assistance prototype with limitations at 1024 resolution, error accumulation during upscaling and difficulty with strongly specular metalness.[21] AutoLab should use this pattern as a research reference, not assume the maps are production-ready.

For AutoLab, inspect each map separately under a neutral material preview and test the final surface under at least neutral, grazing and coloured environment lighting. A beauty render alone can hide a wrong normal orientation, incorrect roughness scale or tiled leather pattern.

### 5.5 Interactivity

A result qualifies as an interactive 3D experience when it contains runtime geometry or a runtime representation, a camera and lighting state, input-driven state changes, and a renderer that responds to those changes. A turntable video is not sufficient evidence.

React Three Fiber maps JSX elements to Three.js objects and supports geometry, standard materials, lights, animation and pointer events.[22] The public Hanashi project demonstrates a real R3F scene graph with GLTF content, lights, camera components, Leva controls, Bloom, ToneMapping and ordered dithering.[23] Its polish should not be mistaken for proof of complex geometry, but its inspectable source shows the difference between a rendered image and a runtime scene.

## 6. Prompting methodology for AutoLab

### 6.1 Prompt structure

Use this structure for serious requests:

```text
ROLE
You are an automotive 3D asset and runtime engineer working inside an existing AutoLab repository.

OBJECTIVE
Create or modify exactly one named component for the 2020 Lexus RX 350 interior.

CURRENT BASELINE
Describe the existing asset, material slots, camera presets, shader hooks and tests. State what must not change.

GEOMETRY SPECIFICATION
Name objects, coordinate system, dimensions or proportional references, hierarchy, symmetry, seams, clearances and articulation.

MATERIAL SPECIFICATION
Name allowed material slots, required maps, UV set, texel density, colour space, map packing, roughness/metalness semantics and lighting assumptions.

RUNTIME CONTRACT
State whether the output is Blender source, GLB, Three.js code, a shader, maps or a test fixture. State the import path and required runtime bindings.

BUDGET
Set triangle, draw-call, file-size, texture-memory and frame-time limits before generation.

ITERATION RULE
Preserve approved geometry. Make one bounded change. Do not rebuild unrelated objects. Report changed files and hashes.

VALIDATION
Run asset, material, camera, interaction, screenshot and performance checks. Return failures instead of hiding them.
```

### 6.2 Reference images

Provide references by purpose rather than as a random image pile:

- orthographic or multi-view references for proportion;
- close-ups for seam, leather and stitch scale;
- lighting references for mood, not geometry;
- material swatches for colour and roughness direction;
- sketches or masks for panel boundaries;
- screenshots of the current runtime for regression comparison;
- a scene manifest that names the expected object and material relationships.

Tell the model what each image is allowed to influence. For example: “Use image A only for seat silhouette, image B only for stitch spacing, image C only for warm environment lighting. Do not copy the dashboard colour from image A.” This reduces accidental blending of incompatible references.

### 6.3 Controlled iteration

Ask for one of four operations, not an open-ended rewrite:

- **Inspect:** report current objects, materials, maps, bounds, cameras and counters.
- **Add:** create one named object or material treatment without replacing existing work.
- **Refine:** change one measurable property while preserving all other contracts.
- **Diagnose:** explain a screenshot or test failure, propose the smallest fix, then wait for approval if the fix crosses a contract boundary.

After each operation, require a compact change report:

```text
Changed:
Preserved:
Files and hashes:
New objects/materials:
Renderer counters before/after:
Screenshots captured:
Tests passed:
Known uncertainty:
Rollback procedure:
```

## 7. Practical AutoLab prompt examples

The following prompts are templates. They are deliberately more constrained than a generic “make it realistic” request.

### 7.1 Create a realistic automotive seat

**Vague request:** “Generate a realistic Lexus RX seat with luxury leather.”

**Technically informed request:**

```text
Create one front driver-seat asset for the 2020 Lexus RX 350 AWD showroom.
Use a Blender Python script or editable Blender scene first; do not output an opaque single mesh without named parts.

Coordinate and structure:
- Keep the seat origin at the existing AutoLab driver-seat origin.
- Create named objects for seat shell, cushion, backrest, headrest, outer bolsters, centre insert and power-switch trim.
- Preserve left/right symmetry and keep the seat within the four existing camera frustums.
- Use separate material assignments compatible with MAT_Seat_Primary, MAT_Seat_Secondary and MAT_Seat_Stitching.

Surface:
- The seat must support base colour, normal and ORM/roughness maps.
- Do not add stitch geometry for fine thread; leave a maskable region for the existing ORM-alpha thread workflow.
- Use UVs with consistent scale across the seat. Mark any unverified dimensions as estimates.

Runtime:
- Export a GLB candidate without renaming AutoLab’s existing slots.
- Do not modify the React configuration adapter or thread-mask shader.
- Record triangle count, draw calls, GLB bytes, texture dimensions and object/material names.

Acceptance:
- Load the candidate behind a test-only switch.
- Verify all four camera presets, seat textures, thread mask and two-tone colour bindings.
- Reject the candidate if it exceeds 80,000 triangles, 24 draw calls or 5,242,880 bytes.
- Return screenshots from Driver Hero and Stitch Detail plus a change report.
```

### 7.2 Refine leather and stitching

```text
Inspect the existing Diamond upholstery treatment before changing it.

Preserve:
- MAT_Seat_Primary, MAT_Seat_Secondary and MAT_Seat_Stitching names;
- the existing base, normal and ORM/roughness maps;
- the ORM alpha thread mask used by autolab-l4a-thread-v1;
- the existing UV scale and all four camera presets;
- the current triangle, draw-call and GLB-size budgets.

Goal:
Improve the perception of neutral warm leather without changing seat silhouette or adding stitch geometry.

Method:
1. Report the current maps and their colour spaces.
2. Generate or edit only tileable material maps.
3. Inspect base colour, roughness, normal and ORM alpha separately.
4. Use physically plausible roughness variation at upholstery scale; do not create high-contrast noise that reads as dirt.
5. Validate under neutral, grazing and warm room lighting.
6. Change only the material maps or shader parameters explicitly listed in the report.

Return map dimensions, packing, tiling scale, roughness range, screenshots, renderer counters and tests. If the desired result requires moving the thread mask, stop and report that as a migration rather than silently changing the shader.
```

### 7.3 Build a detailed dashboard

```text
Create a dashboard refinement as a separate, reversible asset experiment.

Use the current Lexus scene manifest as the source of truth. Keep dashboard trim, cockpit accent and cockpit black as separate named surfaces. Do not merge them into one material merely to simplify generation.

Model only the visible dashboard region required by the current Cockpit & Dash camera. Use low-complexity geometry for large forms and shader/material detail for grain, seam and subtle embossing. Keep clearance from the camera near plane and preserve the existing console and steering bindings.

If adding a new trim zone, propose whether it should reuse MAT_Console_Carbon or receive a new slot. Do not decide silently. If reusing the slot, preserve the existing KTX2 trim UV scale; if not, define the complete new contract and map budget.

Export a test GLB and provide:
- named objects and materials;
- bounds in AutoLab coordinates;
- triangles, draw calls and bytes;
- map roles and resolutions;
- fixed renders from Cockpit & Dash and Cabin Pair;
- a list of visual differences from baseline;
- rollback instructions.
```

### 7.4 Create a door panel with integrated controls

```text
Generate one front door-card prototype for the 2020 Lexus RX 350 interior.
This is a design-study asset, not an approved production replacement.

Geometry:
- Use named parent objects DoorCard, Armrest, Insert, Handle, SwitchPanel and SpeakerGrille.
- Keep controls as separate selectable meshes or instances so future interaction can target them.
- Define a stable local coordinate system and preserve the hinge/door plane relationship.
- Model the silhouette, gaps and major padded volumes; represent micro-perforation and fine grain in maps.

Materials:
- Define upholstery, trim, plastic and metal as separate slots.
- Provide base colour, normal and ORM/roughness requirements for each.
- Do not reuse existing seat slots unless the manifest explicitly approves it.

Runtime:
- Export GLB with Draco only if the decoder output preserves all required materials.
- Keep the candidate below the AutoLab asset budget.
- Do not add a second configuration state. Report how the existing colour and trim state would map to this zone.

Validation:
- Check silhouette from the planned Door Ingress camera.
- Test missing-texture recovery and camera near-plane safety.
- Return a scene manifest update proposal, not a silent source change.
```

### 7.5 Construct a rear-seat assembly

```text
Design a rear-seat assembly as a separate zone proposal for future multi-part loading.

Create named components for left seat, centre section, right seat, headrests, armrest, belt guides and visible lower trim. Use the same material-role vocabulary as the front cabin, but do not assume that a front-seat material instance can be shared safely until the runtime architecture supports shared zone bindings.

Define:
- zone ID and parent transform;
- material slots and which UI choices should affect them;
- UV scale and texture budgets;
- camera presets needed for inspection;
- whether the zone is loaded as a separate GLB or merged into a treatment GLB;
- how loading failure should preserve the rest of the cabin.

Produce an editable Blender source, a candidate GLB, a manifest and an integration decision record. Do not change AutoLab’s runtime or configuration adapter in this task.
```

### 7.6 Create a starlight headliner

```text
Create a starlight-headliner prototype for a future AutoLab optional treatment.

Use a dark headliner base with a controlled set of fibre-light points. Generate the point layout from a deterministic seed and store the seed. Separate the visible headliner surface from the fibre points and from the light-emission/control data.

Requirements:
- No random layout changes between builds with the same seed.
- Use instancing or a shader approach where possible; do not create thousands of unique materials.
- Define maximum point count, draw-call impact, texture impact and animation cost.
- Provide a reduced-motion mode and a static fallback.
- Keep the feature isolated from current seat and trim materials.
- Return a GLB or runtime prototype plus a data manifest, not only a beauty render.

Validate at the planned roof camera, under the existing room environment and on software WebGL. Report whether the feature is suitable for the current viewer or requires a new zone-loading design.
```

### 7.7 Improve materials and lighting of an existing GLB

```text
Improve the appearance of the supplied GLB without changing its geometry, object names, material names, UVs or camera framing.

First inspect and report:
- all meshes and material names;
- missing or failed texture decodes;
- map colour spaces and packing;
- normal orientation and strength;
- roughness and metalness ranges;
- bounding box and camera visibility;
- renderer calls, triangles, texture count and memory indicators.

Then make the smallest change that addresses the specific defect. Do not replace the full material graph. Do not introduce a new environment map without measuring the effect. Do not use base-colour darkening to hide incorrect roughness.

Render fixed views under:
1. neutral room lighting;
2. grazing side light;
3. warm ambient light;
4. the normal customer lighting state.

Return before/after screenshots, changed parameters, map hashes, counters, test results and known limitations. If the defect is geometric, stop and recommend a geometry task instead of masking it with a texture.
```

### 7.8 Inspect and correct defects from a rendered result

```text
You are reviewing AutoLab screenshot evidence, not starting a new scene.

Observed defect:
[insert screenshot path and precise observation]

Allowed scope:
- change only the named material, object transform or camera parameter;
- preserve every other approved object, material slot, map and configuration binding;
- do not regenerate the GLB globally;
- do not change budgets without reporting the proposed increase.

Diagnostic procedure:
1. Reproduce the exact camera and treatment state.
2. Capture a baseline screenshot and renderer snapshot.
3. Classify the defect as geometry, UV, map packing, colour space, roughness, normal, lighting, camera or interaction.
4. Identify the smallest testable correction.
5. Apply it in a branch or test-only switch.
6. Capture the same view and one adversarial view.
7. Run the relevant material, binding, camera and recovery tests.

Return a diagnosis with confidence level. If the evidence cannot distinguish between two causes, say so and propose the next measurement rather than guessing.
```

## 8. Comparing AI-assisted production approaches

| Approach | Visual quality potential | Geometry accuracy | Live configuration | Refinement | Main risk | AutoLab recommendation |
|---|---|---:|---:|---:|---|---|
| AI-generated Three.js/R3F | High for stylized or procedural scenes; can be real-time | Good for explicit procedural forms; weak for hidden measured surfaces | Excellent | Fast for code-local changes | Plausible but crude geometry, stale APIs, shader bugs and uncontrolled complexity | Use for viewer logic, procedural details, cameras, interaction and bounded shader work |
| AI-generated Blender Python | High when the scene needs editable geometry and offline inspection | Better for named meshes, modifiers, UVs and repeatable construction | Indirect; export required | Strong if scene inspection and screenshots are used | Context-sensitive operators, poor topology, object sprawl and slow dependency updates | Use for component prototypes, repeated upholstery, parametric assemblies, UVs and baking |
| Fable-assisted 3D development | Potentially high, based on broad vendor claims | Unresolved without public artifact and tests | Potentially excellent through code/tools | Potentially fast but evidence is less reproducible | Hidden tool path, unclear asset provenance and weak diagnostics | Evaluate experimentally; do not make it the production assumption |
| Hybrid Blender + Three.js | Highest practical potential for AutoLab | Strongest separation of authoring and delivery | Excellent | Good with export/import tests | Interchange failures, mismatched coordinate systems, map loss and duplicated logic | Recommended default for serious new cabin zones |
| Image-to-3D/text-to-3D | Useful for candidate forms and concept assets | Weak-to-moderate for occluded and measured automotive parts | Good after cleanup and import | Fast candidate generation; slower cleanup | Wrong back sides, poor topology, UV defects, heavy meshes and uncertain scale | Use for exploration or non-critical accessories; require remesh/UV/map/runtime gates |
| Conventional modelling assisted by AI | High and controllable | Highest when human/engineering references are authoritative | Good | Slower but predictable | Higher labour cost and need for skilled review | Use for approved production geometry and the most visible/structurally important surfaces |

The open-source automotive dashboard example is a useful reference because it exposes the whole browser path: Three.js, glTF/GLB, PBR, clearcoat/iridescence references, scripted doors and wheels, camera/orbit controls, lighting controls, tone mapping and Draco compression.[24] Its own README also makes an important limitation explicit: it is visualization, not a physics, manufacturing or safety tool. AutoLab should adopt that same honesty for a showroom configurator.

## 9. Recommended AutoLab methodology

### Phase 0: Establish the contract

Before generating anything, freeze the target:

- vehicle and trim reference;
- target browser and minimum device class;
- camera list;
- object and material naming;
- configuration states;
- map packing and colour-space rules;
- maximum triangles, draw calls, bytes and texture memory;
- load and interaction targets;
- reduced-motion and fallback behaviour;
- evidence required for acceptance.

For the current viewer, start with the existing 10-slot material contract, the seven active Lexus bindings, the ORM-alpha thread mask, local decoders, camera limits and the roadmap’s 80,000-triangle/24-draw-call/5,242,880-byte gates.[19]

### Phase 1: Build a scene manifest

Create a machine-readable manifest before geometry generation. It should include:

```json
{
  "assetId": "lexus-rx350-front-seat-study",
  "coordinateSystem": "AutoLab-runtime",
  "parent": "front-cabin",
  "objects": [
    {"name": "DriverSeat_CentreInsert", "role": "upholstery", "materialSlot": "MAT_Seat_Primary"},
    {"name": "DriverSeat_Bolster", "role": "upholstery", "materialSlot": "MAT_Seat_Secondary"},
    {"name": "DriverSeat_StitchMask", "role": "mask", "channel": "ORM.alpha"}
  ],
  "cameras": ["hero_driver", "cabin_pair", "cockpit_dash", "stitch_macro"],
  "budgets": {"triangles": 80000, "drawCalls": 24, "glbBytes": 5242880},
  "provenance": {"model": "record before generation", "seed": "record before generation"}
}
```

The manifest makes the AI work against named relationships instead of a vague visual target.

### Phase 2: Generate the smallest vertical slice

A vertical slice should include one component, one camera, one material treatment, one configuration action and one acceptance test. Examples:

- a driver-seat leather map change that preserves the thread shader;
- a console trim preview with unchanged geometry and KTX2 packing;
- one door-card prototype with a named armrest control;
- one starlight-headliner test with deterministic points and reduced-motion fallback.

A vertical slice gives AutoLab a measurable result and reveals whether the problem is geometry, material, runtime, performance or interaction before the project expands.

### Phase 3: Use the right authoring tool

Use Blender when the task needs editable mesh topology, UV inspection, modifiers, Geometry Nodes, baking, rigging or offline render comparison. Use Three.js/R3F when the task needs live browser controls, application state, camera switching, runtime shader behaviour, material selection or user-facing interaction. Use image-to-3D only when the generated asset is acceptable as a candidate and downstream cleanup is budgeted.

### Phase 4: Iterate with evidence

For every iteration, capture:

- the same fixed camera before and after;
- an adversarial camera that exposes hidden defects;
- a material-map inspection view;
- renderer counters;
- object/material binding state;
- load and error state;
- test output;
- changed-file and hash report.

A screenshot can reveal that a seat seam is misplaced. It cannot prove that the mesh is manifold or that a normal map uses the right convention. Pair visual evidence with structural inspection and runtime tests.

### Phase 5: Gate the asset

Reject candidates that fail any of these categories:

**Identity and structure:** expected objects, materials, hierarchy and coordinate system are present.

**Map contract:** required base, normal and ORM/roughness maps decode; colour spaces and packing are correct; UV scale is within contract.

**Runtime binding:** UI state reaches the intended materials; no second configuration store is introduced; thread and trim hooks remain valid.

**Cameras:** all customer presets show the intended component; no near-plane clipping or unusable orbit state.

**Performance:** triangles, draw calls, payload, texture memory and frame time fit the target device.

**Recovery:** missing asset, failed decoder or unsupported shader produces a controlled fallback and retains customer selections.

**Provenance:** source references, prompts, model/tool versions, seeds, generated files, human edits, hashes, screenshots and known limitations are recorded.

### Phase 6: Export and rollback

Build assets from committed Blender scripts or reproducible generation steps. Record Blender, Three.js, KTX2/Basis and model/tool versions. Run the asset gate and save real output. Load the asset behind a test-only switch. Run binding, thread-mask, trim, camera and recovery tests. Compare fixed renders. Swap the URL and hash only after approval. Keep the previous GLB so rollback is one commit revert.[19]

## 10. Materials, textures and lighting guidance for AutoLab

### 10.1 Leather

Leather realism comes primarily from scale, roughness variation, grazing response and seam/panel structure. Use a relatively restrained base colour. The normal map should communicate grain or embossing at a scale consistent with the camera; excessive high-frequency noise reads as stone or plastic. Roughness should vary by material role and wear story, not by random noise alone.

For perforated leather, separate the visible perforation pattern from true holes. Use a normal/roughness or alpha treatment when the camera does not require actual openings; reserve geometry or opacity for close views where parallax and shadow matter. Record the choice because it affects draw calls, overdraw and texture memory.

### 10.2 Stitching and quilting

Quilting has two layers: broad padded form and fine stitch appearance. Broad form belongs in geometry or carefully controlled normal/height detail. Fine thread can often be represented by a mask and shader colour, as AutoLab already does. This is more scalable than creating a unique mesh and material for every stitch.

The thread mask must be tested under different thread colours and leather colours. It should not disappear when the base colour is dark, nor leak across panel boundaries. Use fixed stitch-detail screenshots and program-cache assertions.

### 10.3 Wood, carbon and lacquer

Wood and carbon materials are highly scale-sensitive. A carbon pattern that is too large looks like a printed checkerboard; a wood grain aligned across adjacent panels can look artificial if UV direction ignores the panel layout. Lacquer requires reflection and clearcoat behaviour, but high reflectivity can expose a poor environment more than it improves realism. Validate under a controlled PMREM and a secondary light.

### 10.4 Lighting

Use lighting to diagnose materials, not just to flatter them. A neutral environment shows base colour and broad roughness. Grazing light reveals normals and seams. A warm environment shows whether colour choices remain legible. Keep a fixed diagnostic lighting preset in addition to the customer-facing ambient-light previews.

AutoLab’s current viewer uses a room environment, ambient and directional lights, and concealed coloured point lights without adding shadow-casting geometry.[17] New AI-generated lighting must respect that resource model unless a measured change is approved.

## 11. Performance and production discipline

AI-generated 3D often fails by producing more objects, textures and shader branches than the runtime can afford. Set the budget before generation and repeat it in the prompt. The current AutoLab GLB budget is already tight enough that visual detail should usually be added through maps, instancing, compression or LOD rather than unconstrained geometry.[19]

Use these controls:

- indexed meshes and merged static surfaces where material boundaries permit;
- instancing for repeated fibres, perforations or fasteners;
- texture atlases or shared maps where UV and material semantics remain clear;
- KTX2/Basis compression and mipmaps;
- Draco where decoder and material validation remain intact;
- shader detail instead of true displacement for small features;
- LOD or zone loading for future rear, door and roof assemblies;
- workers for expensive procedural preparation;
- deterministic seeds for generated layouts;
- target-device profiling rather than showcase-device assumptions.

Do not use a headless software-renderer timing number as a universal FPS claim. Measure AutoLab on the owner’s workshop PC and representative mobile hardware. Keep triangle, draw-call, asset-byte, texture-memory, load-time and frame-time results beside the screenshots.

## 12. Known limitations and unresolved questions

### Dilum and the V8

The implementation, prompt, source, renderer, model pipeline, accuracy and performance of the V8 demonstration remain unresolved. The visible result may be a live system, a pre-rendered or composited sequence, or a hybrid. No public evidence reviewed here justifies a specific Three.js, Blender, Unity, Unreal or shader attribution.

### Astra

Astra’s public evidence strongly supports code-driven and tool-assisted 3D application development. It does not prove autonomous production topology, UV authoring, physically measured PBR, rigging or cross-device performance without external tools and review. Public showcase results should be reproduced under AutoLab’s own gates before they become architecture decisions.

### Claude Fable

Fable’s official material supports broad agentic and interactive-3D capability claims, but the checked public evidence does not expose a comparable source repository, exported asset, complete tool trace or runtime benchmark. Treat any Fable experiment as an evaluation project until its artifact is inspectable.

### Image-to-3D

Single-view systems infer hidden surfaces. They can produce compelling turntables while still failing on back-side geometry, topology, UVs, scale, material separation or rigging. AutoLab should not use them as the default for safety-relevant or measurement-sensitive automotive geometry.

### Physical and commercial accuracy

The current AutoLab repository itself says that colours and treatments are digital samples, not calibrated physical finishes, and that the existing shading, geometry/UV and simplified cockpit do not certify visual fidelity.[16] Any AI-generated improvement must preserve that disclosure. A convincing showroom should not be presented as manufacturing data, fitment certification, or a substitute for customer consultation.

### Model and tool drift

Model names, versions, APIs, hosted services and capability pages change. Every experiment must record the exact model identifier, date, prompt version, tool version, seed, input references and output hashes. Do not rely on a name such as “Astra” or “Fable” without a source and version.

## 13. Recommended first AutoLab experiments

1. **Material-safe leather refinement.** Use the existing Diamond GLB. Generate three neutral leather map candidates. Preserve the ORM-alpha thread mask. Compare fixed renders, map views and counters. Accept only the candidate that improves the material without exceeding current contracts.

2. **Procedural stitch-layout study.** In Blender, generate a parametric seam/stitch guide as an editable source. Do not integrate it into the runtime yet. Evaluate whether the result should become a normal/ORM mask, instanced geometry or a new shader path.

3. **Console trim calibration.** Create a controlled wood/lacquer/carbon material study using the current `MAT_Console_Carbon` contract. Validate KTX2 packing, UV scale and PMREM response. Do not add new trim slots until the owner chooses the zone architecture.

4. **Door-card vertical slice.** Prototype one front door card with named objects and one camera. Keep it outside production loading until shared material state and multi-part loading are designed.

5. **Starlight headliner feasibility.** Test deterministic instanced points and reduced-motion behaviour under a strict draw-call budget. Decide whether the feature belongs in a new GLB zone, a runtime particle/instance layer or a shader-only approximation.

6. **AI evaluation harness.** Give Astra and Fable the same scene manifest, screenshots, constraints and defect task. Score each result on structural correctness, visual quality, editability, reproducibility, runtime performance and provenance—not on the beauty render alone.

## 14. Conclusion

AutoLab can use AI to reach a more sophisticated 3D showroom, but the winning strategy is not to ask a model to replace the entire asset pipeline. The winning strategy is to make the pipeline legible to the model and to the engineers who must maintain it.

Use AI for decomposition, procedural code, repeated geometry, material studies, shader scaffolding, test generation and bounded corrections. Use Blender for editable geometry, UVs, baking, inspection and asset preparation. Use Three.js/R3F for browser delivery, UI state, camera control and live configuration. Use images as references and diagnostic evidence, not as proof that geometry is correct. Use source manifests, renderer counters, fixed renders and automated tests to keep the result honest.

Dilum Sanjaya’s public work shows that an AI-assisted creator can aim at ambitious interactive engineering visualizations. The public record does not disclose enough to copy his private process, and it should not be presented as if it does. AutoLab’s advantage is that it already has a real runtime, explicit material bindings, a shader contract, camera presets, decoder handling, diagnostic state and measurable budgets. Those constraints are not obstacles to AI generation. They are what make AI-generated 3D work reproducible and commercially useful.

## References

[1]: https://x.com/DilumSanjaya/status/2096280244663775423 "Dilum Sanjaya public V8 visualization post"
[2]: https://www.youtube.com/shorts/yAQKHK0VCIc "Secondary repost describing V8 features"
[3]: https://developers.openai.com/blog/how-to-build-games-with-astra "OpenAI developer article on building Void Explorer with Astra"
[4]: https://devtalk.blender.org/t/3d-agent-blender-ai-assistant-built-a-multi-agent-system-on-top-of-blenders-mcp-and-python-api-and-sharing-architecture-learnings-for-the-lab-discussion/44260 "Blender DevTalk 3D-Agent architecture discussion"
[5]: https://github.com/microsoft/TRELLIS "Microsoft TRELLIS open 3D generation repository"
[6]: https://openai.com/index/gpt-6-astra/ "OpenAI GPT-6 Astra announcement and 3D examples"
[7]: https://dilum.dev/ "Dilum Sanjaya personal site"
[8]: https://dilum.dev/lab "Dilum Sanjaya AI Lab"
[9]: https://dilum.dev/handcrafted "Dilum Sanjaya handcrafted Three.js/WebGL work"
[10]: https://x.com/DilumSanjaya/status/2053155739389378849 "Dilum Cell Architecture Studio post"
[11]: https://x.com/DilumSanjaya/status/2092293934844346660 "Dilum code-generated tank post"
[12]: https://x.com/DilumSanjaya/status/2080335531108716750 "Dilum hexapod inverse-kinematics post"
[13]: https://x.com/DilumSanjaya/status/2020181365095023053 "Dilum hexapod simulator post"
[14]: https://x.com/DilumSanjaya/status/2106426962738880879 "Dilum warehouse digital twin post"
[15]: https://www.youtube.com/watch?v=Amef2nkVccI "Dilum public character and 3D workflow video"
[16]: https://github.com/Suyanka21/Auto-lab-digital-ui "AutoLab Digital Showroom repository"
[17]: https://github.com/Suyanka21/Auto-lab-digital-ui/blob/main/src/viewer/RuntimeViewer.tsx "AutoLab R3F runtime viewer"
[18]: https://github.com/Suyanka21/Auto-lab-digital-ui/blob/main/src/lib/three/thread-mask.ts "AutoLab thread-mask shader hook"
[19]: https://github.com/Suyanka21/Auto-lab-digital-ui/blob/main/docs/3d-roadmap/3D_MIGRATION_AND_COMPATIBILITY.md "AutoLab 3D migration and compatibility roadmap"
[20]: https://docs.blender.org/api/current/info_overview.html "Blender Python API overview"
[21]: https://ubisoft-laforge.github.io/world/chord/ "Ubisoft La Forge CHORD material generation and SVBRDF estimation"
[22]: https://docs.pmnd.rs/react-three-fiber/getting-started/introduction "React Three Fiber documentation"
[23]: https://github.com/takara-ai/project-elevenlabs "Hanashi React Three Fiber open-source project"
[24]: https://github.com/studio-public-demos/car-concept-3d-dashboard "Open-source Three.js automotive dashboard example"
[25]: https://stable-fast-3d.github.io/ "Stable Fast 3D official project page"
[26]: https://github.com/VAST-AI-Research/TripoSR "TripoSR official repository"
[27]: https://github.com/TencentARC/InstantMesh "InstantMesh official repository"
[28]: https://github.com/Tencent-Hunyuan/Hunyuan3D-2 "Hunyuan3D-2 official repository"
[29]: https://www.anthropic.com/claude/fable "Anthropic Claude Fable product page"
[30]: https://docs.anthropic.com/en/docs/about-claude/models/overview "Anthropic Claude model overview"
[31]: https://www.babylonjs.com/ "Babylon.js real-time 3D engine"
[32]: https://www.techart.de/en/service-dialog/techart-3d-configurator.html "TECHART 3D Configurator"
[33]: https://www.3dtuning.com/en-US/ "3DTuning online vehicle configurator"
[34]: https://github.com/ubisoft/ubisoft-laforge-chord "Ubisoft La Forge CHORD source repository"
[35]: https://developers.openai.com/showcase/void-explorer "OpenAI Void Explorer showcase"
[36]: https://developers.openai.com/api/docs/models/gpt-6-astra "OpenAI GPT-6 Astra model documentation"


# Reference-library supplement

This supplement extends the earlier AI-to-3D guide with a 2020 Lexus RX 350 AWD evidence package. It does not replace the earlier findings about Dilum Sanjaya, AI-to-3D workflows, Astra/Fable uncertainty or AutoLab’s runtime contracts.

## What the collected evidence adds

The strongest exact-year sources are the Lexus USA Pressroom media page and its linked product-specification PDF. The pressroom page identifies the media as 2020 Lexus RX material and provides high-resolution downloads, but its copyright notice limits the media to editorial use and prohibits advertising, marketing or other commercial use without permission. These images are therefore suitable for internal visual comparison and geometry review, not product incorporation.

The official 2020 RX material confirms that the model-year cabin includes a forward-positioned central display, a trackpad-style Remote Touch interface, available 8-inch or 12.3-inch displays, revised seat/detail treatments, ambient lighting, heated and ventilated seating on applicable grades, and trim choices that vary by grade and market. The official European newsroom also describes a vertical seat-stitching pattern and matching quilting on door-panel trims, but European equipment and grade details must not be assumed for the U.S. RX 350 AWD target.

## Highest-priority AutoLab geometry work

1. **Front-seat silhouette and panel boundaries.** Use the official front-seat image as broad visual evidence, then obtain owner/VIN-specific photographs or measured references for exact seat grade, headrest shape, seam placement and perforation pattern.
2. **Dashboard-to-console transition.** The official cockpit and console images are more valuable than generic luxury-interior images for camera framing, screen placement, console width and steering relationship.
3. **Door-panel layering.** Current public references are weaker than the official cockpit images. A controlled set of owner/vehicle-specific door-panel photographs or a legitimate parts diagram would materially reduce uncertainty.
4. **Rear-seat and headliner geometry.** The package has supporting rear-seat imagery, but exact five-seat RX 350 AWD rear-seat and roof references remain incomplete.
5. **Material studies.** Quilting, perforation, leather grain and starlight-headliner images are useful for scale and shader discussion, but are not evidence of Lexus-specific materials or colours.

## How to use the references in generation prompts

Pass each image with a declared role: silhouette, component adjacency, material scale, lighting only or process reference. Do not ask an AI model to infer exact dimensions from a perspective image. For every generated change, require a before/after camera capture, a scene-manifest comparison, map inspection and the current AutoLab triangle/draw-call/GLB-size checks.

## Rights interpretation

No asset in this package is classified as commercial-use permitted. The official Lexus media are editorial/reference-only; dealer and marketplace images are reference-only or unverified; stock-like and YouTube thumbnails have unresolved ownership or permission. This is intentional. The package is evidence for internal engineering decisions, not a licence to copy imagery into the showroom.
