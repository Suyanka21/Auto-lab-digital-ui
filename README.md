# AutoLab independent showroom experiment

A Vite / React / TypeScript / Tailwind 4 demonstrator with the committed AutoLab front-cabin renderer. This repository is independent of the authoritative production showroom.

## Run locally

Node >=22.12 is required. From this repository:

```sh
npm ci
npm run dev
```

Development: http://127.0.0.1:5173/studio

For the verified static build:

```sh
npm run build
npm run preview
```

Preview: **http://127.0.0.1:4173/studio**. Port 3000 belongs to the separate production project; it will not show this experiment. `/` is the landing experience; `/studio` directly opens the real cabin. Reload starts a fresh configuration. In-app navigation retains choices.

## Checks

```sh
npm test
npm run typecheck
npm run lint
npm run build
```

Browser contract tests require installed Edge and a test-only build: set `VITE_E2E=1`, run `npm run build -- --outDir dist-e2e`, then `npx vite preview --outDir dist-e2e --port 4174 --strictPort`. Set `TEST_URL=http://127.0.0.1:4174` before running the binding/recovery tests. Use `npm run test:e2e -- --project=runtime` for diagnostics tests and `npm run test:e2e -- --project=release` for the normal build. The unfiltered command runs both projects against their respective servers. Tests run sequentially with software WebGL. Never use `VITE_E2E=1` for the owner preview. `release.spec.ts` targets the normal preview on 4173 and asserts diagnostics are absent.

## Real functionality

- Classic / Diamond Quilted / Perforated use three actual KTX2/Draco GLBs.
- Primary changes seat centres. Secondary changes bolsters, headrests and steering leather. Single-colour applies primary to both zones.
- Accent thread updates stitching and the Diamond thread shader.
- Four exact source camera presets; Driver Hero starts the experience.
- Trim previews update dashboard and console inserts together. Console black and metal parts retain source finishes.
- Ambient previews change local point-light colours, not modelled LED strips.
- Summary reflects current choices. Everything is exploratory; no price, availability or workshop approval is asserted.

## Evidence and boundaries

See [final handoff](docs/FINAL_HANDOFF.md), [execution record](docs/IMPLEMENTATION.md), [provenance](docs/PROVENANCE.md), and [source manifest](docs/SOURCE_MANIFEST.json).

The source commit is `12558846c5f3635539a45174530a6599dbdbff28`. Assets were exported from Git objects, never the dirty production working tree. No production files, geometry or camera coordinates were changed. No merge or deployment.

Photographic reference cards remain illustrative and are not a guarantee of model fidelity. Existing images need rights clearance before public use. Physical samples and real-phone performance require owner review. Decoder/renderer notices are retained in `public/licenses/`.
