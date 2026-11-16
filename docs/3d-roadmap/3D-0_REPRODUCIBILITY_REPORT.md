# 3D-0 — Asset provenance and reproducibility report

Date: 2026-11-16. Scope: reproducibility and asset validation only. No production GLB, geometry, viewer, camera preset or UI file was changed.

## 1. Result in one paragraph

The shipped front-cabin GLBs **can be rebuilt from committed sources, but not byte-for-byte**. The full chain (historic GLB inputs → Blender build → KTX2/Draco finalisation) runs on Linux with Blender 5.2.2 and KTX-Software 4.4.2. The rebuild has the same 11 nodes, 10 materials, 24 primitives, 66,260 triangles, materials and extensions, and it passes the asset gate. The seats and stitching (10 of 24 primitives) are identical. The console, dashboard and wheel use the same vertex positions, but some triangles are split differently and some UV assignments differ. Six procedural textures differ by a few 8-bit levels. The rebuild is deterministic on Linux: two runs gave identical hashes. The shipped GLBs therefore stay the baseline. A rebuilt GLB must never replace them without the owner's visual approval.

This corrects the PR #2 audit, which said no committed script produced the shipped GLBs. The scripts exist, but the build starts from three older GLBs, not from the `.blend` files.

## 2. Source-of-truth chain (verified)

All paths are in `Suyanka21/AUTOLAB-DIGITAL-SHOWROOM` (read-only), commit `a7bb961` (2026-11-06), the last commit to touch the GLBs.

| Step | File | Role |
|---|---|---|
| 0 | `public/assets/3d/lexus-rx350/interior-l4-*.glb` at commit `fa3d62a` | Historic inputs: seats, stitching, cockpit and their KTX2 textures. SHA-256 classic `168ecc26…`, diamond `db7828e1…`, perforated `c26f5198…` |
| 1 | `scripts/prepare-front-cabin.mjs` | Reads the three GLBs with `git show fa3d62a:…`, writes KTX2 textures, transcodes classic to PNG, writes `blender/out/front-cabin/source-render.glb` and `inputs.json` |
| 2 | `blender/build_front_cabin.py` (+ `front_cabin_constants.py`, `front_cabin_carbon.py`, `cockpit_surfaces.py`, `lexus_l2b_cockpit.py`, `lexus_l2b_constants.py`, `.agents/skills/realistic-3d-craft/scripts/craft_kit.py`) | Blender 5.2.2: imports `source-render.glb`, keeps the driver seat, mirrors the passenger seat, builds the console, carbon and metal procedurally (seeded NumPy), writes `cabin-raw.glb` and `build.json` |
| 3 | `scripts/finalize-front-cabin.mjs` (+ `scripts/validate-glb.mjs`) | `toktx` UASTC encode, per-treatment texture swap, Draco, material factors from the manifest, gate check on all three, then copy to `public/` |

Evidence that this chain produced the shipped files:
- `docs/review/front-cabin-2026-11-05/evidence/assets.json` lists output hashes `e5bdde01…`, `4c217dd0…`, `d53f5554…`, the shipped hashes.
- `evidence/blender-build.json` records Blender 5.2.2 LTS and 66,260 triangles. Its three script hashes match the committed files: `front_cabin_constants.py` and `front_cabin_carbon.py` as-is, `build_front_cabin.py` with Windows CRLF line endings (LF `26aab9d3…`, CRLF `27977c7d…` = recorded).
- `evidence/inputs.json` is reproduced exactly: same input hashes, primitives and texture names.

**Not part of the chain:** `blender/models/*.blend` (`front-cabin.blend`, `components/*.blend`). They are older outputs. The `.blend` written by step 2 goes to `blender/out/` and was never committed.

## 3. Provenance gaps (unresolved)

1. **Root inputs are GLBs, not editable sources.** The seats, stitching and cockpit geometry and their textures come from `fa3d62a`. The script that made those GLBs was not traced in 3D-0. Recovering editable seat geometry needs a separate trace of `fa3d62a`'s own history.
2. **The original build ran on Windows** (`C:\Users\user\OneDrive\Desktop\…`). The exact KTX build, NumPy build and OS that produced the shipped bytes are not recorded. Only Blender 5.2.2 is recorded.
3. **Tool paths are Windows-only** (`C:/Program Files/KTX-Software/bin/{ktx,toktx}.exe`). Path substitution was needed. It was done only in a scratch copy; the original repo is unchanged.
4. **Licences and origin of the `fa3d62a` textures are not recorded.** They need an owner check before any rework reuses them.

