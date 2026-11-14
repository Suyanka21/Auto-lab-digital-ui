# AUTOLAB generative material workflow

**Date:** 2026-11-14  
**Recommendation:** Use generative AI as a controlled source and variation step, not as a replacement for UVs, geometry, PBR authoring or real-time rendering. The supplied Production Engineering Audit blueprint is the governing asset specification.

## Blueprint-controlled output contract

The target is a Three.js r186 / React Three Fiber real-time cabin with dynamic tinting, 12 leather hides, five thread colours, live carbon/wood/lacquer finishes and four calibrated camera presets. Textures must never bake fixed leather colour or directional lighting. These requirements come from the supplied blueprint.

Enhancements are limited to four slots: `MAT_Seat_Primary` (2048² preferred, 1024² minimum, fixed 2:1 atlas over 0.80 m × 0.72 m bounds, 15 mm boundary fade and exact 3.2 mm / 1.0 mm perforations); `MAT_Seat_Secondary` (1024² seamless, 50 mm Nappa micro-tile); `MAT_Console_Carbon` (2048² strict four-way seamless, 448 mm repeat); and `MAT_Steering_Leather` (1024² seamless, 50 mm cylindrical-seam micro-tile). [1]

Each accepted slot requires `base`, `normal` and packed `orm` master PNGs. Base is sRGB neutral grayscale in the 0.85–0.94 range with no baked dye or light. Normal is linear/non-colour OpenGL +Y with pore depth ≤0.25 mm and stitch relief ≤0.08 mm. ORM is linear/non-colour: R=AO, G=roughness, B=0 metallic for leather/thread/wood and A=contrast-thread mask where required. Masters must be transcoded with the blueprint’s UASTC/Zstandard 9 `toktx` commands and checked with `ktx validate`; a manifest must record slot, treatment, resolution, UV layout, map paths and metrics. [1]

## 1. Split the output into two tracks

AutoLab should maintain two separate production tracks:

1. **Reusable configurator material.** This must tile across UVs, survive camera rotation, use valid PBR channels, support controlled colour variants, and render correctly on the existing GLB.
2. **Fixed-camera presentation image.** This can tolerate perspective, lighting baked into the image and non-repeatable detail. General generators are much more useful here.

A successful hero image is not evidence of a successful reusable material.

## 2. Input preparation

Start with one of the following, in descending order of physical reliability:

- A clean, controlled photograph or scan of an approved physical swatch.
- A neutral, front-facing reference image with an accompanying scale reference and colour target.
- A generated concept reference, clearly labelled as synthetic and not physically approved.

Do not upload private OEM or customer assets to third-party services without explicit authorization. Record the source, owner, permission, capture lighting, camera, scale and colour profile in an asset manifest.

For each test swatch, prepare:

- 2048×2048 or higher source for the seat atlas and wood tile; 1024×1024 for secondary/steering leather micro-tiles.
- Neutral diffuse/base-colour reference with highlights and cast shadows minimized.
- A small colour chart or approved digital swatch beside the sample where rights permit.
- A scale marker for grain, perforation diameter, quilting pitch and stitch spacing.
- A mask identifying the material region when using image-to-image or inpainting.

## 3. Generate the base material

For the first pilot, use **Scenario Texture** because it documents top-down tileable generation, reference images, seeds, seam erasure, overlap and feather controls, and a separate map-generation step. Use it first for the 448 mm wood tile and 50 mm leather micro-tile; treat the seat atlas and exact perforation pattern as a procedural/compositing post-process. Use the same reference, prompt, dimensions and seed policy across all candidates. [1]

Use general generators—OpenAI, Gemini, Firefly, FLUX or Stable Diffusion—for concept variants, colourway exploration, or a fixed-camera interior image. Do not route their ordinary raster output directly into the GLB material unless it passes the blueprint’s neutral-base, tile, channel-packing and renderer gates. Their official documentation does not establish native PBR texture sets. [2] [3] [4]

When a real swatch exists, run a parallel **Polycam capture** track. Photogrammetry is a better evidence source for actual surface appearance than hallucinated texture, although lighting, capture quality and processing still require validation. Polycam documents AO/normal outputs for some processing tiers and roughness at Full; this does not prove equivalent output from its AI 2D texture generator. [5]

## 4. Make the base colour usable

Generated images commonly contain lighting, glossy highlights, deep shadows and ambient occlusion. These contaminate a base-colour map. Treat the first raster as a reference or albedo candidate, not as a finished diffuse map.

Apply a controlled cleanup pass:

1. Remove large-scale lighting gradients and cast shadows.
2. Separate material colour from illumination as far as the evidence allows.
3. Preserve real colour variation that belongs to the material.
4. Match the average colour and neutral balance to the approved swatch.
5. Convert the cleaned candidate to neutral grayscale in the 0.85–0.94 albedo range. Preserve colour variants only as shader uniforms, never in the base map.
6. Save both the unmodified generated image and the cleaned neutral-base candidate.

Do not use a generated hero render as a diffuse map merely because it looks realistic under one light.

## 5. Enforce seamlessness

Run an automated 2×2 and 3×3 repeat preview on the base colour and every derived map. Compare opposite edges numerically and inspect the repeat under grazing light. Reject assets with visible seams, periodic tonal bands, motif discontinuity or obvious repeated defects.

