# Independent showroom integration — technical assessment

Date: 2026-11-13. Status: APPROACH PROPOSED; implementation awaits owner approval.

## Repository boundary and evidence

- Experimental repository: `Suyanka21/Auto-lab-digital-ui`, local baseline `4634b1e`, initially clean on `main`; assessment branch `codex/independent-3d-assessment`.
- Source repository: `Suyanka21/AUTOLAB-DIGITAL-SHOWROOM`, inspected read-only. Source HEAD `b9f2556aa11dc8c4aee93cc94cecfb5a11b358e5`; working viewer is from `12558846c5f3635539a45174530a6599dbdbff28`. Subsequent commit adds preserved Blender sources and documentation, not viewer changes.
- Production has unrelated uncommitted AI Studio/configuration changes. Do not import its whole working tree or current package.json/types. Export specific committed files and assets, with source paths, commit, hashes and applicable notices recorded in the experiment.
- Read every Markdown file in `autolab-corpus/`, including AGENTS, four rules, five patterns, prompts 00–06, assets/references/handoff READMEs; rendered and inspected the supplied logo PDF. Inspected the desktop/mobile reference compositions under `public/assets/aistudio/` and the React implementation.
- Corpus prompts describe an earlier placeholder-building sequence. Preserve their design and contracts; do not replay generation. The current owner request explicitly permits read-only production inspection/reuse, superseding the corpus handoff's older prohibition on connecting to that repository.
- This is a source/asset feasibility assessment, not a completed browser or visual acceptance audit. No production files, services or Git refs were changed. No implementation, dependency installation, deployment or merge occurred.

## Recommendation

Retain Vite, React, TypeScript and Tailwind 4. Keep the existing shell, landing, six selectors, summary, central state and typed CabinViewer boundary. Port the proven renderer behind that boundary with one explicit configuration adapter and one canvas. Do not import the production Next.js application or its backend dependencies.

R3F officially supports Vite directly and pairs Fiber 9 with React 19: https://r3f.docs.pmnd.rs/getting-started/installation . Vite produces a static application bundle: https://vite.dev/guide/ . Next.js adds migration work without serving a requirement in this frontend-only experiment.

## Corpus audit — what to retain and what is missing

| Corpus area | Existing implementation worth retaining | Gap / precise correction after approval |
|---|---|---|
| 00 setup; AGENTS; visual-direction | All eight core palette tokens; Playfair Display / Plus Jakarta Sans hierarchy; reusable primitives; all prescribed component boundaries; centralized typed configuration | No lockfile or installed dependencies. Pin a reproducible, peer-compatible baseline. `lint` currently means TypeScript only; add a real lint check and tests. TypeScript strict mode is absent. |
| 01 landing; landing pattern | Required headline and CTA; four craft disciplines; walkthrough; local illustrative imagery; restrained hairlines and cyan | CTA changes React state, not `/studio`. Add URL/history handling and direct-route/Back checks. Correct unsupported business claims rather than treating catalogue flags as owner approval. |
| 02 shell; studio/viewer patterns | Desktop 8/12 viewer and 4/12 panel; mobile viewer before controls; four camera buttons; explicit eight-field viewer props | CabinViewer changes photographs, labels and swatches only. No canvas, loaders, renderer recovery or actual material changes. Replace its interior; preserve outer layout and external controls. |
| 03 configuration; configuration/summary patterns | Three distinct treatment previews; three colour choices; thread options; two compositions; trim/lighting labelled illustrative; previous/next/reset; editable summary with camera | Primary/secondary surface descriptions conflict with real slots; console and armrest cannot follow seat colour under current bindings. Correct wording/diagram. Ambient copy promises perimeter light lines that the source only approximates with local light washes. |
| 04 responsive; responsive rules | Purposeful mobile step strip, 4:3 mobile stage, 16:9 wider stage, 44px+ buttons and compact selectors | Source intent is not browser proof. Check 390×844, 1440×900 and intermediate widths, touch orbit vs page scroll, long labels, zoom and focus visibility. Avoid using body overflow hiding as proof of no overflow. |
| 05 audit; anti-slop/content | No prices, fake reviews, awards, order submission or decorative animation loops found; neutral editorial controls; CSS reduced-motion handling | Custom buttons with radio roles have no arrow-key/roving-focus handling. Mobile overlay menu has Escape but no focus containment/return or background inertness. Remedy and verify. Check contrast/readability of 10–12px secondary text in browser. |
| 06 handoff; assets/references | README has architecture, file map and viewer replacement instructions; local image files; fonts named explicitly | README surface mapping is inaccurate; Node 18 minimum needs reconciliation with resolved Vite toolchain. No image/font provenance or licence ledger. Hand-drawn SVG logo differs from supplied PDF; use faithful derivative. Add source manifest, tests, limitations and measured evidence. |

