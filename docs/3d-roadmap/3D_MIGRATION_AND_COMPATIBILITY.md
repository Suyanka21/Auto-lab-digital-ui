# 3D migration and compatibility

Date: 2026-11-15. Scope: what any new or improved GLB must satisfy so Astra's showroom keeps working.

Copying a GLB is not enough. The live cabin depends on seven contracts below.

## 1. Runtime contracts (verified in `src/viewer/RuntimeViewer.tsx` and `src/lib/three/`)

| Contract | Current behaviour | Rule for new assets |
|---|---|---|
| Material names | Viewer finds `MeshStandardMaterial`s by name and throws if `MAT_Seat_Primary` exists without `MAT_Seat_Secondary` and `MAT_Seat_Stitching` | Keep all 10 names. New surfaces get new names; never rename existing ones. |
| Required textures | Viewer throws if seat textures fail to decode | Seat slots keep base, ORM and normal maps |
| Thread mask | `thread-mask.ts` patches `MAT_Seat_Primary` via `onBeforeCompile`, reading the ORM alpha in Diamond; cache key `autolab-l4a-thread-v1` | Keep the mask channel, or bump the cache key and its test |
| Trim | `cabin-trim.ts` swaps maps on `MAT_Console_Carbon` from four KTX2 files and shares the PMREM | Trim surfaces keep the same UV scale, or the trim KTX2 files are rebaked |
| Decoders | Draco and Basis decoders served locally from `public/` | No CDN; keep extension set |
| Cache revisions | `lexus-runtime-assets.ts` appends `?v=<sha256>`; a test checks it against the file | Update hashes in the same commit as the asset |
| Cameras | Four preset IDs; orbit limits `0.35`–`4` distance, no pan | New geometry must not sit inside any preset's near plane |

The configuration adapter (`ConfigurationProvider` → `mapConfigurationToRuntime()` → viewer) is the only place UI state turns into material values. 3D work changes assets and viewer internals, not the adapter's inputs.

## 2. Budgets

| Budget | Current | Source |
|---|---|---|
| Triangles per GLB | 66,260 (hard limit 80,000) | Inherited gate output |
| Draw calls per GLB | 24 (limit 24) | Inherited; D0 kept the 24 limit per exported GLB |
| Scene draw calls | 24 measured | D0; floor and shadow plane would add 2 |
| Bytes per GLB | 3.51–3.79 MB (cap 5,242,880) | Verified bytes |

Any increase is an owner decision, measured on the workshop PC first.

## 3. Migration order (each a separate PR)

1. **Port the asset gate.** Make `scripts/validate-glb.mjs` run against files that exist in this repo, with self-made fixtures (pattern from original PR #1). Today it fails with "0 nodes".
2. **Port the `hero_driver` reframe** (`[1.9, 1.25, 0.2]`) as data only, after the owner confirms the default camera. Codex recommended Cabin Pair as the default; that decision stays with the owner.
3. **Reference the Blender sources** from the original repo at commit `b5338d3`, or copy them with a provenance note. Do not copy `docs/review/` history.
4. **Then** start asset work (see the fidelity plan).

## 4. Swap and rollback procedure for a new asset

1. Build from a committed Blender script; record Blender and KTX versions.
2. Run the asset gate; paste real output and SHA-256.
3. Load in the viewer behind a test-only switch; run the binding, thread-mask, trim and recovery tests.
4. Compare fixed renders from all four presets against the current asset.
5. Swap the URL and hash in one commit. Rollback is reverting that commit; the old GLBs stay in history.

## 5. Open compatibility decisions

- Multi-part loading (needed for the full cabin): the viewer loads one GLB per treatment today. Loading zones separately (front cabin, doors, rear, headliner) needs a design for shared material instances so one colour choice reaches every part.
- Whether new trim zones (door inserts, dashboard band) reuse `MAT_Console_Carbon` or get a new slot.
