# Dilum Sanjaya 3D technique research

Date: 2026-11-15. Purpose: separate what is proven by public source from what is claimed, and decide what AutoLab can use.

## Method and access limits

- GitHub: listed all 100 most recently updated public repositories of `dilums` through the GitHub API and read `package.json`, file trees and selected sources. **Verified.**
- `dilum.dev/lab/engineering` and `dilum.dev/handcrafted/threejs`: fetched public HTML. **Verified.**
- X, YouTube and CodePen: the Firecrawl MCP server failed to start in this session ("connection closed: initialize response" on all five calls), and X needs a login. I used public search-engine snippets and re-posts instead. **I did not watch the videos**, so any statement about how a demo looks is a hypothesis.
- No code or asset was copied. Licences were recorded per repository.

## Evidence table

| Source | What it shows | Stack | Licence | Status |
|---|---|---|---|---|
| `jet-engine-threejs` (2023) | Airflow through a jet engine, 583-line `src/main.js` | Vite, three 0.125 | MIT | **Evidenced**: `InstancedMesh` ×4, `ShaderMaterial` ×2, `Points` ×2, `DataTexture` ×2, `ParametricBufferGeometry`, `CurvePath` ×3, no model files |
| `spells-and-potions`, `wildfire`, `valentines-threejs`, `lost-at-sea`, `3d-timeline-concept`, `r3f-cannon-basic-objects` (2023) | Handcrafted scenes | Vite + three 0.150, or R3F + cannon | MIT | **Evidenced** that they are procedural; `spells-and-potions` is described as "without using any models" |
| `aisdk-threejs-starter` (2025) | An LLM returns JSON for primitives (`box`, `sphere`, `cylinder`, `cone`) that R3F renders | Next 15.5, R3F ^9.3, drei ^10.7.6, three ^0.180 | none | **Evidenced**: `<Canvas>`, `<Environment>` with a 1k HDRI file, `<OrbitControls>` |
| `hexapod-robot-simulator` (2025) | Robot simulator | Next 16, Plotly, Zustand; **no three.js** | none | **Evidenced** that not every 3D demo uses Three.js |
| AI Lab, Engineering category (13 items incl. **V8 Engine**, Skymaster Landing Gear) | Links to X posts only | unknown | n/a | **Creator claim**: "Most of what I build these days, I build with AI." |
| V8 reference post | "Interactive visualization of a V8 engine I made with GPT-6 Astra" (LinkedIn, 2026-09-08; about 3.8 M views on X) | unknown; no public source | n/a | **Creator claim** |
| Gadget thread (2026-09-01) | "Everything here is generated with code." Models default to Three.js primitives, "which aren't very polished"; lathe, extrude and custom geometries look better but cost more tokens | Three.js | n/a | **Creator claim** |
| Live-stream listing | Workflow with Nano Banana, Midjourney, Hunyuan3D, Gemini Pro and Three.js | mixed | n/a | **Creator claim**; implies image-to-mesh generation in some work |

## The seven questions

1. **Procedural geometry with Three.js.** Evidenced in the MIT demos (instancing, parametric surfaces, curve paths, custom shaders). The AI Lab demos claim the same, through lathe and extrude geometry. Fit for AutoLab: good for rigid, repeatable or parametric detail (stitch rows, perforation, LED strips, starlight fibres). Poor for organic upholstery and moulded trim.
2. **Blender-assisted modelling and GLB export.** No public Blender file or GLB was found in any inspected repository. Whether the V8 used Blender is **unknown**. The Hunyuan3D mention suggests some assets come from image-to-3D tools, which is a **hypothesis** for any single demo.
3. **PBR materials and real-time shading.** Evidenced only as a drei `<Environment>` with an HDRI and custom `ShaderMaterial`s. No evidence of baked maps.
4. **Camera choreography and object exploration.** Evidenced only as `OrbitControls`. Exploded views, part isolation and guided tours are **hypotheses** from post titles ("interactive visualization").
5. **Reusable scene components.** Evidenced in the JSON-to-component pattern of the starter. The V8 structure is unknown.
6. **Lighting, reflections and shadows.** Evidenced: environment maps and emissive or point-based effects. No shadow-map setup found in inspected code.
7. **Detail versus performance.** Evidenced: `InstancedMesh` and `Points` to draw thousands of repeated parts in one call; `DataTexture` to drive shaders instead of geometry.

## What applies to AutoLab

| Technique | Use in AutoLab | Why |
|---|---|---|
| Instancing (`InstancedMesh` / `Points`) | Starlight fibres, perforation dots if geometric, cupholder ribs | One draw call for thousands of items |
| Curve-driven geometry (`TubeGeometry` along a `CurvePath`) | Ambient LED strips, piping and seams | Exact path from Blender curves; colour stays live |
| Shader-driven detail (`DataTexture`, `onBeforeCompile`) | Already used for the Diamond thread mask; extend to perforation and quilting patterns | Detail without triangles |
| Environment HDRI | Replace `RoomEnvironment` with a studio HDRI AutoLab owns or licenses | Leather and lacquer need believable reflections (licence decision required) |
| LLM-generated primitives | **Not used** for vehicle geometry | Unverifiable accuracy, primitive look |
| Image-to-mesh tools (e.g. Hunyuan3D) | **Not used** for production geometry | Licence, topology and accuracy are unproven for a real Lexus interior |

The demos set a presentation target (clear, explorable, mechanical detail), not a technical recipe. They model rigid machines; a cabin is mostly soft, sculpted surfaces where Blender is the better tool.
