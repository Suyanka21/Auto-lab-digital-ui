# R5-C-refined · one finish correction

**Owner visual review pending.** Start with the fixed-camera comparison, then open the native three-quarter render at whole-seat scale. R5-C and the refinement use the same studio lighting, AgX settings, lens, samples and image filter.

## What I see

- The headrest and outboard bolster have a deeper brown-gold tone. The pale pink cast is reduced in the same lit areas. The lighter centre tone still distinguishes the inserts. The approved primary has different lighting and its colour is a visual target.
- The upper insert, lumbar and cushion front resolve as perforated surfaces from the three-quarter camera. The outer bolsters read as plain leather beside them. The shader keeps the same staggered 4 mm pitch, widens the dark core by 0.48 mm, and gives the fibre inside the impression a diffuse response. At the smaller comparison-sheet size, the dots partly merge into a fine texture, especially on the sloping cushion top.
- The macro shows all four lumbar recesses. Their shadow falls beside narrow padded lands. Two tonal thread rows follow the yoke joint and a single row follows each draw line. On the far side at whole-seat scale the individual rows still merge with the channel shadow.
- A softer highlight now rolls over the cushion crest. The primary's front roll has a more pronounced change of direction. The headrest top tapers slightly more than R5-C, although its flat front face and straight sides remain visible. The rails, guide posts, seat height and mounting datum match the approved geometry.
- In the 125 mm-wide leather macro the bolster grain breaks up the highlight and the two tonal stitch rows are individually visible. At this magnification the punch floors look darker and more uniform than in the primary. In the full-seat plain control the insert pattern disappears while the yoke joint and lumbar padding remain visible.

## Normal-distance perforation check

The table measures fine-pattern contrast in the same three 40 × 40 pixel patches of the 1536-pixel whole-seat renders. Values are the RMS difference between display luminance (Pillow L, 0–255) and a 1.5-pixel Gaussian blur. Patch centres are measured from the top left. These values describe the review images.

| Patch centre | R5-C | Refined | Refined, plain |
|---|---:|---:|---:|
| Yoke (947, 480) | 4.1 | 12.9 | 0.5 |
| Lumbar (836, 762) | 3.7 | 12.3 | 0.6 |
| Cushion (474, 1120) | 3.8 | 14.7 | 0.7 |

## Construction check

The fresh-open comparison found all 14 panel meshes and original cut edges intact. All three insert controls switch independently. At draw values 0, 0.5 and 1, the lumbar foundation and fitted thread followed their expected positions and thickness. A second build reproduced the same evaluated geometry digest. The master audit passed. The approximately 66 mm mounting-floor difference remains open for cabin assembly.
