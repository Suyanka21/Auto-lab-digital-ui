# Excluded Reference Policy — Showroom Concepts

## Status: EXCLUDED FROM 3D GEOMETRY MODELLING

This folder documents the exclusion policy for AI-generated white showroom concepts and presentation renderings.

### 1. Architectural Guidance for Astra

- **Not Authoritative Geometry:** The bright white showroom environment is an **application presentation requirement** and lighting stage design for the Three.js viewport, **not** a physical asset or vehicle geometry specification to be reconstructed in 3D.
- **Do Not Model as Environment Geometry:** Astra must **not** attempt to model the white floor reflections, cyclorama curved walls, or background ambient haze into the vehicle GLB meshes.
- **Runtime Lighting Role:** Studio lighting, reflections, contact shadows, and stage backdrops are handled dynamically at runtime via Three.js ambient/directional lights, HDR environment maps, and shadow ground planes.
- **Current Pack Status:** Zero white showroom concept images were supplied in the initial 16-asset reference pack. Any future concept renderings showing white showroom staging must be deposited here and kept strictly excluded from geometry and material pipelines.
