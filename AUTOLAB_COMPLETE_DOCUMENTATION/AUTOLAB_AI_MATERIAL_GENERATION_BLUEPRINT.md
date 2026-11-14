# AUTOLAB — AI Material Generation & PBR Ingestion Blueprint
**Target System:** AutoLab Digital Showroom (2020 Lexus RX 350 Luxury Interior)  
**Consumer:** Manus / External Image Generation & 3D Texture Research Agent  
**Authority:** Production Engineering Audit (November 2026)  
**Status:** Authorized Technical Blueprint  

---

## 1. Executive Summary & Objective

This blueprint establishes the exact visual and technical specifications for generating photorealistic, physically based rendering (PBR) texture maps for the AutoLab Digital Showroom using AI-assisted imagery and neural texture synthesis.

### Core Constraint
The AutoLab configurator is a real-time WebGL application running on mobile and desktop browsers via Three.js (r186) and React Three Fiber. The cabin allows dynamic real-time color changes (12 leather hides, 5 thread colors), live finish swaps (carbon, open-pore walnut, poplar, lacquer), and free camera orbit across 4 calibrated presets.

**Any proposed texture enhancement must work within this real-time dynamic tinting architecture. Textures must NEVER bake in fixed leather colors or directional lighting.**

---

## 2. Target Material Zones & Geometry Contracts

