# AutoLab Digital Showroom

Interactive frontend-only prototype for **AutoLab Interior Studio** (Nairobi, Kenya), presenting an editorial showroom landing experience (`LandingPage`) and a two-column cabin configurator (`StudioPage`) structured for straightforward drop-in replacement of the illustrative viewer stage with AutoLab’s real GLB assets and Three.js / React Three Fiber rendering engine.

> **Prototype status:** This repository is a frontend demonstrator prototype, not a production system. It contains no backend, authentication, database, pricing, availability, or order-submission logic.

---

## Running the Prototype

**Prerequisites:** Node.js 18+ (or Bun)

```bash
# Install dependencies
npm install

# Start the development server (port 3000)
npm run dev

# Run TypeScript typechecking
npm run lint

# Create a production static bundle in dist/
npm run build
```

---

## Architecture Overview

- **Centralized typed state (`src/state/ConfigurationContext.tsx`, `src/types/configuration.ts`):** All configuration selections (`material`, `primaryColour`, `secondaryColour`, `accentThread`, `composition`, `trim`, `ambientIllumination`, `activeCamera`) and active step state (`activeStep`) live in `ConfigurationProvider`. State invariants—such as clearing `secondaryColour` in `single-colour` mode and keeping primary/secondary hides distinct in `two-tone` mode—are enforced inside context callbacks.
- **Catalog metadata (`src/data/catalog.ts`):** Single source of truth for option labels, descriptions, swatches, camera definitions, configuration steps, and `confirmed` vs. `illustrative` classifications.
- **Pure presentation components (`src/components/`):** `StudioPage` reads `useConfiguration()` and passes explicit typed values and callbacks to `CabinViewer`, `CameraControls`, `ConfigurationPanel`, the six selector components, and `SpecificationSummary`. Presentation components contain no configuration business logic and zero 3D engine dependencies.
- **Reusable design tokens & primitives (`src/index.css`, `src/components/primitives/`):** Tailwind CSS v4 `@theme` tokens define the Editorial Atelier palette (`ivory` `#F3F0E9`, `paper` `#FAF8F3`, `ink` `#252425`, `graphite` `#101114`, `cyan` `#72C4E1`, `cyan-ink` `#17596D`, `muted-grey` `#65615B`, `fine-border` `#D2CEC5`), typography (`Playfair Display`, `Plus Jakarta Sans`), and motion curve (`--ease-atelier`).

---

## File Map

```text
index.html                              # Document metadata and Google Fonts (Playfair Display, Plus Jakarta Sans)
src/
  index.css                             # Tailwind v4 @theme design tokens, focus-visible contrast, reduced-motion fallback
  main.tsx                              # React entry point
  App.tsx                               # Route controller ('landing' | 'studio') wrapped in ConfigurationProvider
  types/
    configuration.ts                    # Domain IDs, CabinConfiguration, CabinViewerProps, OptionMetadata types
  data/
    catalog.ts                          # Workshop & illustrative option lists, camera presets, step metadata, defaults
  state/
    ConfigurationContext.tsx            # Centralized state provider, step navigation, two-tone hide invariants
  assets/
    images/                             # Local bundled editorial, camera-angle, material, and trim photographs
  components/
    LandingPage.tsx                     # Editorial hero, 4 craft discipline cards, confirmed vs. illustrative scope, walkthrough
    StudioPage.tsx                      # Desktop (2/3 viewer + 1/3 panel) & mobile (step strip + dominant viewer + controls)
    CabinViewer.tsx                     # Replaceable presentation stage accepting CabinViewerProps (illustrative fallback)
    CameraControls.tsx                  # External 4-view camera switcher mounted beneath CabinViewer
    ConfigurationPanel.tsx              # Desktop step tabs, active selector routing, Previous/Continue/Reset footer
    SpecificationSummary.tsx            # Structured specification readout with click-to-edit step links & illustrative labels
    primitives/
      AtelierShell.tsx                  # Sticky header, left mobile drawer (Escape-closable), main frame, footer
      AtelierButton.tsx                 # Primary, secondary, outline-cyan, and ghost button variants (44px+ touch targets)
      AutoLabLogo.tsx                   # Geometric SVG monogram traced from AUTOLAB LOGO .pdf
      EditorialHeading.tsx              # EditorialType typography component with explicit contrast handling
      SectionDivider.tsx                # Hairline section rule with optional centered label
      Surface.tsx                       # Ivory, paper, and graphite surface container primitive
      index.ts                          # Primitive barrel exports
    selectors/
      MaterialSelector.tsx              # Classic · Diamond Quilted · Perforated (distinct texture previews)
      ColourSelector.tsx                # Exclusive Black · Sienna Brown · Light Ivory + two-tone secondary selector
      ThreadSelector.tsx                # Seam stitch colour selector with tactile double-stitch plates
      CompositionSelector.tsx           # Single-colour vs. Two-tone surface zoning diagram and mapping notes
      TrimSelector.tsx                  # Illustrative preview: Carbon Fibre, Poplar Wood, Walnut Wood, Piano Lacquer
      IlluminationSelector.tsx          # Illustrative preview: Cyan, Amber, Rose, Ocean, Champagne perimeter lighting
      index.ts                          # Selector barrel exports
```

