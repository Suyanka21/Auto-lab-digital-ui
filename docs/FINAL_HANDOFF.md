# Independent showroom - owner handoff

Updated 2026-11-14. Branch: `codex/independent-3d-assessment`.

Latest repair: [Back/reset preservation](BACK_NAVIGATION_FIX.md) keeps the view when revisiting steps and requires confirmation before clearing choices. Current unit suite: 39 passing tests.

Previous refinement: [Atelier imagery and eight-colour palette](ATELIER_REFINEMENT.md) adds workshop atmosphere and five live leather colours. Evidence is in `evidence/atelier/`.

Previous presentation: [Editorial showroom refinement](EDITORIAL_REFINEMENT.md) adds original illustrative material imagery, a cinematic magazine cover and tactile Studio choices. Desktop/mobile screenshots and recordings are in `evidence/editorial/`.

Previous UI refinement: [Cinematic Studio](CINEMATIC_STUDIO.md) keeps the cabin visible, slides between selections and brings review into the same panel. Its screenshots and recordings are in `evidence/cinematic/`.

## Outcome

The existing Editorial Atelier frontend now controls the actual committed cabin. Vite, React, TypeScript and Tailwind 4 are retained. Production stayed read-only. No source working-tree changes were imported; source Git object `12558846c5f3635539a45174530a6599dbdbff28` supplies the renderer, assets and camera contracts.

Owner preview: **http://127.0.0.1:4173/studio**. Landing: http://127.0.0.1:4173/ . Use this address instead of the other application's port 3000. `npm run preview` restarts it if the local process stops.

## Delivered and checked

- Three real treatments, primary/secondary colours, accent thread including Diamond shader, and single/two-tone composition.
- Four unchanged camera coordinates/orbit limits, starting at Driver Hero.
- Shared dashboard/console trim updates and five illustrative point-light colours.
- One live WebGL canvas; lazy viewer bundle; KTX2/Draco, 45-second loading timeout, error boundaries and Retry retained.
- Accurate source zone descriptions and diagram; steering uses effective secondary colour. Console black/metal stays fixed.
- Authentic committed brand logo; no approximate replacement emblem. Editorial palette, typography and landing retained.
- Arrow/Home/End radio navigation, disabled-secondary skipping, mobile menu focus/escape, reduced motion, URL history and current-state specification.
- No unsupported commercial approval claims; samples and illustrative finishes remain explicitly labelled.

## Validation evidence

| Check | Actual result / evidence |
|---|---|
| Adapter red-to-green | 12 failing contract tests before implementation, then pass; phase-2 evidence |
| Unit suite | 34/34 across five files; `evidence/final-tests.txt` |
| Typecheck / ESLint | exit 0; final and release logs |
| Normal production build | exit 0, 5.11 seconds; `evidence/release-build.txt` |
| Three GLB gates | PASS, exit 0; `evidence/{classic,diamond,perforated}-gate.json` |
| Actual scene bindings | PASS, all treatments/colours/thread/composition/cameras/trims/lights; `evidence/phase3-static-bindings-corrected.txt` |
| Responsive / core recovery | 6 browser tests PASS in 2.2m; `evidence/final-browser.txt` |
| Desktop scene | 24 draw calls, 66,260 triangles; KTX2 compressed mip chains observed; `evidence/final/desktop-metrics.json` |
| Widths | 320, 390, 768, 1024, 1440 px; no document overflow; `evidence/final/responsive.json` |
| Source binary integrity | All copied GLB/KTX2/WASM bytes compared to import hashes; `evidence/final/asset-integrity.json` |

Additional validation: KTX2 transcoder and trim-texture failure/Retry tests both PASS (1.1m), `evidence/decoder-trim-recovery-rerun.txt`. Normal-build route, keyboard, menu-resize and recorded real-asset checks all PASS (4 tests, 3.0m), `evidence/release-browser.txt`. The three fetched GLB SHA256 values exactly match the source; normal-build diagnostics are absent. Across the targeted runs, 11 distinct browser scenarios pass. The standalone earlier smoke spec was superseded by these broader checks, not counted as a new pass. Historical source tests are not counted as experiment tests.

**Presentation readiness: READY for a controlled owner demonstration, with visual-fidelity and physical-device limitations below explicitly disclosed. This is not production or human visual acceptance.**

## Screenshots and recording

