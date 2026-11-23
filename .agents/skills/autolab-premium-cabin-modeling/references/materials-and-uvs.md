# Materials and UVs

Develop a small material lab using the same colour management as the component. Use large soft lights and a useful environment gradient; adjust only with a recorded reason. Tone, roughness and normal detail work together. Never call a uniform base colour a completed leather material.

## R4 techniques to adapt, not universal presets

- Leather combines UV-driven noise and Voronoi edge grain, very small bump, subtle tone/roughness variation and restrained sheen. Local shape compression carries padding tension. In the refined example roughness varied roughly 0.46–0.57; this is a worked setting, not a specification for every leather. R4 still looked too uniform in broad areas despite visible grain.
- Walnut uses directional UV scaling, low-frequency warp and dark colour variation with restrained coat. R4's darker revision improved its tone but remained too regular. More noise alone is not convincing wood figuring; inspect grain direction at boundaries and in oblique light.
- Plastic uses restrained microtexture and broader roughness. Do not let structural plastic inherit leather padding or metal reflections.
- Satin metal uses a metallic response with sufficient roughness and actual edge thickness. A bright trim line can still look wrong if its corner geometry is pinched.
- The speaker master uses staggered circular alpha holes above acoustic backing rather than thousands of hole meshes. R4's provisional 2.4 mm pitch was a sampling choice, not OEM evidence. Inspect at overview and native close-up size: fine patterns can alias or be erased by denoising.

R4's shader graphs are editable Blender implementations. They are not export-ready PBR maps or validated material definitions for the live model.

## UV and texture discipline

Use surface coordinates that respect the component: path length around a grip; continuous panel coordinates for padded inserts; purposeful projection for flat trim. Keep predictable physical scale across adjacent pieces. The R4 `Surface_Metres` layer is a useful authoring convention, not a claim of distortion-free unwrap.

Check checker distortion and seam placement before baking. Curved sidewalls and inner cavities need deliberate islands; a global planar projection can collapse them. Finite UV data passes the included audit but says nothing about overlap, stretch, density or tangent correctness.

For a runtime derivative, create suitable UV0 islands/padding, bake in linear data space for normal/roughness/metal/AO maps and sRGB for base colour. Verify tangent basis, normal orientation and every mip level. Preserve the existing Diamond ORM alpha thread-mask contract until an explicitly tested replacement is approved. Material previews must not silently recolour a fixed upper dashboard or rename shared trim slots.
