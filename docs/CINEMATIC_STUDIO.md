# Cinematic Studio refinement
Owner request: keep the cabin visible during selection, reduce scrolling, introduce horizontal editorial progression.
Scope: experimental UI only; keep palette/type, real bindings, asset bytes and cameras unchanged.
Layout: viewport-contained studio, dominant stage plus one sliding selection rail; compact bottom controls on mobile.
Motion: 420ms directional rail; no duplicate canvas, no continuous animation; reduced-motion removes sliding.
Navigation: six existing steps, next/back, direct chapter jumps, horizontal touch swipe on panel text; review uses the same rail.
Acceptance: real selections and summary work, cabin remains in viewport, no document scroll at desktop/mobile, errors remain usable, keyboard and reduced motion supported.
Original desktop/mobile overflow reproduced first by cinematic.spec.ts. Final evidence appended after browser validation.

Camera guidance: changing steps selects an existing preset (Driver Hero for material/colour/composition, Stitch Detail for thread, Cabin Pair for trim/light). Numeric camera presets, orbit limits and the viewer implementation are unchanged. Manual cameras remain available.
On short displays and in specification review, only the control pane can scroll; the stage and Back/Continue stay visible. The landing page keeps normal document scrolling.

## Verification
- Regression before change: desktop cabin y=-306.6px and mobile y=-281.1px after selecting an option; both failed visibility checks.
- Updated actual bindings + desktop and mobile full journeys: 3 browser tests PASS (5.3m). Cabin within viewport; document scroll zero; specification in the same panel; one canvas.
- Unit suite: 34/34 PASS, including original material/loader/gate contracts. Typecheck and lint exit 0.
- Normal build PASS (3.10s); no new dependencies. Main JS now 269.42kB vs previous 287.89kB. Viewer remains lazy, with its existing large-chunk warning.
- Reviewed real desktop/mobile screenshots. Source assets unchanged; apparent source geometry/shading defects remain visible and unapproved.
- Motion harness first lacked the required Touch identifier; corrected with actual Touch/TouchEvent construction. Resize assertion initially sampled the previous height before reflow; screenshot showed fitted layout, so the assertion now waits for layout settlement. Failed logs retained.
- Desktop/mobile interaction videos and screenshots are under evidence/cinematic. Final owner-preview and reduced-motion outcomes are appended below.

## Change summary
What was built: a cabin-centred, viewport-contained Studio with a horizontally sliding configuration rail and review panel.
Assumptions: retained Editorial Atelier palette/type and existing sample choices; guided cameras reuse approved numeric presets.
Edge cases handled: short screens, internal control/review overflow, keyboard radios, backward/direct navigation, touch cancellation and reduced motion.
Failure modes covered: original loading/error/Retry renderer remains in its stable stage; UI movement never duplicates or remounts the WebGL viewer.
What was not covered: model refinements, new material capabilities, physical-device testing, production changes or deployment.
Confidence: HIGH for measured layout/bindings; owner judgement remains necessary for motion preference and inherited visual fidelity.
Tests added: desktop/mobile no-scroll journey, simulated touch/back, reduced-motion keyboard behaviour, camera guidance, persistent canvas and normal-build viewport checks.
Blast radius: experiment presentation components and browser tests only; original renderer and asset bytes unchanged.

## Final completion evidence
- Final motion test PASS (45.8s): simulated touch swipe/back, keyboard, reduced-motion CSS, preserved canvas, existing camera guidance and viewport fitting at 320x568, 768x1024 and 1024x768.
- Navigation regression: 3/3 PASS (51.9s), including direct URL, history, keyboard radio controls and mobile drawer resizing.
- Normal release browser: 2/2 PASS (2.2m). All three fetched GLB SHA256 values match the imported source, no test diagnostics, no page errors; desktop/tablet/mobile screenshots show the actual cabin and live Sienna selection.
- Recovery: 2/2 PASS (59.4s). Failed GLB and context loss recover through Retry while retaining colour; unavailable WebGL preserves selections and the review pane.
- Total current browser scenarios: 11 PASS across focused runs. Logs are cinematic-browser.txt, cinematic-motion-final.txt, cinematic-navigation.txt, cinematic-release-browser.txt and cinematic-recovery.txt.
- Final npm run typecheck and npm run lint both exited 0 after all source/test edits. Earlier failures remain recorded; no source changes followed the successful final production build.
- Reviewed owner-colour-1440.png, owner-colour-768.png and owner-colour-390.png. The colour-1440.png capture shows a loading transition, not a completed-render claim.
- owner-showroom-interactions.webm records the normal release. journey-1440.webm and journey-390.webm record the guided desktop/mobile flows.
- Historical handoff images were restored; this refinement's evidence is isolated in evidence/cinematic. Touch was simulated in Edge; physical phones and hardware GPU performance remain untested.
- All modifications are confined to the experimental branch. Production, model assets, viewer source, dependencies, numeric cameras and orbit limits are unchanged.
