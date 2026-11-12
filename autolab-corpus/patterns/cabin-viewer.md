# Cabin Viewer Pattern

## Objective

Create a replaceable viewer component that can later receive AutoLab’s real GLB assets and existing Three.js / React Three Fiber rendering engine.

## Component contract

```tsx
type CabinViewerProps = {
  material: MaterialId;
  primaryColour: ColourId;
  secondaryColour?: ColourId;
  accentThread: ThreadId;
  composition: CompositionId;
  trim?: TrimId;
  ambientIllumination?: IlluminationId;
  activeCamera: CameraId;
};
```

## Implementation rules

- Keep viewer state separate from configuration state.
- Do not embed configuration logic inside the viewer.
- Do not hard-code a specific 3D engine.
- Provide a clean props interface.
- Use a visual placeholder if no real 3D asset is available.
- Label placeholder imagery as illustrative.
- Do not fake unrestricted rotation.
- Do not build an unrelated 3D car model merely to fill the viewport.

## Placeholder behaviour

Use high-quality automotive cabin imagery and meaningful camera-state transitions.

For each camera option:

- Driver Hero
- Cabin Pair
- Cockpit & Dash
- Stitch Detail

Use a restrained transition between states. Do not imply full 3D navigation if it is not implemented.

## Future integration

The future engineering agent must be able to replace the placeholder without rebuilding the interface.

Provide:

- Clear component boundary.
- Typed props.
- No fake 3D data dependency.
- README instructions for replacing the viewer.
