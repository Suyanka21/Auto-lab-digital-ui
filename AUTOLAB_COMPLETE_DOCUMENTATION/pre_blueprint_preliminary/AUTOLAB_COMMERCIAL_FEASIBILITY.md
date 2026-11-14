# Preliminary pre-blueprint version

> This is the preliminary deliverable produced before the authorized AI material blueprint was supplied.

# AUTOLAB commercial feasibility

**Date:** 2026-11-14  
**Verdict:** **CONDITIONAL GO**

## Bottom line

Generative AI is commercially promising for AutoLab as a reference, variation and fixed-camera visualization accelerator. It is not demonstrated as a drop-in replacement for material authoring. The most credible production architecture is a hybrid: use a dedicated tileable-texture workflow or a real captured swatch for the base appearance, process and validate PBR maps locally, and use general image generators only for concepts, colourway exploration and marketing imagery.

This is a **CONDITIONAL GO**, not a claim of completed integration or measured savings. No candidate was practically tested, the Antigravity blueprint was unavailable, and the authoritative production repository/GLB could not be inspected because GitHub requested authentication.

## What could reduce cost and time

### Likely savings

The strongest plausible savings are upstream:

- Faster exploration of leather, quilt, perforation, stitch, wood and carbon-fibre directions.
- More rapid creation of colourway moodboards and fixed-camera presentations.
- Fewer manual iterations before an approved design direction exists.
- A reusable manifest-driven workflow for generating controlled material candidates.
- Lower dependence on bespoke photography for early-stage concept work.

Scenario is the strongest first candidate for reusable swatch exploration because it documents top-down tileable generation, seam controls, reference images, seeds and a separate map-generation step. Materialize is a useful no-cost local support tool for seamless tiling and derived maps. Polycam is attractive when an approved physical swatch exists because capture can preserve real material evidence better than freeform synthesis. [1] [2] [3]


### Savings not demonstrated

No time-and-motion study was run. Therefore AutoLab should not claim that generative AI:

- Replaces an artist or material technical director.
- Eliminates UV work or shader work.
- Produces an accepted GLB material automatically.
- Reduces the time to onboard a complete vehicle.
- Improves real-time appearance under camera rotation.
- Produces manufacturing-accurate quilting, perforations or stitching.
- Produces native production-ready PBR maps from one prompt.

The only responsible commercial claim at this stage is that the technique may reduce early visual exploration and variation labour, subject to a renderer-validated POC.

## Economics

Free access is fragmented and often unsuitable for production:

- Gemini Nano Banana Pro has no documented free API tier; the cited paid API price is approximately $0.134 per 1K/2K output or $0.24 per 4K output, before other charges. [4]
- OpenAI offers rate-limited ChatGPT Free image creation, but this is not a free image API. The API is usage-priced and requires separate developer access. [5]
- Firefly has limited free web generations, while API credentials and entitlements are separate. [6]
- FLUX hosted generation is pay-as-you-go; open weights have different commercial licensing requirements. [7]
- Stability lists 25 initial API credits and low per-operation prices, but commercial use and license conditions still apply. [8]
- Scenario provides daily Free compute units, but texture generation/API/commercial use require paid access. [1]
- Materialize is free and local but Windows-only and not an AI generator. [2]
- Polycam’s official pages conflict on Free access to its 2D texture generator, and its API is Enterprise plus add-on. [3]

The relevant economic metric is not cost per generated image. It is:

`cost per accepted, renderer-validated material asset = generation + retries + map processing + manual cleanup + QA + storage + integration labour`.

A higher-cost generator may be cheaper overall if it reduces failed iterations. Conversely, a free generator can be expensive if it requires extensive seam repair, colour correction and manual map authoring.

## Commercial risks

### Rights and confidentiality

Terms differ between web access, APIs, open weights and paid plans. Some services may use unpaid-service prompts and outputs to improve products. Some hosted services attach C2PA, Content Credentials or SynthID provenance. Open-weight licensing can be non-commercial by default. AutoLab must approve the data route before uploading customer, OEM or unreleased vehicle assets.

### Quality and repeatability

A beautiful image does not prove a valid material. The critical failure modes are baked highlights, incorrect roughness, non-seamless edges, inconsistent grain scale, drifting colour variants and details that disappear or swim during camera rotation. General generators do not document guarantees for these requirements.

### Integration risk

The experimental UI expects a real GLB viewer with material, colour, thread and camera state. Its documented viewer boundary calls for normal/roughness/bump mapping and reactive camera rigs. [9] Without inspection of the authoritative GLB, AutoLab cannot yet know whether generated textures will fit its UV islands, material slots, texel density or tangent basis.

### Scope creep

The technique can easily become a second visual system that improves screenshots but not the actual configurator. The project should only expand after a neutral-leather asset passes the repeat, map and renderer gates.

## Recommended operating model

1. **Design stage:** use OpenAI, Gemini, Firefly or FLUX for moodboards, material directions and fixed-camera presentations.
2. **Material stage:** use Scenario Texture or a controlled scan as the base appearance source.
3. **Processing stage:** use local tools for cleanup, seamless validation, PBR derivation and colour management.
4. **Geometry stage:** retain conventional modeling/procedural methods for quilting, perforation openings, stitch relief and any camera-visible silhouette detail.
5. **Integration stage:** bind maps to the authorized GLB, expose shader tint parameters for neutral materials, and test all cameras and lighting.
6. **Governance stage:** store prompts, seeds, model versions, references, maps, rights decisions and renderer screenshots in an asset manifest.

## Go/no-go gates

Proceed beyond pilot only if the workflow:

- Beats or matches the conventional baseline on accepted-asset labour.
- Passes automated 2×2/3×3 seam tests.
- Produces semantically valid maps with documented colour space and tangent convention.
- Supports the required neutral, black, brown and ivory variants without baked illumination.
- Preserves appearance under camera rotation and the target lighting range.
- Meets the configurator’s memory and frame-time budget.
- Has clear commercial rights, data-handling terms and provenance treatment.
- Does not require uploading restricted assets without authorization.

If ordinary photography, a real swatch scan, procedural textures or conventional material processing beats the generated workflow on these gates, choose the conventional method. That outcome would still be a successful technical finding.

## Final recommendation

**CONDITIONAL GO.** Run the neutral-leather POC with Scenario Texture plus controlled local processing, with Polycam photogrammetry as the physical-swatch comparator and Materialize as a free local support tool. Keep a general image generator in the experiment only as a fixed-camera/concept control. Do not claim production integration, cost savings or native PBR generation until the authorized Lexus RX 350 GLB is tested in the actual renderer.

## References

[1]: https://help.scenario.com/articles/4276871610-pricing-plans "Scenario pricing plans"
[2]: https://boundingboxsoftware.com/materialize/ "Materialize official capabilities"
[3]: https://poly.cam/tools/material-generator "Polycam AI material generator"
[4]: https://ai.google.dev/gemini-api/docs/pricing "Google Gemini API pricing"
[5]: https://developers.openai.com/api/docs/guides/image-generation "OpenAI image generation and editing"
[6]: https://developer.adobe.com/firefly-services/docs/firefly-api/ "Adobe Firefly API"
[7]: https://docs.bfl.ai/quick_start/pricing "Black Forest Labs pricing"
[8]: https://docs.stability.ai/pricing "Stability API pricing"
[9]: https://github.com/Suyanka21/Auto-lab-digital-ui "AutoLab experimental UI repository"