The master cabin asset (`interior-l4-classic.glb`, `interior-l4-diamond.glb`, `interior-l4-perforated.glb`) comprises 11 nodes, 66,260 triangles, and 24 draw calls. Enhancements are strictly confined to four specific material slots:

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                         AUTOLAB CABIN MATERIAL ZONES                         │
├─────────────────────────┬───────────────────────┬────────────────────────────┤
│ Material Slot           │ Geometry Node         │ Texture Mapping Scheme     │
├─────────────────────────┼───────────────────────┼────────────────────────────┤
│ MAT_Seat_Primary        │ GEO_Seat_Front_Driver │ Fixed 2:1 Atlas UV (0.80m  │
│                         │ GEO_Seat_Front_Pass.  │ x 0.72m physical bounds)   │
├─────────────────────────┼───────────────────────┼────────────────────────────┤
│ MAT_Seat_Secondary      │ GEO_Seat_Front_Driver │ Discrete Island UVs        │
│                         │ GEO_Seat_Front_Pass.  │ (Bolsters, Headrest)       │
├─────────────────────────┼───────────────────────┼────────────────────────────┤
│ MAT_Console_Carbon      │ GEO_Dashboard_Lexus   │ Triplanar / Planar UVs     │
│ (Wood Veneer / Twill)   │ GEO_Console_Body      │ Seamless Tiling (448mm)    │
│                         │ GEO_Console_Selector  │                            │
├─────────────────────────┼───────────────────────┼────────────────────────────┤
│ MAT_Steering_Leather    │ GEO_SteeringWheel     │ Cylindrical Seam UVs       │
│                         │ _Lexus                │ Seamless Micro-Grain       │
└─────────────────────────┴───────────────────────┴────────────────────────────┘
```

---

## 3. Required PBR Channel Specifications

Every material delivered by Manus must strictly adhere to the following 3-map channel packaging:

### 3.1 Map 1: Neutral Base Albedo (`base`)
* **Role:** Diffuse reflection multiplier.
* **Color Space:** `sRGB` (transcoded to `KHR_texture_basisu` with `srgb` OETF).
* **Format:** 8-bit PNG (source) $\rightarrow$ UASTC / Zstandard level 9 KTX2.
* **Crucial Invariant:** **ABSOLUTELY NO BASE COLOR TINTING.** The texture must be a calibrated neutral greyscale map (albedo values between $0.85$ and $0.94$). AutoLab's WebGL shader multiplies this map by the customer's chosen hex color:
  $$\text{DiffuseColor} = \text{TextureAlbedo} \times \text{UniformColor}_{\text{hex}}$$
  If the base texture contains brown, red, or beige pigment, recoloring to White or Cyan will severely distort.

### 3.2 Map 2: Tangent-Space Normal (`normal`)
* **Role:** Surface micro-relief, pores, flutes, and grain.
* **Color Space:** `Linear` / `Non-Color` (transcoded with `linear` OETF).
* **Format:** 8-bit RGB PNG (source) $\rightarrow$ UASTC KTX2.
* **Convention:** **OpenGL format (+Y Up).**
  * $R = X$ (Left $\rightarrow$ Right)
  * $G = Y$ (Bottom $\rightarrow$ Top, Green channel pointing UPwards)
  * $B = Z$ (Surface Normal pointing outward toward viewer)
* **Depth Calibration:** Leather pore depth must not exceed $0.00025\text{ m}$ ($0.25\text{ mm}$); stitch relief must not exceed $0.00008\text{ m}$ ($0.08\text{ mm}$). Overly deep normals produce harsh black grazing artifacts in WebGL.

### 3.3 Map 3: Packed ORM + Mask (`orm`)
* **Role:** Compact multi-attribute packing for WebGL PBR pipeline.
* **Color Space:** `Linear` / `Non-Color`.
* **Format:** 8-bit RGBA PNG (source) $\rightarrow$ UASTC KTX2.
* **Channel Allocation:**
  * **Channel R (Red):** Ambient Occlusion (AO). Range $[0.60, 1.0]$. Cavities and seams darken; flat surfaces remain $1.0$.
  * **Channel G (Green):** Perceptual Roughness. Leather baseline $0.45 - 0.52$; thread baseline $0.32 - 0.38$; wood veneer $0.23 - 0.50$.
  * **Channel B (Blue):** Metallic. Must be strictly $0.0$ ($0$ in 8-bit) for all leather, thread, and wood surfaces.
  * **Channel A (Alpha):** **Contrast Thread Mask.**
    * Stitched thread pixels: $1.0$ ($255$).
    * All leather/backing pixels: $0.0$ ($0$).
    * Used by Three.js `attachThreadMask` hook to dynamically recolor diamond quilt stitching.

---

## 4. Zone-by-Zone Asset Generation Requirements

### Zone A: Quilted & Perforated Seat Inserts (`MAT_Seat_Primary`)

* **Texture Resolution:** $2048 \times 2048$ (or $1024 \times 1024$ minimum).
* **UV Coordinate Space:**
  ```text
  U = 0.0                      U = 0.5                      U = 1.0
  ┌────────────────────────────┬────────────────────────────┐ V = 1.0
  │                            │                            │
  │       CUSHION INSERT       │      BACKREST INSERT       │
  │                            │                            │
  │   Physical Width: 0.40m    │   Physical Width: 0.40m    │
  │   Physical Height: 0.72m   │   Physical Height: 0.72m   │
  │                            │                            │
  └────────────────────────────┴────────────────────────────┘ V = 0.0
  ```
* **Seam Clearance Rules:**
  All pattern features (diamond fluting, perforation holes) must taper smoothly to zero amplitude within $0.015\text{ m}$ ($15\text{ mm}$) of the panel boundaries to prevent hard seam clipping where the insert meets the bolsters.
* **Perforation Specifications:**
  * Hole pitch: $3.2\text{ mm}$ center-to-center in staggered hexagonal or square grid.
  * Hole aperture: $1.0\text{ mm}$ diameter, with slightly depressed lip.
  * Holes must carry AO darkening ($R \approx 0.40$) and low albedo ($Base \approx 0.20$).

---

### Zone B: Open-Pore Architectural Wood Veneers (`MAT_Console_Carbon`)

* **Texture Resolution:** $2048 \times 2048$ seamless tile.
* **Tiling Metric:** AutoLab uses a calibrated $0.448\text{ m}$ ($44.8\text{ cm}$) tile repeat (`texture.repeat.set(0.1, 0.1)` on $44.8\text{ mm}$ physical UVs).
* **Tiling Requirement:** **Strict 4-way seamless wrap.** Zero visible seams along horizontal or vertical wrap lines.
* **Target Species:**
  1. **Open-Pore Walnut:** Warm, dark linear grain with subtle pores ($0.15\text{ mm}$ deep), satin finish (Roughness $0.48 - 0.52$).
  2. **Open-Pore Poplar Anthracite:** Grey/black fiddleback figure, muted chatoyancy, soft sheen (Roughness $0.42 - 0.46$).
  3. **Piano Lacquer Flowing Lines:** Deep mirror black (Roughness $0.18 - 0.22$, Clearcoat $0.85$) with thin, hairline silver/white parallel metallic pinstripes.

---

### Zone C: Nappa Leather Grain (`MAT_Seat_Secondary` & `MAT_Steering_Leather`)

* **Texture Resolution:** $1024 \times 1024$ seamless micro-tile.
* **Scale:** $0.05\text{ m}$ ($50\text{ mm}$) physical repeat.
* **Characteristics:** Fine, supple semi-aniline pebble grain. Irregular cellular distribution ($0.3 - 0.6\text{ mm}$ cell diameter). Soft transitions, no harsh sharp ridges.

---

## 5. Texture Encoding & Compression Pipeline

All generated textures must pass through the AutoLab KTX-Software processing toolchain before integration. Manus must deliver uncompressed 16-bit or 8-bit master PNGs, which are compiled as follows:

```bash
# 1. Base Albedo (sRGB)
toktx --t2 --encode uastc --uastc_quality 2 --uastc_rdo_l 1.1 --zcmp 9 \
      --genmipmap --assign_oetf srgb --threads 4 \
      texture-base.ktx2 texture-base.png

