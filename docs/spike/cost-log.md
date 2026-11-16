# 3D cost log

| Date | Phase | Step | Wall-clock | Attempts | Failures |
|---|---|---|---|---|---|
| 2026-11-16 | 3D-0 | Download + checksum Blender 5.2.2, KTX 4.4.2 | ~5 min | 1 | 0 |
| 2026-11-16 | 3D-0 | Scratch rebuild (prepare, Blender, finalize) | ~27 s per run | 3 | 1: copied script still called `ktx.exe` (ENOENT), so Blender found no `source-render.glb` |
| 2026-11-16 | 3D-0 | Determinism rerun | ~27 s | 1 | 0 |
| 2026-11-16 | 3D-0 | Camera screenshots (SwiftShader) | ~1 min | 1 | 0 |