Additional findings:
- The four reference images are art direction, not screenshots of the running app or evidence of existing capabilities. Written studio instructions specify six steps; reference compositions show four primary steps plus supplementary trim/light presentation. Preserve existing six-step implementation, retaining the illustrative labels, rather than reopening the information architecture.
- The corpus approves Nairobi workshop identity and exploratory copy; `classification: confirmed`, “tailored in-house”, “engineered for breathable contact surfaces” and detailed offering claims in `catalog.ts`/`LandingPage.tsx` need an owner-backed offering record. A label in generated code is not proof. Use neutral sample/exploration language until confirmed.
- The local image directory has 28 JPEGs totalling 19,556,563 bytes; this is repository size, not measured network transfer. Several versions are unused. Four camera images are mounted eagerly in the placeholder. Lazy-load the real viewer on Studio entry and audit only shipped imagery; avoid copying unused image generations.
- Existing `@google/genai`, `express`, `dotenv` and `motion` have no application imports found. Do not inherit unnecessary API/server/animation dependencies. Remove verified-unused entries as a small dependency-baseline change after approval.
- External Google Fonts are a network dependency; no licence records are bundled. Verify notices and provenance before any self-hosting. No third-party imagery/font download is authorized by this assessment.

## Integration architecture and actual contracts

`ConfigurationProvider -> CabinViewerProps -> pure mapConfigurationToRuntime() -> ported viewer -> actual shared GLB materials/lights/camera`

Keep one state owner; do not bring in the production ConfiguratorProvider, database catalogue, Next routes, concierge backend assumptions or historical Mercedes paths. Runtime-local state is limited to loading/errors, camera interaction, decoder/resource ownership and statistics.

| Experimental selection | Runtime mapping / boundary |
|---|---|
| classic / diamond-quilted / perforated | classic / diamond / perforated; select the three complete `interior-l4-*.glb` assets, not a synthetic fixture or seat-only file |
| primaryColour | Resolve catalogue sRGB hex to `MAT_Seat_Primary`: cushion/backrest centres |
| secondaryColour, composition | Single-colour sends primary to both seat slots. Two-tone sends the second hex to `MAT_Seat_Secondary`: outer bolsters/headrests/side bands. Keep existing different-colour invariant. Correct prototype copy instead of swapping geometry/material assignments. |
| accentThread | Resolve catalogue hex to `MAT_Seat_Stitching`; retain Diamond ORM-alpha shader mask on primary seat material and its cleanup/program cache key |
| four camera IDs | driver-hero -> hero_driver; cabin-pair -> cabin_pair; cockpit-dash -> driver_cockpit; stitch-detail -> seam_macro. Reuse numeric presets/orbit limits unchanged. |
| carbon-fibre / poplar-wood / walnut-wood / piano-lacquer | autolab-twill-carbon / open-pore-poplar / open-pore-walnut / piano-lacquer-flowing-lines; update shared `MAT_Console_Carbon` on dashboard, selector surround and console inserts |
| ambientIllumination | Resolve experiment's five existing hex values into source local point lights; illustrative wash, not dimensioned LED strips or measured brightness |