---

## Replacing `CabinViewer` with the 3D R3F Stage

`src/components/CabinViewer.tsx` is isolated as a strict presentation boundary. Replace its internals—or swap the component export—without changing `StudioPage`, `CameraControls`, `ConfigurationPanel`, `ConfigurationContext`, or `SpecificationSummary`.

### 1. Preserve the props contract (`src/types/configuration.ts`)

```ts
export interface CabinViewerProps {
  material: MaterialId;                    // 'classic' | 'diamond-quilted' | 'perforated'
  primaryColour: ColourId;                 // 'exclusive-black' | 'sienna-brown' | 'light-ivory'
  secondaryColour?: ColourId;              // Defined only when composition === 'two-tone' (guaranteed != primaryColour)
  accentThread: ThreadId;                  // 'amber-ochre' | 'cyan' | 'warm-ivory' | 'tonal-charcoal'
  composition: CompositionId;              // 'single-colour' | 'two-tone'
  trim?: TrimId;                           // 'carbon-fibre' | 'poplar-wood' | 'walnut-wood' | 'piano-lacquer' (illustrative)
  ambientIllumination?: IlluminationId;    // 'cyan' | 'amber' | 'rose' | 'ocean' | 'champagne' (illustrative)
  activeCamera: CameraId;                  // 'driver-hero' | 'cabin-pair' | 'cockpit-dash' | 'stitch-detail'
}
```

### 2. Preserve container sizing and stage separation

In `StudioPage.tsx`, `<CabinViewer />` sits directly above `<CameraControls />` inside a dark `#101114` (`bg-graphite`) stage wrapper (`lg:col-span-8`). Keep these behaviors in the replacement:

- Maintain the responsive stage box (`relative w-full aspect-[4/3] sm:aspect-[16/9] bg-graphite overflow-hidden`) so the desktop 2/3 stage and mobile dominant viewer proportions remain intact.
- Drive camera rig transitions reactively from `props.activeCamera` (interpolating camera position/target to match `driver-hero`, `cabin-pair`, `cockpit-dash`, and `stitch-detail`) while allowing `CameraControls` to remain external to the canvas.
- Map `material` (normal/roughness/bump maps), `primaryColour` (outer bolsters & console), `secondaryColour` (seat inserts & headrests when `composition === 'two-tone'`, otherwise `primaryColour`), and `accentThread` onto the GLB material slots.
- Continue marking `trim` and `ambientIllumination` as illustrative previews unless AutoLab confirms commercial inclusion.
- Respect `prefers-reduced-motion` when animating camera lerps or post-processing transitions.
