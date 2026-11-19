# AUTOLAB — Approved 3D Interior Reference Pack

## 1. Executive Purpose & Scope

This reference library contains the curated and approved AI-generated design references created for **Astra**, the 3D modelling and technical asset agent for **AutoLab Digital Showroom**.

The mission of this library is to guide the creation of a visually realistic, coherent, generic premium mid-size SUV cabin for AutoLab's interactive customisation configurator.

### Core Modelling Directives for Astra

- **Generic Premium SUV (RX-Inspired):** While visually inspired by the fourth-generation (2020) Lexus RX 350 AWD donor cabin, **manufacturer-accurate reconstruction is not required**.
- **Realism & Usability Over Precision CAD:** Visual realism, surface cleanliness, coherent topology, and smooth configurator interaction take precedence over millimeter-exact factory measurements.
- **Modelling References Only:** These images are visual and geometric concept references. They are **not** ready-made texture maps, PBR materials, UV charts, or 3D geometry assets.
- **Separation from Factory Research Photography:** This collection is strictly isolated from the 35-photo factory research gallery and technical documents located in `AUTOLAB_2020_LEXUS_RX350_REFERENCE_LIBRARY/`. Do not conflate AI design targets with OEM press photos.
- **No Trademark Reproduction:** Do not model brand logos, badges, steering wheel emblems, or proprietary infotainment interface graphics. Keep all badges neutral and original.

---

## 2. Evidence Hierarchy & Roles

To eliminate guesswork during 3D asset creation, every asset in this pack is categorized into a strict hierarchy:

| Role | Meaning & Usage Rule for Astra |
|---|---|
| **PRIMARY** | **The Authoritative Design Target.** Exactly one primary image exists per component zone. Astra must follow the primary image for the intended form factor, silhouette, split lines, seam boundaries, and material zoning. |
| **SECONDARY** | **Structural / Overall Context.** Provides overall spatial orientation, alignment, or complementary angles (e.g. rear-facing perspective, ceiling layout). Subordinate to the primary component view. |
| **ALTERNATES** | **Supplementary Context Only.** Alternative camera angles, lighting conditions, or subtle variations. Useful for cross-checking edge depth, side profiles, and hidden surfaces. **Must never override the Primary reference.** |
| **EXCLUDED** | **Not Authoritative for Geometry.** White showroom environment concepts and marketing renderings. Must **never** be used as geometry specifications. |

---

## 3. Critical Component Guidelines

### 3.1 Structural Cabin Shell vs. Finished Cabin Interior
- Images in `06_CABIN_SHELL/` (`AUTOLAB_SUV_CABIN_SHELL_3Q_CUTAWAY_01.jpg` and `AUTOLAB_SUV_CABIN_SHELL_REAR_FORWARD_02.jpg`) depict a stripped body-in-white/cutaway cabin structure with exposed sheet metal, raw door inner panels, and naked cross-car beams.
- **CRITICAL DIRECTIVE:** Astra must **NOT** reproduce exposed metal, raw stampings, structural holes, or dismantled parts in the finished customer-facing cabin.
- The cabin shell references exist exclusively to provide spatial proportion, pillar trajectory (A/B/C/D pillars), tunnel elevation, floorpan drop, window cutouts, and component clearance envelopes.

### 3.2 Starlight Headliner Implementation
- References in `07_STARLIGHT_HEADLINER/` depict an aftermarket luxury optical-fibre starlight ceiling embedded in dark Alcantara/suede upholstery.
- **CONFIGURATOR INTEGRATION REQUIREMENT:** Astra and the graphics pipeline must model the starlight system as an **independently controllable configurator feature** (e.g. an `InstancedMesh` or vertex-twinkling `Points` system with adjustable intensity and on/off state in night/dark studio presets), **not** a permanently emissive or baked-in glowing texture.

