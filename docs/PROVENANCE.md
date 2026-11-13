# Source and asset provenance

The experimental UI remains governed by `autolab-corpus/`. Owner approval on 2026-11-13 permits reuse of first-party AutoLab assets and viewer code from commit `12558846c5f3635539a45174530a6599dbdbff28` of `Suyanka21/AUTOLAB-DIGITAL-SHOWROOM`.

Exports must use Git objects at that commit. The production working tree contains unrelated edits and is not an import source. No production dependencies, backend, environment files or credentials are copied.

## Existing editorial assets

The JPEGs under `src/assets/images/` and reference PNGs under `public/assets/aistudio/` arrived in experimental commit `4634b1e`. No original-photographer or generation provenance is recorded. Retained for this owner-supplied local demonstrator and labelled illustrative; not evidence of actual workmanship or a licence clearance for public distribution. They do not become 3D textures.

The authentic logo is `autolab-corpus/AUTOLAB LOGO .pdf`; a faithful browser derivative will replace the prototype approximation without modifying the PDF.

## Fonts

The existing Google Fonts request is retained; no font files are downloaded into the repository. Official family licences were inspected 2026-11-13:
- Playfair Display: SIL OFL 1.1, reserved name Playfair Display: https://raw.githubusercontent.com/google/fonts/main/ofl/playfairdisplay/OFL.txt
- Plus Jakarta Sans: SIL OFL 1.1: https://raw.githubusercontent.com/google/fonts/main/ofl/plusjakartasans/OFL.txt

Offline fallback remains Georgia/system sans. Self-hosting requires bundled notices and remains outside this change.

## Runtime resources

The source export manifest will record exact source paths, commit and SHA256 for GLBs, KTX2 previews, camera data, shader, loaders and gate. Decoder licence notices must be included. Three, Fiber, Drei and three-stdlib are MIT packages; this does not change the ownership of AutoLab assets.

## Implementation references

- R3F Vite support / React compatibility: https://r3f.docs.pmnd.rs/getting-started/installation
- Three GLTFLoader decoding extensions and resource handling: https://threejs.org/docs/pages/GLTFLoader.html
- Vite asset paths: https://vite.dev/guide/assets.html
- Vite exposed test-build variables: https://vite.dev/guide/env-and-mode

Authentic logo reused as bytes from 1255884:public/brand/autolab-logo.png (SHA256 ef2da71ac1b447a80375a146f11d33d4bcd8e234503ee5b51711a87165b31234); original corpus PDF preserved. Replaced inherited approximate SVG.

Bundled decoder license texts: https://raw.githubusercontent.com/BinomialLLC/basis_universal/master/LICENSE, https://raw.githubusercontent.com/google/draco/main/LICENSE, https://raw.githubusercontent.com/pmndrs/react-three-fiber/master/LICENSE. MIT notices copied from installed packages to public/licenses.
