# Preliminary pre-blueprint version

> This is the preliminary deliverable produced before the authorized AI material blueprint was supplied.

# AUTOLAB image-tool capability matrix

**Date:** 2026-11-14  
**Author:** Manus AI  
**Status:** Preliminary but decision-ready; all practical generation tests are marked **NOT TESTED**.

## Scope and repository findings

The requested Antigravity document, `AUTOLAB_AI_MATERIAL_GENERATION_BLUEPRINT.md`, was not available in the accessible repository material. The production repository could not be read from this environment because GitHub requested authentication. No production GLB, UV layout, material-slot map, or renderer evidence was therefore inspected. The public experimental repository was readable and confirms the future UI expects three material families—classic, diamond-quilted, and perforated—plus colour variants, two-tone composition, accent thread, trim, and camera views. Its replacement contract explicitly calls for mapping material normal/roughness/bump maps and colours onto GLB material slots. [1]

The matrix below therefore treats texture-generation conclusions as provisional until tested against the authoritative production GLB.

## Decision matrix

| Candidate | Best role for AUTOLAB | Free access versus production access | Reference/edit/mask support | Texture/PBR suitability | Commercial and provenance notes | Verdict |
|---|---|---|---|---|---|---|
| **Scenario Texture** | Reusable, tileable material exploration | Free plan: 50 daily compute units, but texture generation, API access, and commercial use require paid access. Paid plans are credit-based; published plans include Starter $15/month, Pro $45/month, and Max $75/month. [2] | Reference images, image-to-image, structure/ControlNet, seeds, variations, seam erase, overlap and feather controls | Strongest documented fit for the 448 mm wood tile and 50 mm leather tile. Its separate map step can produce height, normal, metallic, edge and AO, but it does not document neutral 0.85–0.94 albedo, OpenGL +Y, packed thread alpha, 15 mm atlas fade or exact 3.2 mm perforation geometry. Post-processing is mandatory. [2] | Paid outputs are commercially usable under the terms. Free outputs are personal/evaluation only. Enterprise offers stronger data controls; ordinary service data may be used to operate and improve the service. [2] | **Best first pilot for reusable swatches** |
| **Polycam material generator / photogrammetry** | Real-swatch capture, and a secondary AI texture option | Free scan access exists, but exports are limited and watermarked. Texture-generator entitlement is inconsistent across official pages; API is Enterprise plus add-on. Basic is published at $30/month or $150/year. [3] | AI texture generator accepts prompts, reference images, image-guidance strength and negative prompts. Photogrammetry captures provide a physical-source route. | AI generator claims up to four seamless, tileable textures up to 2048 px, but blueprint-required packed ORM alpha, neutral albedo range, OpenGL +Y and exact atlas/physical scales are not documented. Photogrammetry maps still need repacking and calibration. [3] | AI texture page claims royalty-free commercial use; scanned models have separate terms and public-display attribution requirements. Resolve the product distinction contractually. | **Best when a physical swatch exists; gated pilot** |
| **Materialize** | Local tiling and map derivation | Free standalone Windows application; no hosted API or quota was found. Windows-only. [4] | No AI reference conditioning or semantic masking documented. It accepts source images/imported maps and has XML clipboard automation. | Useful for seamless tiling and derived maps, but it does not natively guarantee the blueprint’s packed ORM layout, thread-mask alpha, OpenGL +Y orientation, roughness ranges or KTX2 output. It can support the preprocessing stage only. [4] | GPLv3 software; review obligations if modified/distributed. User texture content is a separate rights question. No cloud upload path was identified. | **Best free supporting utility, not a generator** |
| **Stable Diffusion / Stable Image** | Flexible low-cost or self-hosted experimentation | Hosted API gives 25 initial credits; listed operations are roughly $0.025–$0.065 each depending on endpoint. SD 3.5 open weights are available under the Community License, subject to its conditions. [5] | Text/image-to-image, inpaint, structure, style controls, search-and-recolor, alpha/black-white masks; a tile-texture style preset is documented. | Useful control surface, but seamlessness is not guaranteed by the tile preset. No native PBR channel set is documented; local engineering is required. | C2PA metadata is documented for API outputs. Community License has attribution and revenue thresholds; review before commercial deployment. [5] | **Best engineering-owned fallback** |
| **FLUX hosted/open** | Concept variants and masked edits | Hosted Playground/API is pay-as-you-go, not a documented unlimited free tier. FLUX.1 Kontext examples are roughly $0.04–$0.08/image; open local weights have non-commercial defaults unless commercially licensed. [6] | Reference-image editing; FLUX Fill supports explicit masks. | Strong visual editing, but no documented seamless-texture guarantee or native PBR output. | Hosted outputs carry BFL C2PA credentials; open local outputs do not receive that BFL signing guarantee. Licensing differs sharply between hosted and open routes. [6] | **Good concept/mask option, secondary material route** |
| **Adobe Firefly** | Brand-safe concept imagery and masked edits | Free web plan has limited daily generations. API requires Adobe credentials and entitlement; published web plans include credit subscriptions. API per-image cost was not clearly published in the reviewed official pages. [7] | Style and structure references, image-to-image instruct edit, grayscale masks, Generative Fill, custom models. | Strong image editing, but seamless tiling, UV-aware output and native PBR maps are not documented. | Adobe states non-beta outputs can be used commercially and applies Content Credentials to certain exports. Country and entitlement restrictions apply. [7] | **Strong fixed-camera/brand workflow, not core material pipeline** |
| **OpenAI image generation/editing** | Fixed-camera imagery, moodboards, colourway exploration | ChatGPT Images is available on Free with changing rate limits; that is not free API access. Current documented GPT Image API pricing is token-based, including $8/M image-input tokens and $30/M image-output tokens for the cited current image models. [8] | Reference images, multi-turn edits, alpha masks, transparent backgrounds, compositing guidance. | No native seamless-texture or PBR guarantee. Repeated edits can drift; pixel-locked areas should be composited from the approved source. | Services terms assign output rights to the customer to the extent permitted by law, but outputs may not be unique. API data controls and C2PA/SynthID provenance need review. [8] | **Useful visual ideation tool, not material authoring** |
| **Gemini 3 Pro Image / Nano Banana Pro** | High-fidelity product concepts and visual colour/material variants | No documented free API tier for Nano Banana Pro. Paid API pricing is approximately $0.134 per 1K/2K image and $0.24 per 4K image, excluding input/text charges; consumer access depends on plan, account and region. [9] | Up to six object, five character and three style references for the cited Pro workflow; semantic conversational editing. Pixel masks are not documented. | No native seamless or PBR output documented. PNG/JPEG images are documented; no material-map/UV export is documented. | Generated images include SynthID. Google terms say Google does not claim ownership, but outputs may be similar for others and unpaid-service data handling differs from paid services. [9] | **Useful concept/variant tool, not core material authoring** |