Preserve all seven original live slot capabilities plus the three console slots. `MAT_Dashboard_Trim` means dashboard leather, not decorative carbon. Console black/metal and armrest remain their existing finishes. Proposed adapter follows the source behaviour of steering leather using the effective secondary colour; dashboard leather, cockpit black and metal accent retain source defaults. Do not expose extra controls.

Keep experimental colour/thread/light swatch values, rather than silently substituting production catalogue values; they remain screen previews requiring physical sample confirmation. Surface terminology changes require approval below.

### Files/resources to reuse selectively

- `src/components/configurator/SpikeViewer.tsx`: renderer, demand frames, camera rig, readiness, Suspense/error boundary, 45-second timeout, Retry and context-loss handling. Restyle status chrome to corpus; retain behaviour.
- `src/lib/three/{ktx2-runtime,thread-mask,cabin-trim}.ts`: renderer-owned KTX workers, load settlement/cleanup across StrictMode and Retry, quilt thread shader, bounded trim texture ownership/carbon restoration.
- `src/config/lexus-camera-presets.ts`, `lexus-runtime-assets.ts`, `trim-preview-assets.json`, relevant front-cabin manifest, and the small trim-ID contract.
- Three GLBs; four baked trim KTX2 files; local `public/basis/` and `public/draco/` decoder resources with notices. No external CDN at runtime.
- Relevant slot/loader/shader/cache/recovery tests and asset validator, adapted to the experimental paths and test harness. Export from the chosen source commit, not dirty working files.

Framework adaptations: replace `process.env.NEXT_PUBLIC_E2E` with an explicitly gated Vite test-build variable; preserve diagnostics absence in normal builds. Adjust aliases and type-only imports; remove Next-only shell concerns. Use React lazy/Suspense at Studio boundary. Respect Vite base URL for model/decoder paths. Keep hash-versioned assets and validate fetched bytes so stale cached console-free models cannot recur. Vite environment reference: https://vite.dev/guide/env-and-mode .

Candidate source-compatible matrix: React/DOM 19.3.1, Three 0.186.1, Fiber 9.8.2, Drei 10.7.9, three-stdlib 2.36.1 and matching types. These are source versions inspected, not a verified experimental install. Verify registry availability/peer resolution, pin exact versions and create the experiment's own lockfile. Directly declare three-stdlib because the loader imports it. Retain Vite/Tailwind rather than copying the Next/Tailwind 3 toolchain. Installed source packages declare MIT for Three/Fiber/Drei/stdlib; preserve actual licence texts and decoder notices when copying. Owner permission covers first-party reuse, not automatic third-party relicensing.

## Actual asset inspection and inherited evidence

Read GLB headers/JSON and independently hashed current source assets with Node (exit 0). All require `KHR_draco_mesh_compression` and `KHR_texture_basisu`; each has 11 nodes and the expected 10 named materials.

| Treatment | Bytes | SHA256 |
|---|---:|---|
| Classic | 3,650,764 | e5bdde016348df34889ec4c0ff0e406caad7e368504308bd5a4f5b725a55c056 |
| Diamond | 3,787,228 | 4c217dd00d86d8bae3925d735beddb63b225d24c5f1bafd60726f501bfcba8ad |
| Perforated | 3,509,764 | d53f55546232db473ecadee08be9bff6454b5d3a510ee30e88415f2477ca9f9e |

Source `docs/review/live-trim-2026-11-11/REPORT.md` and its evidence record gate passes, 66,260 triangles/24 calls, 123 unit tests passing, focused browser reruns and a build pass. These are HISTORICAL SOURCE results, not tests of this experiment. The model is already at the documented draw-call budget; do not add postprocessing, shadow passes or extra geometry casually. Existing gate warnings and visual defects remain open.

Source cold loads were roughly 12–13 seconds in software-rendered browser tests; this is not a phone/GPU benchmark. Strong console reflections, seat shading/faceting, simplified cockpit geometry, junctions and veneer UV approximation remain known limitations. Real assets will not match the photographic placeholder's visual fidelity. No remodelling or human acceptance is implied.