- `evidence/final/showroom-interactions.webm`: recorded real interactions from the normal build.
- `evidence/final/release-console.png`: normal-build Cabin Pair showing gear console.
- `evidence/final/release-network.json`: fetched GLB hashes, zero page errors, diagnostics absent.
- `evidence/final/desktop-studio.png`: default real Driver Hero.
- `evidence/final/mobile-studio.png`: 390px Studio.
- `evidence/final/mobile-two-tone.png`: mobile controls, corrected zones and two-tone scene.
- `evidence/final/desktop-welcome.png`: existing landing with truthful sample language.
- `evidence/interactions/diamond-two-tone.png`: actual Diamond and colour interaction before final copy/branding changes.
- `evidence/interactions/cabin-console.png`: real cabin/console view.
- `evidence/final/recovery-error.png`: intentionally failed GLB with working controls.

## Measured performance and limits

The desktop test measured 9,326 ms from navigation to render success on installed Edge with **SwiftShader software rendering**. This is one local observation including page loading, not a phone benchmark or GPU timing. Renderer counts are observations, not estimates of GPU memory. After cycling assets the loader cache retains resources; a representative three-treatment run reports 34 textures / 84 geometries. No hardware FPS, thermal or real-phone claim is made.

GLB sizes: Classic 3,650,764; Diamond 3,787,228; Perforated 3,509,764 bytes. All exceed the inherited 3.5 MB soft target, pass the 5 MiB hard limit and meet 80k triangle / 24 call gates. Khronos reports expected unsupported Draco/Basis extension inspection warnings; browser decoding supplies additional runtime evidence. Original geometry is unchanged.

The normal viewer chunk is 1,071.95 kB minified / 297.06 kB gzip, loaded only on entering Studio; main JS 287.89 kB / 84.25 kB gzip. Vite's >500 kB chunk warning remains visible. Existing large sample photos and remote Google Fonts remain loading dependencies. No extra permanent WebGL context or decoration library was introduced.

## Known limitations / owner review

- Seat normals/faceting and inflated highlights remain visible; Diamond geometry/normal detail does not match photographic samples.
- Cockpit/steering and junctions are simplified; some camera views obscure components. Source coordinates remain unchanged by approval.
- Veneer previews use approximate mapping over existing carbon UVs; lighting is a wash, not physical LED-installation evidence.
- Human visual acceptance, physical material samples, actual workshop availability and real-phone performance remain open.
- Existing photographic assets have unresolved public-use provenance. This is a local owner demonstrator, not a cleared public launch.
- Runtime audit recorded zero vulnerabilities; after the Vite security patch seven moderate development findings remain in the ESLint/typescript-eslint/minimatch tree. No forced downgrade or unrelated upgrade was made.
- Configuration remains in React memory through in-app navigation. Reload intentionally starts defaults. No backend, saved orders, pricing or production handoff integration was added.

## Failure history, without hiding results

Initial TypeScript 7 install conflicted with lint peers; corrected to 5.9.3 without force. One generated file had Windows encoding and was rewritten as UTF-8 after an actual build failure. Early browser runs were disrupted by development HMR; fixed static builds prove the runtime, and watch/CSS scope now excludes evidence/build output. A trim locator incorrectly assumed visible label preceded image alt text; corrected the test. Exact camera assertions were corrected for floating-point tolerance without changing coordinates. A baseline screenshot helper produced four images but stalled during cleanup; it is not counted as a passing test. Decoder tests after the overnight session initially saw connection refused; the test preview was restarted and the failed log retained.

## Rollback boundaries

- `3b07f48`: reproducible dependencies and adapter contracts.
- `e5b5e31`: real viewer/asset integration and binding evidence.
- `62a17f9`: accurate branding/material presentation.
- `ffeb846`: route, accessible/responsive interaction and recovery evidence.
- Final verification/documentation commit follows these. Revert the relevant experiment commit if needed; never apply these operations to production.

## Change summary

What was built: working independent real-3D showroom retaining the existing Editorial Atelier frontend.
Assumptions: source material zones and original cameras are authoritative; sample offerings are not commercial approvals.
Edge cases handled: missing secondary input, disabled same-colour secondary, keyboard cycling, narrow layouts, navigation/remount, failed loading and lost context.
Failure modes covered: loading/error/Retry retain selections; unavailable WebGL leaves configuration and summary usable; code-chunk reload explicitly warns it resets configuration.
Not covered: geometry repair, physical-phone/hardware GPU validation, public image clearance, backend/production changes, merge or deployment.
Confidence: MODERATE for presentation readiness, HIGH for the tested desktop runtime contracts; human visual and physical-device review remain necessary.
Tests added: adapter contracts, source loader/shader/trim/gate regressions, actual-scene bindings, route/keyboard/responsive/fault recovery and normal-build asset checks.
Blast radius: experimental repository only; copied binaries remain unchanged and production remains read-only.