Scenario’s overlap, feather and seam controls, and Materialize’s documented seamless-tiling functions, are useful starting points. [1] [6] For tools without a documented tile mode, use a separate offset/repair workflow and label the result as post-processed.

The acceptance test must include:

- Edge colour difference.
- Edge gradient difference.
- Visible seam score in a 3×3 repeat.
- Repeat registration of quilting, perforations and stitches.
- Seam behaviour after mipmapping and texture compression.

## 6. Derive or author PBR maps

Use a local, versioned material-processing step. Materialize can derive height, smoothness, metallic, normal and occlusion maps from imported images and supports seamless tiling, but it is a conventional derivation tool rather than a physically measured material scanner. [6]

Scenario’s Generate Maps workflow can provide height, normal, metallic, edge and AO outputs after albedo generation. Treat them as generated/derived maps and inspect whether they encode the intended material semantics. [1]

For upholstery, the safer map strategy is usually:

- **Base colour:** cleaned and colour-managed material appearance.
- **Roughness:** authored from material knowledge and measured/reference observations, not copied from highlight brightness.
- **Normal:** generated from validated micro-relief or authored procedurally; verify tangent orientation.
- **Height/displacement:** reserved for relief that should affect silhouette or strong grazing-light response. Do not use it for every visible stitch without scale control.
- **AO:** derived cautiously and not multiplied into base colour unless the renderer pipeline explicitly expects it.
- **Metallic:** near-zero for leather, fabric and wood unless the approved material specification says otherwise; carbon fibre trim may still be a non-metallic composite.

Perforation through-holes, seat seams and deep diamond quilting may require geometry or carefully controlled displacement. A normal map alone will not create actual openings or reliable silhouettes.

## 7. UV and GLB integration

The production repository and GLB were not accessible in this run, so the following is the required integration procedure, not completed renderer evidence.

1. Inspect the authoritative GLB material slots, UV channels, texel density, colour space and tangent convention.
2. Identify which slots correspond to seat inserts, bolsters, headrests, console, stitching and trim.
3. Confirm whether the UV islands are tileable and whether different zones share a texture atlas.
4. Fit the material to the UV layout. Do not stretch a square swatch across a non-square or non-uniform island without checking grain direction and scale.
5. Bind base colour, normal, roughness, AO and any height/displacement maps with the renderer’s correct colour-space settings.
6. Keep colour choice as a shader parameter over a neutral base material wherever the physical material allows it. This is the most credible way to support black, sienna brown and light ivory variants from one controlled texture set.
7. Use a separate material or mask for two-tone zones. Do not generate a separate entire seat image for every colour unless the texture itself changes materially.
8. Keep trim and illumination previews labelled illustrative until AutoLab confirms their commercial scope.
9. Test all four camera views named by the experimental UI: driver hero, cabin pair, cockpit dash and stitch detail. [7]

## 8. Render and acceptance validation

Run the accepted candidate through the actual target renderer, not only a 2D preview. Test neutral, black, brown and ivory variants; single-colour and two-tone composition; all applicable cameras; and at least two lighting environments.

A material survives integration only if:

- Grain scale is plausible at stitch-detail distance.
- Highlights move with camera and light instead of remaining baked into the texture.
- Quilting, perforation and stitches remain coherent during rotation.
- Colour variants are consistent and do not expose baked lighting.
- Mipmaps and compressed textures do not destroy the micro-detail.
- The map set does not create seams, inverted normals or implausible roughness.
- Performance remains within the configurator’s texture-memory and frame-time budget.

## 9. Asset manifest and change control

Every accepted asset should ship with a manifest containing:

- Source image/scan and rights status.
- Tool, model and version.
- Prompt, negative prompt, reference identifiers and seed.
- Output dimensions, file formats, colour profile and bit depth.
- Post-processing tool versions and parameter files.
- UV target, material-slot target and texel density.
- Map semantics and tangent convention.
- Repeatability results and renderer screenshots.
- Provenance metadata, Content Credentials/C2PA/SynthID status where applicable.
- Commercial-use decision and any attribution or watermark obligations.

## 10. What should remain conventional

Do not use generative imagery as a substitute for seat geometry, UV mapping, shader authoring, procedural quilting, true perforation geometry, stitching paths, colour management or real-time performance testing. Where a real swatch, procedural pattern or conventional scan gives better control, use it. The commercial opportunity is in reducing reference and variation work, not in removing the material pipeline.

## References

[1]: https://help.scenario.com/articles/3312894507-scenario-texture-the-essentials "Scenario Texture workflow"
[2]: https://developers.openai.com/api/docs/guides/image-generation "OpenAI image generation and editing"
[3]: https://ai.google.dev/gemini-api/docs/image-generation "Gemini image generation"
[4]: https://docs.bfl.ai/flux_1_fill "FLUX Fill masking"
[5]: https://learn.poly.cam/hc/en-us/articles/30299027821716-What-Are-the-Different-Photogrammetry-Processing-Types "Polycam photogrammetry processing types"
[6]: https://boundingboxsoftware.com/materialize/ "Materialize capabilities"
[7]: https://github.com/Suyanka21/Auto-lab-digital-ui "AutoLab experimental UI repository"
