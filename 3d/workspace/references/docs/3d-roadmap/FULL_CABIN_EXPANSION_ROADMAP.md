# Full-cabin expansion roadmap

Date: 2026-11-15. Status: long-term direction. Not authorised for implementation; each phase needs owner approval.

Prerequisite: the front-cabin plan through stage 3D-5 and the multi-part loading decision in `3D_MIGRATION_AND_COMPATIBILITY.md`.

## Phases

| Phase | Zone | Technique | Live configuration | Est. cost (inferred) |
|---|---|---|---|---|
| F1 | Door cards (front) | Blender, baked detail; armrest, pull, speaker grille, switch panel | Primary/secondary leather on inserts; trim strip on `MAT_Console_Carbon` or a new door-trim slot | 15–25 k tris, 3–4 calls |
| F2 | Pillars, floor, carpet edge, kick panels | Blender low-poly + tiling textures | Fixed finishes | 5–10 k tris, 2 calls |
| F3 | Rear bench (60/40), rear door cards, rear console | Blender; reuse seat panel kit from 3D-2 | Same seat slots as front | 25–40 k tris, 4–6 calls |
| F4 | Headliner, roof console, visors, grab handles | Blender; fabric or Alcantara-style material | New headliner slot | 5–10 k tris, 2 calls |
| F5 | Starlight headliner | Fibre points as one `InstancedMesh` or `Points` (500–1,500 points); twinkle in the vertex shader; brightness tied to a night-lighting mode | Star colour, density pattern, on/off | 1–2 calls; fill-rate cost if bloom is added |
| F6 | Full-cabin exploration | Zone-based loading, LOD per zone, camera presets per zone, guided tour | All zones share one colour state | Target under 15 MB total with progressive loading |

## Notes and risks

- **Starlight is aftermarket, not OEM.** Lexus did not offer a starlight headliner on the 2020 RX 350 to my knowledge (inferred; confirm). Present it as an AutoLab installation option. Cars with the panoramic moonroof limit headliner area; ask whether to model the moonroof variant.
- **Night illumination realism** needs a darker studio mode and possibly bloom post-processing, which adds a full-screen pass. Measure on the workshop PC before adopting; a baked glow sprite is the cheaper fallback.
- **Rear cabin accuracy** depends on references for rear seat shape and door cards; none exist in the repo today.
- **Loading time:** today's single GLB takes about 12–13 s cold in software rendering (inherited). Full cabin must load the front zone first and stream the rest.
- **Mobile:** expect a reduced LOD and no bloom on phones.

## Acceptance for each phase

Asset gate, binding tests for every new slot, fixed render set from new zone presets, measured frame time on the workshop PC, and owner visual acceptance.