## 4. Tools (installed in the working environment only)

| Tool | Version | Source | SHA-256 verified |
|---|---|---|---|
| Blender | 5.2.2 LTS (hash `d13f752e3b9c`, built 2026-09-15) | `download.blender.org/release/Blender5.2/blender-5.2.2-linux-x64.tar.xz` | `84098912…a168`, matches the official `blender-5.2.2.sha256` |
| KTX-Software | 4.4.2 (`ktx`, `toktx`) | GitHub release `KTX-Software-4.4.2-Linux-x86_64.tar.bz2` | `a8781bad…a245`, matches the GitHub asset digest |
| Node | 22.23.2 | nvm | — |
| glTF Transform / glTF Validator | 4.5.1 / 2.0.0-dev.3.10 | `package.json` | — |

## 5. Exact rebuild procedure (scratch only)

```bash
S=~/scratch/repro && mkdir -p $S
git -C AUTOLAB-DIGITAL-SHOWROOM archive origin/main | tar x -C $S           # no change to the original checkout
git -C AUTOLAB-DIGITAL-SHOWROOM bundle create ~/scratch/orig.bundle origin/main
cd $S && git init -q && git fetch -q ~/scratch/orig.bundle origin/main      # makes `git show fa3d62a:` work
sed -i 's#C:/Program Files/KTX-Software/bin/\(t\?o\?ktx\)\.exe#'$HOME'/tools/ktx/bin/\1#g' scripts/{prepare,finalize}-front-cabin.mjs
npm ci
export LD_LIBRARY_PATH=$HOME/tools/ktx/lib
node scripts/prepare-front-cabin.mjs
~/tools/blender-5.2.2-linux-x64/blender -b --factory-startup --python-exit-code 1 --python blender/build_front_cabin.py
node scripts/finalize-front-cabin.mjs
```

Linux run: about 27 s end to end. Blender took 3.1 s wall and peaked at 559 MB.

## 6. Rebuild vs shipped baseline

Comparison tool: `node scripts/compare-glb.mjs <baseline> <candidate> --report out.json` (new in this PR). Full reports: `docs/evidence/3d-0/compare-*.json`.

| | classic | diamond | perforated |
|---|---|---|---|
| Shipped SHA-256 / bytes | `e5bdde01…` / 3,650,764 | `4c217dd0…` / 3,787,228 | `d53f5554…` / 3,509,764 |
| Rebuilt SHA-256 / bytes | `af070cc2…` / 3,642,356 | `02c7ec30…` / 3,788,348 | `0994f738…` / 3,510,884 |
| Gate (80k tris / 24 calls / 5 MB) | PASS | PASS | PASS |
| Nodes, materials, extensions | equal | equal | equal |
| Triangles / draw calls | 66,260 / 24 equal | equal | equal |
| Identical primitives | 10 of 24 (seats, stitching) | 10 of 24 | 10 of 24 |
| Same vertex positions, different triangulation | Console_Body #0, #1 | same | same |
| UV assignment differs (same UV range) | 9 console/dashboard primitives | same | same |
| Texture differences | 3 carbon + 3 classic insert | 3 carbon | 3 carbon |

Decoded texture differences (classic, `ktx extract --transcode rgba8`, 8-bit):

| Texture | Max difference | Notes |
|---|---|---|
| bolster base / normal / ORM | 0 | identical |
| carbon base / roughness | 2 | visually identical |
| carbon normal | 15 | 0.01 % of pixels differ by more than 8 |
| insert base | 4 | PSNR 76.6 dB |
| insert normal | 10 | PSNR 54.4 dB |
| insert ORM | 20 | PSNR 47.4 dB; 0.66 % of pixels differ by more than 8 |

Determinism: a second Linux run produced identical `cabin-raw.glb` (`0f1f7753…`) and identical final GLBs.

**Likely causes (hypotheses, not verified):** floating-point and library differences between the original Windows build and Linux in Blender's procedural textures, bmesh triangulation and UV seam ordering. A second candidate is `toktx` UASTC encoding with rate-distortion optimisation (`--uastc_rdo_l 1.1`) on 4 threads, which may encode differently on another CPU. Proving either needs a rerun on the original Windows machine.

