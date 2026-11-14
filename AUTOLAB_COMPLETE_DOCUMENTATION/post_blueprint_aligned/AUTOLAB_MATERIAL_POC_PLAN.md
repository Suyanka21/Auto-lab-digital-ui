# AUTOLAB material proof-of-concept plan

**Date:** 2026-11-14  
**POC verdict target:** Decide whether blueprint-compliant generated material assets can reduce onboarding effort without degrading the existing real-time configurator. The supplied blueprint is the controlling specification.

## Hypothesis

A dedicated tileable texture workflow, combined with controlled local PBR processing, can reduce the time needed to create a convincing neutral-leather material swatch. It will not replace the GLB’s geometry, UVs, shader setup or renderer validation.

## Scope

Use one neutral Nappa leather reference as the first test. Do not upload private OEM material. Use either a public/licensed sample or a locally created neutral reference with permission to process it. The authorized target contains four slots: `MAT_Seat_Primary`, `MAT_Seat_Secondary`, `MAT_Console_Carbon` and `MAT_Steering_Leather`. The production GLB was not accessible in this run, so the POC should first use a neutral test plane and then the authorized GLBs only after repository access and asset authorization are confirmed.

The first POC batch must produce blueprint-shaped outputs: `MAT_Seat_Primary` at 2048² preferred/1024² minimum with a 2:1 atlas, 15 mm boundary fade and 3.2 mm pitch/1.0 mm perforations; `MAT_Seat_Secondary` and `MAT_Steering_Leather` at 1024² seamless with 50 mm repeat; and `MAT_Console_Carbon` at 2048² with strict four-way 448 mm seamless repeat. Each slot must contain `base`, `normal` and `orm` master PNGs. Base must be neutral 0.85–0.94 grayscale, normal linear OpenGL +Y, and ORM linear packed AO/roughness/metallic/thread-mask channels. These are requirements from the supplied blueprint.

Test the following candidates:

1. Scenario Texture as the primary dedicated tileable workflow.
2. Polycam, only if a physical swatch and eligible account are available.
3. Stable Image or self-hosted Stable Diffusion as the flexible low-cost comparison.
4. Materialize as the common local tiling/PBR derivation step.
5. One general generator—OpenAI, Gemini, Firefly or FLUX—for a concept-only control. Do not treat it as a reusable-material baseline unless it independently passes all gates.

The official documents support different capability claims, but none of the candidates was practically tested during this research. No candidate may bypass the local repacking and compression stage: compile all three maps with the blueprint’s `toktx` UASTC/Zstandard 9 settings, run `ktx validate`, and record the results in `manifest.json`. [1] [2] [3] [4]

## Standardized input

Prepare one 2048×2048 neutral-leather reference with:

- Flat, diffuse illumination and no strong cast shadow.
- A visible scale marker or known grain pitch, including the 0.3–0.6 mm grain target and 50 mm repeat target.
- A colour target or approved digital colour value.
- One crop showing the grain, one showing edge/variation behaviour, and one showing any seam/stitch context if relevant.
- An input manifest containing ownership, permission, capture device, lighting and colour profile.

Use the same reference, wording, desired output size, aspect ratio and evaluation seed policy for every candidate. Do not buy credits or subscriptions without approval.

## Generation protocol

For each tool, create three independent outputs and one controlled colour variant. Record the exact model/version, prompt, references, seed, dimensions, settings, timestamp, account/plan, output format and credit usage. If a tool cannot expose a seed or version, record that limitation.

The base prompt should describe only the target material and scale. Do not ask for a photographic interior render. For example: “neutral automotive Nappa leather surface, top-down flat material sample, fine irregular 0.3–0.6 mm grain, uniform diffuse illumination, no cast shadow, no object perspective, no border, no logo, neutral grayscale albedo suitable for shader tinting.” Never prompt for fixed brown, red or beige dye in the base asset.

For each candidate, save:

- Original generated image.
- Cleaned base-colour candidate.
- Derived or generated maps.
- Masks and intermediate files.
- 2×2 and 3×3 repeat previews.
- Renderer screenshots.
- Cost and elapsed-time record.

## Acceptance criteria

### A. Seamless tiling

Pass only if the 2×2 and 3×3 repeats show no visible seam under neutral and grazing light. Measure opposite-edge pixel and gradient differences on base colour, normal and roughness. The exact thresholds should be calibrated on a known good conventional texture; as a starting gate, no obvious seam may be visible at 100% and edge difference should be below the project’s conventional-texture baseline.