## Capability conclusions by material requirement

### Neutral leather and colour variants
All general generators can plausibly depict neutral leather and produce colour variants, but none of the reviewed official documentation guarantees grain scale, calibrated colour, reflectance, or repeatability. Scenario has the strongest documented path because the workflow is explicitly top-down and tileable. A real swatch captured under controlled illumination is preferable when colour and grain are commercially important.

### Seamless tiling
Seamless output is explicitly productized by Scenario and claimed by Polycam. Materialize provides local seam/tiling support. Stable Image documents a tile-texture preset but not mathematical edge continuity. For Gemini, OpenAI, Firefly and FLUX, seamlessness is not documented and must be treated as unverified until an automated 2x2/3x3 repeat test passes.

### Quilting, perforations and stitching
General generators are useful for visual direction, but generated quilting, perforations and stitches should be treated as 2D appearance references unless geometry and relief are independently authored. The reviewed tools do not guarantee manufacturable diamond pitch, hole diameter/spacing, stitch gauge, or repeat registration. For the configurator, a hybrid approach is safer: model or procedurally generate the macro pattern, then use generated imagery only to inform micro-variation.

### Wood and carbon fibre
General image generators are reasonable for design exploration. They do not establish weave direction, anisotropy, grain scale or calibrated reflectance. For carbon fibre in particular, procedural or photographed weave references are likely more reproducible than freeform generation.

### PBR maps
No reviewed general image-generation API documents a native production-ready set of base colour, roughness, metallic, normal, height/displacement and AO maps. Scenario documents an albedo-then-map workflow; Materialize derives maps locally; Polycam documents PBR channels for photogrammetry processing rather than clearly for its AI texture generator. Any accepted asset must pass channel-semantics, bit-depth, colour-space, tangent-convention and renderer tests.

## Provenance and evidence status

No candidate was practically tested. The following remain **NOT TESTED**: actual leather grain quality, edge continuity, diamond-quilt regularity, perforation spacing, stitch continuity, colour error against a swatch, cross-generation consistency, output metadata after export, and appearance in AutoLab’s renderer. Costs and plan details are dated 2026-11-14 findings and can change.

## References

[1]: https://github.com/Suyanka21/Auto-lab-digital-ui "AutoLab experimental UI repository"
[2]: https://help.scenario.com/articles/3312894507-scenario-texture-the-essentials "Scenario Texture: essentials"
[3]: https://poly.cam/tools/material-generator "Polycam AI material generator"
[4]: https://boundingboxsoftware.com/materialize/ "Materialize official capabilities"
[5]: https://docs.stability.ai/pricing "Stability API pricing and credits"
[6]: https://docs.bfl.ai/quick_start/pricing "Black Forest Labs pricing"
[7]: https://developer.adobe.com/firefly-services/docs/firefly-api/ "Adobe Firefly API"
[8]: https://developers.openai.com/api/docs/guides/image-generation "OpenAI image generation and editing"
[9]: https://ai.google.dev/gemini-api/docs/pricing "Google Gemini API pricing"
