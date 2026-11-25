# Runtime integration contract at the publication base

The application remains Vite / React / TypeScript / Tailwind 4 with one React Three Fiber viewer. This handover adds no application dependency and changes no production file.

Authoritative implementation: `src/viewer/RuntimeViewer.tsx`, `src/viewer/configuration-adapter.ts`, `src/config/lexus-camera-presets.ts`, `src/config/lexus-runtime-assets.ts`, `src/lib/three/{ktx2-runtime,thread-mask,cabin-trim}.ts`, `src/config/scene-manifest.front-cabin.json` and `scripts/validate-glb.mjs`.

Seven live bindings: `MAT_Seat_Primary`, `MAT_Seat_Secondary`, `MAT_Seat_Stitching`, `MAT_Steering_Leather`, `MAT_Dashboard_Trim`, `MAT_Cockpit_Accent`, `MAT_Cockpit_Black`. The shipped baseline has ten slots: MAT_Console_Black, MAT_Console_Carbon and MAT_Console_Metal remain part of the asset contract. Do not truncate the manifest to seven materials.

- Classic, Diamond and Perforated load different verified GLBs. Existing KTX2/Draco decoding and recovery must remain intact.
- Single-colour maps secondary to primary; two-tone retains the selected secondary; steering follows secondary. Fixed dashboard/structural/metal accents are not seat-colour fields.
- `MAT_Console_Carbon` is the existing shared finish-preview slot for dash/console; its name persists for wood previews. R2 door assignments are proposals using this existing slot, not independent door controls.
- Accent thread updates actual stitching and the Diamond-specific shader mask. The Diamond ORM alpha mask is not proof that Classic/Perforated can discard their stitch geometry. Preserve UV0 and tangent orientation during baking/export.
- Initial camera remains Driver Hero (`hero_driver`); Cabin Pair (`cabin_pair`), Cockpit & Dash (`driver_cockpit`), Stitch Detail (`seam_macro`) remain accessible. Reuse exact coordinates/orbit limits. Offline review cameras are separate.
- Preserve configuration state, reference generation, copy/specification/WhatsApp semantics, Retry and fallback behaviour. Trim/illumination options remain illustrative where that is the current offering status.

Complete-cabin per-GLB ceilings: 80,000 decoded triangles, 24 primitives as draw-call proxy, 5,242,880 bytes. The detailed R4 master is outside this budget by design. Runtime transformation must be separately authored and tested; no R4 runtime equivalence is claimed.

Independent door upholstery, headliner colour and starlight enabled/intensity/twinkle controls require explicit design/API approval. Existing proposed `MAT_Headliner` is not a shipped slot. Do not expand UI options to accommodate master materials.