# 2. Normal Map (Linear, Non-Color)
toktx --t2 --encode uastc --uastc_quality 2 --uastc_rdo_l 1.1 --zcmp 9 \
      --genmipmap --assign_oetf linear --threads 4 \
      texture-normal.ktx2 texture-normal.png

# 3. Packed ORM (Linear, Non-Color)
toktx --t2 --encode uastc --uastc_quality 2 --uastc_rdo_l 1.1 --zcmp 9 \
      --genmipmap --assign_oetf linear --threads 4 \
      texture-orm.ktx2 texture-orm.png

# 4. In-flight Validation
ktx validate texture-base.ktx2
ktx validate texture-normal.ktx2
ktx validate texture-orm.ktx2
```

---

## 6. Machine-Readable Asset Manifest Specification

Manus should output asset deliverables accompanied by a `manifest.json` conforming to this schema:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "batchId": "manus-ai-pbr-v1",
  "generatedDate": "2026-11-14",
  "assets": [
    {
      "slotIdentifier": "MAT_Seat_Primary",
      "treatment": "diamond",
      "resolution": [2048, 2048],
      "uvLayout": "atlas_0.8x0.72m",
      "maps": {
        "base": "diamond-insert-base.png",
        "normal": "diamond-insert-normal.png",
        "orm": "diamond-insert-orm.png"
      },
      "metrics": {
        "averageAlbedo": 0.89,
        "roughnessRange": [0.35, 0.52],
        "normalConvention": "OpenGL_+Y",
        "hasThreadMask": true
      }
    },
    {
      "slotIdentifier": "MAT_Console_Carbon",
      "treatment": "open-pore-walnut",
      "resolution": [2048, 2048],
      "uvLayout": "seamless_tile_448mm",
      "maps": {
        "base": "walnut-base.png",
        "normal": "walnut-normal.png",
        "orm": "walnut-orm.png"
      },
      "metrics": {
        "seamlessTilingVerified": true,
        "averageRoughness": 0.48,
        "normalConvention": "OpenGL_+Y",
        "hasThreadMask": false
      }
    }
  ]
}
```

---

## 7. Acceptance Gate & Rejection Criteria

An asset set delivered by Manus is rejected immediately if any of the following occur:

1. **Banned Pattern: Color Contamination.** The Base Albedo map contains saturated leather dye or baked coloration instead of neutral luminance ($[0.85, 0.94]$).
2. **Banned Pattern: Baked Lighting.** The Albedo or Roughness map includes directional shadows, sun shafts, flash highlights, or room reflections.
3. **Banned Pattern: Inverted Normal Tangents.** Normal map green channel is pointing downward (DirectX format), causing flutes to appear inverted in WebGL.
4. **Banned Pattern: Missing Thread Alpha.** The ORM Alpha channel is opaque ($1.0$) across the entire map, preventing accent thread recoloring.
5. **Banned Pattern: Seam Edge Artifacts.** Tileable wood or carbon maps exhibit hard seam lines or mismatched grain at tile boundaries ($U=0/1$ or $V=0/1$).
6. **Banned Pattern: Budget Violation.** Uncompressed texture payloads exceed $2048 \times 2048$, or transcoded KTX2 VRAM footprint exceeds $16\text{ MB}$ total for the cabin.