### B. Material consistency

Three regenerations must preserve the same material family, grain scale and roughness impression. Reject if the tool introduces visible objects, perspective, baked highlights, repeated motifs or large-scale tonal drift.

### C. Colour neutrality

Compare the average colour and local variation with the approved neutral reference under controlled display conditions. Record RGB/Lab values and, if a calibrated target exists, ΔE. A prompt-only claim of “neutral” is not sufficient.

### D. Detail preservation

At the stitch-detail camera distance, confirm that grain remains plausible after resizing and mipmapping. If quilting, perforations or stitches are added in a later test, record pitch, diameter, spacing and continuity rather than scoring only visual attractiveness.

### E. Map compatibility

Verify that every map has documented semantics, bit depth, colour space and tangent convention. Confirm roughness is not an inverted gloss map, normal orientation is correct, height scale is bounded, metallic is physically plausible and AO is not baked incorrectly into base colour.

### F. Real-time suitability

Apply the maps to a test plane and then the authorized GLB. Test all relevant material slots, neutral and at least two colour variants, two-tone masking, all four configured cameras and two lighting conditions. Capture frame time, texture memory and any visible swimming, stretching, seams or baked illumination.

## Suggested scoring

Score each candidate from 0 to 5 for each category: seam quality, consistency, colour, detail, map validity, renderer appearance, repeatability, cost and labour. A score of 0 means unusable; 5 means it meets the conventional-material baseline. A candidate is eligible for production consideration only if it scores at least 4 for seamlessness, map validity and renderer appearance, and does not fail rights/data gates.

## Cost model

Report both **cost per generation** and **cost per accepted asset**. The latter must include failed generations, colour revisions, map processing, manual cleanup, QA and storage.

Published indicative figures from official documentation include:

- Scenario: paid credit plans; Free provides daily compute units but texture generation/API/commercial use require paid access. [1]
- Stability: 25 initial API credits, with listed operations around $0.025–$0.065 each. [2]
- FLUX.1 hosted: approximately $0.04–$0.08 per cited Kontext image; open local commercial use requires the appropriate license. [3]
- Gemini Nano Banana Pro: approximately $0.134 for 1K/2K and $0.24 for 4K API output, with no documented free API tier. [4]
- Materialize: no hosted fee found; Windows-local and free under its documented software license. [5]
- Polycam: entitlement and pricing depend on product tier; the official texture pages conflict on Free access, so do not budget on Free until account verification. [6]

These figures are not savings claims. The POC must record actual approved spend, elapsed person-hours and accepted assets.

## Failure conditions

Stop or reject the candidate if any of the following occurs:

- Private or restricted material is uploaded without written authorization.
- Commercial-use terms are unclear for the intended deployment.
- Output contains an unremovable watermark or provenance requirement incompatible with the product.
- Seam defects remain after one controlled repair pass.
- Maps are merely attractive RGB images without reliable channel semantics.
- Material appearance depends on baked lighting and fails under camera rotation.
- Grain, quilting, perforation or stitch scale is inconsistent with the reference.
- The tool cannot export or retain the required resolution/format.
- Revisions cannot preserve approved regions.
- Total accepted-asset cost or labour exceeds the conventional baseline.

## Decision rule

- **GO for pilot expansion:** at least one workflow beats the conventional baseline on accepted-asset labour or quality, passes commercial/data gates, and produces renderer-validated assets.
- **CONDITIONAL GO:** the workflow reduces reference or variation labour but still depends on conventional texture processing, procedural geometry or manual QA. This is the expected outcome.
- **NO-GO:** generated imagery does not pass tile, map or renderer gates, or conventional photography/procedural authoring is faster and more reliable.

## References

[1]: https://help.scenario.com/articles/4276871610-pricing-plans "Scenario pricing plans"
[2]: https://docs.stability.ai/pricing "Stability API pricing"
[3]: https://docs.bfl.ai/quick_start/pricing "Black Forest Labs pricing"
[4]: https://ai.google.dev/gemini-api/docs/pricing "Google Gemini API pricing"
[5]: https://boundingboxsoftware.com/materialize/ "Materialize capabilities"
[6]: https://learn.poly.cam/hc/en-us/articles/27426153753364-Using-Polycam-s-2D-Texture-Generator "Polycam 2D texture generator"
