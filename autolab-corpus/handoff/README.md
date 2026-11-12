# Future Integration Handoff

This prototype will be exported as source code and handed to another engineering agent for integration with AutoLab’s existing Three.js / React Three Fiber 3D configurator.

## Requirements

- Clear component structure.
- Reusable design tokens.
- Typed configuration state.
- Replaceable viewer interface.
- No hard dependency on fake 3D data.
- No backend requirements.
- README explaining how to run the prototype and replace the viewer.

## Viewer replacement

The future agent should replace `CabinViewer` with the real AutoLab viewer while preserving:

- Configuration state.
- Camera controls.
- Specification summary.
- Responsive layout.
- Component boundaries.

## Prohibited

- Connecting to or modifying the existing AutoLab production repository.
- Adding backend infrastructure.
- Adding authentication.
- Adding payments.
- Adding database tables.
- Adding external APIs.
