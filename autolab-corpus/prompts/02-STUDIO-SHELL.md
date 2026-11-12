# Prompt 02 — Studio Shell

Use after the landing page is complete.

```text
Using the AutoLab design corpus, build only the Studio shell.

Follow `patterns/studio-page.md`, `patterns/cabin-viewer.md`, `patterns/configuration-panel.md`, and `rules/responsive.md`.

Create `StudioPage` with:

- A prominent automotive cabin presentation stage.
- A focused configuration panel.
- Step navigation.
- Camera controls.
- A specification summary.
- Responsive layout for desktop 1440 × 900 and mobile 390 × 844.

Desktop:
- Cabin viewer occupies approximately two-thirds of the working area.
- Configuration controls occupy a compact right-side panel.

Mobile:
- Cabin viewer remains dominant.
- Controls are compact, touch-friendly, and accessible.
- Do not reduce the viewer to a tiny decorative image.

Implement:
- `StudioPage`
- `CabinViewer`
- `ConfigurationPanel`
- `CameraControls`
- `SpecificationSummary`
- Step navigation
- Previous / next controls
- Editable selections
- Clear progress indication

The viewer must be a replaceable component with a typed props interface for:
- Material
- Primary colour
- Secondary colour
- Accent thread
- Composition
- Trim
- Ambient illumination
- Active camera

If real 3D assets are unavailable, use a high-quality visual placeholder with meaningful camera-state transitions. Clearly label it as illustrative. Do not fake unrestricted 3D rotation.

Camera options:
- Driver Hero
- Cabin Pair
- Cockpit & Dash
- Stitch Detail

Do not build the full selector logic yet. Focus on shell, layout, viewer boundary, navigation, and specification-summary structure.

Before coding, state:
1. The desktop and mobile layout system.
2. The viewer component contract.
3. The configuration state fields.
4. The camera-state approach.
5. The anti-slop checks you will apply.

Then implement only the Studio shell.
```
