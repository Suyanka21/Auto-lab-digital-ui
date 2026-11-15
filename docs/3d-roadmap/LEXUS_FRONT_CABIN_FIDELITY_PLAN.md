# Lexus front-cabin fidelity plan

Date: 2026-11-15. Status: proposal for owner approval. Nothing here is implemented.

Goal: make the existing front cabin read as a real Lexus RX 350 (2020, fourth generation) interior while keeping every live configuration choice working.

## 1. Modelling strategy

| Criterion | Blender modelling | Procedural Three.js | Hybrid (recommended) |
|---|---|---|---|
| Geometry accuracy | Best: sculpted to references, measured | Weak for soft, moulded shapes | Blender for every vehicle-shaped part |
| Surface detail | Bake high-poly detail into normal/AO maps | Shader patterns cheap and live | Bake leather and seams; shader for perforation, quilting thread, LEDs |
| Shading | Full PBR authoring, baked AO | Runtime only | Baked AO + runtime PBR |
| Asset reuse | Parts as linked components | Parametric components | Blender components + runtime instancing |
| Camera behaviour | Unchanged | Unchanged | Unchanged presets |
| Mobile performance | Controlled by LOD and bakes | Shaders cost GPU time | Detail in textures, not triangles |
| Maintainability | Needs a reproducible headless build | Code-reviewed | One build script per zone + small runtime modules |
| Live colour, stitching, trim | Kept through slot names | Native | Kept through slot names |

The Manus PBR blueprint (`AUTOLAB_COMPLETE_DOCUMENTATION/`) covers textures for four slots only. It is a useful input to stage 3, not a geometry plan. Generated maps still pass the asset gate and human review.

## 2. Staged plan

Each stage is one or more small PRs, ends with the asset gate and a fixed render set, and stops for owner review.

| Stage | Work | Exit criteria | Est. effect on budgets |
|---|---|---|---|
| **3D-0 Reproducibility** | Install Blender 5.2.2 and KTX 4.4.2 (authorised in D0 for the original repo; confirm for this repo). Replace the hard-coded Windows `toktx.exe` paths. Rebuild the current GLBs from source; compare node, material and triangle counts against the committed hashes. Port the asset gate. | Same 11 nodes, 10 materials, 24 calls, triangles within 1 %; gate runs in CI | none |
| **3D-1 Reference pack** | Collect authoritative references: Lexus RX 350 owner's manual, Lexus press images and dimensions, and owner-taken photos of a real 2020 RX cabin. Build a dimension ledger, each value tagged measured / published / estimated. | Every dimension used has a source and confidence; `evidenceConfidence` corrected | none |
| **3D-2 Front seats** | Rebuild seat shells at higher density in Blender; real seams, piping and bolster breaks; bake high-poly to the runtime mesh. Keep Classic, Diamond and Perforated as normal/ORM variants of one mesh where possible. | No visible faceting at `seam_macro`; slot zoning matches real seat panels | +10–25 k triangles; 0 extra calls if slots stay merged |
| **3D-3 Material lab** | Leather grain, stitch thread, perforation and veneer maps (own scans or the Manus pipeline). OpenGL normal convention, KTX2 UASTC for normals. | Gate passes; human review scores leather as leather | +0.5–1.2 MB textures per GLB |
| **3D-4 Cockpit surfaces** | Dashboard, steering wheel, console and selector refinement; screen glass, vents and switchgear as low-poly + baked detail; textures for the five flat materials. Close the dashboard ends with an A-pillar and door-cap stub (fixes the Driver Hero grey shape). | No untextured hero surface; Driver Hero clean at the reframed preset | +10–20 k triangles; +2–4 calls for new slots (owner decision on the 24 limit) |
| **3D-5 Lighting and presentation** | Studio HDRI owned or licensed by AutoLab; baked contact shadow under seats and console; ambient LED as emissive strip geometry along real trim lines; adjust camera presets only where geometry changed. | Dark leather readable; ambient colour visible as a wash | +1 call for LED strips; HDRI about 0.5–1.5 MB |
| **3D-6 Human review** | Fixed render set, reference comparison, owner scoring. The agent does not self-certify. | Owner acceptance recorded | none |

Estimated totals after stage 5 (inferred): 90–130 k triangles, 26–30 calls, 5–7 MB per treatment. All exceed today's limits, so stage 2 starts with an owner decision on new budgets measured on the workshop PC. A lower-detail mobile GLB (LOD) is the fallback if phones cannot hold frame rate.

## 3. Validation for every stage

- Asset gate output and SHA-256 pasted in the PR.
- Unit tests: bindings, thread mask, trim swap, cache revisions.
- Browser tests: all three treatments, primary/secondary colour, thread, trim, ambient, four presets, Retry after a failed load.
- Renders from all four presets, before and after, desktop and 390 px mobile.
- Frame time and memory on the workshop PC and one real phone; "not tested" where unavailable.

## 4. Unresolved decisions

1. New triangle, draw-call and byte budgets per GLB.
2. Default camera (reframed Driver Hero vs Cabin Pair).
3. Source of references: may AutoLab photograph and measure a real 2020 RX 350?
4. HDRI and texture sourcing: own capture, licensed library, or AI-generated maps.
5. Which Lexus features are in scope (e.g. 12.3-inch screen, Remote Touch pad, analogue clock) versus simplified.
