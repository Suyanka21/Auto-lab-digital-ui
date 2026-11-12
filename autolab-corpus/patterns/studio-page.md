# Studio Page Pattern

## Objective

Create a focused configuration experience with a prominent automotive cabin presentation stage and a clear configuration panel.

## Desktop layout

- Cabin viewer: approximately two-thirds of the working area.
- Configuration panel: right side.
- Step navigation: clear and compact.
- Specification summary: accessible without disrupting the configuration flow.

## Mobile layout

- Cabin viewer remains dominant.
- Configuration controls appear below the viewer or in a compact bottom sheet.
- Step navigation remains accessible.
- Avoid cramped controls.

## Configuration flow

1. Material
2. Colour
3. Accent Thread
4. Composition
5. Cabin Trim — illustrative preview
6. Ambient Illumination — illustrative preview

## State requirements

Changing material, colour, stitching, composition, trim, or illumination must update:

- The selected control.
- The shared configuration state.
- The specification summary.
- The viewer placeholder or future 3D viewer.

## Camera controls

Provide:

- Driver Hero
- Cabin Pair
- Cockpit & Dash
- Stitch Detail

Camera selection must update the viewer state, even if the current implementation uses a static visual placeholder.

## Completion criteria

- User can navigate forward and backward.
- User can edit earlier selections.
- Progress is clear.
- Specification summary reflects current selections.
- Illustrative options are labelled.