### 3.3 Dashboard and Centre Console Finishing
- The primary reference `05_DASHBOARD_AND_CONSOLE/PRIMARY/AUTOLAB_SUV_DASHBOARD_CONSOLE_PRIMARY_01.jpg` provides the target geometry for the display shroud, tiered passenger fascia, HVAC vents, analogue clock pod, gear selector console, cup holders, and split center armrest.
- Retain the configurator material slot contracts (`MAT_Console_Carbon`, `MAT_Dashboard_Trim`, `MAT_Cockpit_Black`, and `MAT_Cockpit_Accent`). Ensure trim faces are cleanly partitioned so customer finish swaps function seamlessly.

### 3.4 Door Panels & Switchgear
- **Front Door Panels (`01_FRONT_DOOR_PANELS/`):** The primary reference features a straight-on isolated panel with the driver-side quad-window switch pod, door lock toggles, speaker grille, grab handle, and upper accent insert.
- **Rear Door Panels (`02_REAR_DOOR_PANELS/`):** The primary reference features an isolated panel with a single passenger window switch and the characteristic lower-rear wheel-arch cutout contour.

### 3.5 Seating Architecture
- **Front Seats (`03_FRONT_SEATS/`):** Contoured bolster breaks, ergonomic vertical fluting/channels, perforated center inserts, and a realistic lower plastic valence housing seat adjustment controls.
- **Rear Bench (`04_REAR_BENCH/`):** 60/40 split bench with 3 headrests, fold-down center armrest with integrated cup holder / storage section, and floor anchor bracket geometry.

---

## 4. Directory Structure

```text
AUTOLAB_INTERIOR_3D_REFERENCE_PACK/
├── README.md                                    # This guide
├── REFERENCE_MANIFEST.md                         # Detailed component-by-component manifest
├── 00_MASTER_CABIN/
│   ├── PRIMARY/                                 # 3Q perspective view of assembled cabin
│   └── SECONDARY/                               # Symmetrical rear-facing forward cabin view
├── 01_FRONT_DOOR_PANELS/
│   ├── PRIMARY/                                 # Straight-on isolated panel (quad switch cluster)
│   └── ALTERNATES/                              # Perspective 3Q angle of front door panel
├── 02_REAR_DOOR_PANELS/
│   ├── PRIMARY/                                 # Straight-on isolated panel (single window switch)
│   └── ALTERNATES/                              # Perspective variation of rear door panel
├── 03_FRONT_SEATS/
│   ├── PRIMARY/                                 # 3Q isolated seat (retracted headrest posts)
│   └── ALTERNATES/                              # 3Q isolated seat (extended headrest posts)
├── 04_REAR_BENCH/
│   ├── PRIMARY/                                 # Isolated 60/40 bench (flush headrests)
│   └── ALTERNATES/                              # Isolated bench (raised headrests & ISOFIX tabs)
├── 05_DASHBOARD_AND_CONSOLE/
│   ├── PRIMARY/                                 # Connected dash & console assembly (eye-level 3Q)
│   └── ALTERNATES/                              # Connected dash & console assembly (high 3Q angle)
├── 06_CABIN_SHELL/
│   ├── PRIMARY/                                 # 3Q cutaway structural shell & floorpan
│   └── SECONDARY/                               # Rear-forward stripped cabin structural view
├── 07_STARLIGHT_HEADLINER/
│   ├── PRIMARY/                                 # Full cabin forward view showing starlight canopy
│   └── SECONDARY/                               # Upward-facing detail view of starlight array
└── 99_EXCLUDED/
    └── SHOWROOM_CONCEPTS/                       # Policy on bright white showroom concept renders
```

---

## 5. Verification & Review Status

- **Total Images Organised:** 16
- **Primary References:** 8 (exactly 1 per component zone)
- **Secondary References:** 3
- **Alternate References:** 5
- **Ambiguous / Needs Review:** 0
- **Excluded Showroom Assets:** 0 supplied (policy and directives documented)

For individual image dimensions, file sizes, checksums, and modelling limitations, refer to [REFERENCE_MANIFEST.md](file:///c:/Users/user/OneDrive/Desktop/Auto-lab-digital-ui/AUTOLAB_INTERIOR_3D_REFERENCE_PACK/REFERENCE_MANIFEST.md).
