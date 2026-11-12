# Prompt 06 — Handoff Preparation

Use after the audit is complete.

```text
Prepare the AutoLab Digital Showroom for handoff to a future engineering agent that will integrate the real AutoLab GLB assets and existing Three.js / React Three Fiber viewer.

Do not connect to or modify the existing AutoLab production repository.
Do not add backend, authentication, payments, database, or external API functionality.

Complete the following:

1. Review the component structure.
2. Ensure configuration state is typed and centralized.
3. Ensure presentation components are separate from configuration logic.
4. Ensure `CabinViewer` has a clear, replaceable props interface.
5. Ensure no component hard-depends on fake 3D data.
6. Ensure design tokens are reusable.
7. Ensure the README explains how to run the prototype.
8. Ensure the README explains how to replace the viewer.
9. Ensure the specification summary accurately reflects current selections.
10. Ensure illustrative options are clearly labelled.
11. Ensure no unsupported commercial claims remain.

Then provide:
- A concise architecture overview.
- A file map.
- The viewer replacement instructions.
- A list of known limitations.
- A list of remaining visual-polish opportunities.

Do not claim the prototype is production-ready.
```