## 7. Asset gate in this repository

`scripts/validate-glb.mjs` worked before this PR, but only with `--scope lexus-front-cabin`. Its default scope (`full`) needed S-Class files that were never migrated, which produced the empty "0 nodes" report. Changes:

- The default scope is now `lexus-front-cabin` and the default asset is the shipped classic GLB.
- `--help` prints usage.
- The `full` and `spike` scopes fail with a clear "not available in this repository" message instead of an empty report.
- `npm run asset:gate` validates all three shipped GLBs (reports go to ignored `reports/`).
- Budgets are still read from `src/config/scene-manifest.front-cabin.json`: 80,000 triangles, 24 draw calls, 5,242,880 bytes. They are unchanged.

New tests (independent fixtures, generated in memory):
- **Budget mutations:** a model over 80,000 triangles, over 24 draw calls or over 5 MB fails.
- **Contract mutations:** a renamed seat material, an extra node or a truncated shipped GLB fails.
- **Scope check:** S-Class scopes are refused with a clear message.
- **CLI:** the default run passes and reports the shipped classic hash; `--help` works; `--scope full` exits 1.
- **Comparison tool:** a GLB compared with itself reports no differences; classic vs diamond differ only in the three insert textures.
- **Baseline:** the three shipped GLB hashes are pinned.

## 8. Safe recovery process (proposed, not executed)

1. Keep the shipped GLBs as the baseline; the hash test fails if they change.
2. Make the build portable in a new PR. Read the KTX path from an environment variable (default the Windows path), and record OS, NumPy and KTX versions in `build.json`. No change to geometry or material logic.
3. Commit the rebuilt Linux outputs as a **candidate** under `blender/out/` or as CI artifacts, never in `public/`.
4. Compare the candidate to the baseline with `compare-glb.mjs` and a fixed camera render set (Driver Hero, Cabin Pair, Cockpit, Stitch Detail).
5. The owner either accepts the Linux rebuild as the new reproducible baseline, or keeps the Windows bytes. If needed, rerun the chain on the Windows machine to confirm byte identity.
6. Before any seat rework, trace or rebuild the `fa3d62a` inputs so the seats have an editable source.

## 9. Camera screenshots (no camera change)

Captured from this repository's production build at 1440×900 and 390×844 (headless Chromium, SwiftShader software rendering), with the default settings. The Studio opens on Driver Hero.
- `docs/evidence/3d-0/desktop-driver-hero.png`, `desktop-cabin-pair.png`
- `docs/evidence/3d-0/mobile-driver-hero.png`, `mobile-cabin-pair.png`
- Script: `docs/evidence/3d-0/capture-cameras.mjs` (run from the repo root while `npm run preview` is serving)

Observation: in desktop Driver Hero the flat grey end of the dashboard fills roughly the left third of the stage. This is the obstruction that original-repo PR #4 reduced by moving the camera to `[1.9, 1.25, 0.2]`. Cabin Pair shows the dashboard, console, selector and cupholders, with seat backs at both edges.

## 10. Dilum research retry (does not block 3D-0)

| Source | Result | Classification |
|---|---|---|
| X post 2096280244663775423 (via the public syndication endpoint) | Posted 2026-09-05: "Asked GPT-6 Astra to create a highly detailed, interactive visualization of a V8 engine. The result is pretty impressive", with a video | Verified that the post exists; the content is a creator claim. No source code is linked. |
| YouTube `@DilumSanjaya/videos` | Page loads, but video titles are rendered by JavaScript and were not extracted | Not researched |
| CodePen `dilums` (profile and RSS) | Blocked by Cloudflare (HTTP 403) | Not researched |
| Firecrawl | CLI not installed; MCP previously failed to start | Not retried |

The conclusions in `DILUM_3D_TECHNIQUE_RESEARCH.md` are unchanged. The V8 technique remains unknown.

## 11. Confirmed unchanged

- `public/assets/3d/lexus-rx350/interior-l4-*.glb`: hashes unchanged and pinned by a test.
- No file under `src/` changed: viewer, camera presets, configuration and UI.
- The original repository was not modified; all rebuild work ran in `~/scratch`.
