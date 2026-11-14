# Studio Back and reset repair
2026-11-14. Experimental repository only.

## Reproduced
Back from Accent Thread to Colour retained the selected material values but forced the camera from Stitch Detail to Driver Hero. Separately, the unlabelled circular-arrow control immediately reset all configuration and changed Diamond to Classic. The regression test failed on both behaviours before the fix; `evidence/back-fix/red.txt` preserves the output. This does not establish that the actual Back button deleted configuration data.

## Fixed
- Earlier-step navigation retains the current camera and all choices. Forward progression retains the existing guided camera transitions.
- The circular-arrow control now visibly says Reset. It opens a native modal confirmation; Keep my design (the first action) or Escape cancels. Only Reset all choices discards work.
- No changes to assets, renderer, configuration mapping or production repository.

## Evidence
Desktop (1440) and mobile (390) regression journeys PASS, 2/2 in 1.3m. They check Diamond, Forest Green/Warm Stone two-tone and cyan thread through Back, cancellation, specification review and return; actual material state and camera remain stable and the canvas stays mounted. Explicit Reset still restores Classic/material step.
Screenshots and before/after scene snapshots: `docs/evidence/back-fix/`.
Typecheck, lint and all 39 unit tests PASS. Normal build PASS (2.67s); diagnostic build PASS. Existing renderer chunk warning remains.

## Change Summary
What was built: non-destructive backward navigation and clearly labelled, cancellable Reset.
Assumptions made: preserve the selected view when revisiting earlier steps; retain forward camera guidance.
Edge cases handled: review Back, duplicate navigation and cancelling Reset.
Failure modes covered: accidental reset click no longer immediately loses selections.
What was NOT covered: persistence across page reload/browser restart, physical-phone testing or production changes.
Confidence level: HIGH for the reproduced scenarios.
Reason: failing reproduction and passing desktop/mobile browser checks inspect actual cabin state.
Tests added: two browser regression journeys covering Back, camera, material preservation, cancellation and explicit reset.
Blast radius: Studio step navigation and reset control only.
