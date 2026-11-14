# Atelier atmosphere and expanded leather palette
2026-11-14 · Experimental repository only · Owner-requested refinement.

## Delivered
The existing editorial hero now opens on an original imagined upholstery cutting table: leather hides, waxed thread, vintage shears, chalk patterns, grommets and measuring tape. The same image supplies a wide photographic background for the closing invitation, with a dark ink overlay for readable type. Typography, palette, motion controls and navigation remain unchanged.

Five additional digital leather colours join Black, Sienna and Ivory: Oxblood Burgundy (#602C39), Forest Green (#294B40), Midnight Navy (#293D58), Saddle Tan (#AD7950), Warm Stone (#95897B). All eight use the existing catalogue-to-renderer adapter. New options are illustrative, not confirmed workshop stock. Primary/secondary zones, single-colour mode, steering behaviour and duplicate-secondary protection remain intact.

## Verification
- Test-first: five added palette contract cases failed because the new options did not exist; after implementation all 39 unit tests passed.
- Typecheck and lint passed. Normal build passed (3.1s); diagnostic build passed (3.02s). Existing large renderer chunk warning remains.
- Two real browser journeys passed at 1440 and 390 widths (1.5m): each new primary colour reached actual material state, single-colour affected both seat zones, two-tone changed secondary/steering, keyboard selection worked, and the selected green persisted across Classic/Diamond/Perforated.
- Normal-build layout/reduced-motion check passed at 320/768/1024 widths (16.7s total): no horizontal overflow, footer CTA usable, no landing canvas, eight live colour options present.
- Screenshots inspected: desktop hero, desktop/mobile invitation, desktop/mobile live palette. Mobile two-tone may scroll inside the control panel; the live cabin and navigation stay visible.
- No page errors in the two diagnostic journeys; exactly one Studio canvas; no document scrolling in Studio at the tested 900px height.
- An attempted preview start reported port 4173 already in use; the existing server served the rebuilt app successfully. Port 4174 served diagnostics.

## Evidence
[Hero desktop](evidence/atelier/hero-1440.png) · [Hero mobile](evidence/atelier/hero-390.png)
[Invitation desktop](evidence/atelier/invitation-1440.png) · [Invitation mobile](evidence/atelier/invitation-390.png)
[Studio desktop](evidence/atelier/studio-palette-1440.png) · [Studio mobile](evidence/atelier/studio-palette-390.png)
Actual command outputs and material-state snapshots: `docs/evidence/atelier/`.

## Image provenance
Built-in image_gen generated `exec-1d511e31-03a6-423b-96b5-3de553a823a0.png`; original remains in Codex generated_images. Project asset: `src/assets/editorial/atelier-workbench.webp`, 229,954 bytes, WebP quality85/method6. No content editing; reused image means one image download for both placements. Full prompt and SHA256 are recorded alongside this report. It is labelled AI-generated and is not a photograph of the actual AutoLab workshop. Measuring-tape numbers are generated illustration, not reliable dimensional evidence.

## Change Summary
What was built: textured atelier hero and invitation photography; eight working leather colour options.
Assumptions made: retain the approved responsive Editorial Atelier design; added colours are illustrative previews.
Edge cases handled: reduced motion, narrow layouts, keyboard selection, two-tone duplicate prevention.
Failure modes covered: dark background fallback if image fails; existing viewer loading/Retry unchanged.
What was NOT covered: physical-phone/Safari testing, calibrated physical colour matching, geometry or production repository changes.
Confidence level: HIGH for tested functionality; owner visual approval remains open.
Reason: actual browser material-state assertions plus desktop/mobile screenshots support the implementation.
Tests added: five palette contract cases and three browser journeys.
Blast radius: experimental landing imagery, colour catalogue/types and selector presentation only; no model/loader/dependency changes.
