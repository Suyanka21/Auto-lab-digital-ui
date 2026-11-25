# Dependencies, provenance and rights

## Tested local software

| Tool | Actual version / role |
|---|---|
| Blender | 5.2.2 LTS, build `d13f752e3b9c`; headless bpy, Cycles CPU; required for exact R4 reproduction |
| Blender Python | Bundled environment; mathutils/bpy supplied by Blender; NumPy 2.3.4 recorded in original probe |
| Standalone Python | 3.12.6; portable inventory and file checks |
| Pillow | 11.0.0; comparison sheets |
| NumPy | 2.1.3; archived image-comparison helper only |
| Git LFS | 3.5.1 installed locally; handles new archived .blend/.blend1/.glb files |
| KTX-Software | Original workspace probe records toktx 4.4.2; not needed for master audit/build/render, required by later runtime encoding |
| Node | Original workspace probe records v22.23.2; not needed for R4 master reproduction |

The new helpers need no Blender add-on or MCP server. Do not install optional tools to open/audit R4. A Linux/Devin Blender 5.2.2 environment has not been tested here; verify its executable/version before work. The old builder emits a `World.use_nodes` deprecation warning for future Blender 6.0. No Blender 6 compatibility is claimed.

For comparison tools, the small `requirements-review.txt` records tested standalone versions. For old candidate pipelines, `3d/workspace/build_pipeline/package-lock.json` pins @gltf-transform/core/extensions 4.5.1, draco3dgltf 1.5.9, gltf-validator 2.0.0-dev.3.10 and ajv 8.20.0. npm cache contents are intentionally excluded. Install with `npm ci` in a restored scratch pipeline only when that separate runtime work is authorised. Full historical finalizer execution is not part of this handover validation.

## Skills and code actually used

The R4 geometry builder and refinement are first-party project scripts using Blender Python, mathutils, standard-library math/JSON/hash/AST operations. They do not import an external Blender-specialist repository. No third-party specialist add-on is required or claimed as the source of R4 geometry.

The archived **realistic-3d-craft** skill informed silhouette-first work, physical edge/material scale, material labs, bounded image review and the separation of master shaders from web assets. Its advisory comparison script was executed. Verified source pin:

- [Skill tree at b5338d3](https://github.com/Suyanka21/AUTOLAB-DIGITAL-SHOWROOM/tree/b5338d324275ca473349e68194be3ac943ba7687/.agents/skills/realistic-3d-craft)
- [Skill entrypoint](https://github.com/Suyanka21/AUTOLAB-DIGITAL-SHOWROOM/blob/b5338d324275ca473349e68194be3ac943ba7687/.agents/skills/realistic-3d-craft/SKILL.md), Git blob `0a176f606829c930e801bda78b6290e1e26d193b`.
- Archived skill SHA-256 `1864e29b06216d624f8ec515dacc246f12a69741393601b148a645560c9614fb`; archived comparison helper SHA-256 `563b77e205f6340a662bda4612153ed7d8434ce9d863ae61bf2776b7dfc39909`.
- The directory and repository root at that pin had no standalone licence file when checked through GitHub on 2026-11-23. Do not label this skill MIT or infer a public reuse licence. The owner authorised first-party project reuse/publication. The new skill does not relicense unrelated code or reference imagery.

The older craft_kit is retained for earlier cabin-build history; the R4 door builder does not import it. Archived blender-asset-pipeline, gltf-asset-gate, visual-fidelity-review and webgl-viewer-engineering skills are provenance, not automatically loaded requirements. Earlier Dilum/Sanjaya research and PR6 experiments are background and do not establish a hidden external workflow or an adopted dependency.

## External software licences and asset limits

Blender is separate installed software, not bundled in this handover. See its [official licence page](https://www.blender.org/about/license/). npm dependencies retain their package licences when installed; the package lock records exact source packages. No node_modules, software installer or shared cache is published.

GitHub's [large-file documentation](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github) warns above 50 MiB and blocks ordinary Git files above 100 MiB. None of these new individual source assets approaches that threshold, but editable binary history is tracked with LFS to avoid accumulating it in ordinary Git. [LFS stores pointers and separate objects](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage); a push is not verified until an independent clone retrieves those actual objects. Account quotas remain service-controlled.

The approved AI pack remains the owner's visible design authority, not OEM dimensional evidence. The supporting photographs retain their original rights/provenance limitations and are not declared cleared marketing assets. Existing root reference-library paths and files are unchanged. This repository has no blanket project licence; this task does not invent one.