Current experiment verification: `Test-Path node_modules` -> False; `git ls-files '*lock*' '*test*' '*LICENSE*'` -> no results. Node v22.23.2/npm 11.6.0 available. Build, typecheck, tests and browser checks NOT RUN: dependencies are absent and this deliverable stops before implementation/setup. PDF inspection first failed because Python fitz was absent; existing Poppler rendered it successfully without installing software. No screenshots are presented as actual experimental runtime evidence.

## Controlled phases and rollback boundaries

1. **Audit (this deliverable):** corpus/source inventory, capability mismatches and owner decisions. Documentation-only commit; no application changes.
2. **Integration architecture/baseline:** after approval, reproducible install/lockfile, exact source manifest/licence ledger, pure adapter and failing contract tests, existing-app baseline screenshots/build. Resolve `/studio` and source terminology. Checkpoint: baseline runs; revert this commit to untouched prototype.
3. **3D integration:** minimal renderer port plus assets/decoders; verify all three treatments, primary/secondary/thread/composition, four presets, trim/carbon restoration and five light colours against actual scene state. Gate hashes and validate KTX/Draco. Checkpoint: real bindings, one canvas and working Retry; revert renderer slice to explicitly illustrative placeholder.
4. **Visual refinement:** retain Editorial Atelier tokens, landing and controls; refine scene framing/presentation and bounded transitions only after bindings pass. Start from source lighting; no asset redesign, new shaders for decoration or permanent extra context. Separate presentation commit.
5. **Responsive refinement:** desktop/mobile/intermediate layouts, keyboard radios/menu, reduced motion, touch navigation, route history, failure/recovery. Separate interaction commit; retain working renderer underneath.
6. **Final verification:** unit/contract tests, real lint, typecheck, static production build, GLB gates, browser screenshots/short recording, rapid switches, remounts, missing GLB/decoder/trim texture, no-WebGL/context loss, cache revisions, network/console and renderer counts. Capture physical-phone results only if a real device is available; otherwise NOT TESTED. Report each phase and stop for owner review; no merge/deployment.

Each phase has a small reversible commit and evidence report. Do not treat screenshots alone as proof that material changes reached the scene. Test unexpected callbacks after switching, disposal during decode, missing secondary colour and return from error without state loss.

## Approval required

Approve one scoped approach: retain Vite and the existing corpus UI, reuse the committed source viewer/assets with the adapter above, add only renderer/testing dependencies and necessary baseline cleanup, and execute phases 2–6 with reports.

Specific decisions within that approval:
1. Accept accurate surface zoning: primary centres, secondary bolsters/headrests, source steering relationship; fixed console black/metal. Update conflicting copy/diagram rather than invent console recolouring or change the GLB.
2. Recommend Cabin Pair as initial camera so the gear console is visible immediately; retain all four exact presets. This changes the prototype's default Driver Hero, not its available views.
3. Retain current illustrative trim/light previews and sample swatch values; make no workshop availability or LED-installation claim. Supply/confirm an offering record before the UI calls specific options commercially confirmed; until then use neutral exploratory wording.

Reuse permission is already granted and does not need to be requested again. No approval is sought for new geometry, backend features or deployment.

## Change summary

- Built: documentation-only technical assessment and dedicated experimental branch.
- Assumptions: corpus governs design; committed source governs existing 3D capability; framework recommendation awaits approval.
- Edge cases/failure modes: identified adapter defaults, stale caches, decode/Retry/resource ownership, keyboard and state persistence requirements; not implemented here.
- Not covered: runtime/browser verification, install/build, geometry work or production changes.
- Confidence: MODERATE overall; source mapping is evidenced, experimental compatibility and visual results require the approved install and browser phases.
- Tests added: none; read-only source, GLB metadata and SHA checks only.
- Blast radius: experimental documentation/Git branch only; production untouched.
