# Technical Findings

## Verified 2020 RX evidence

- The Lexus USA Pressroom page is a primary model-year source for the 2020 RX family and links four high-resolution media images, a product-specification PDF and video assets.
- The 2020 brochure describes the RX 350 as a 3.5-litre V6 model with available all-wheel drive, and describes model-dependent interior options including NuLuxe/leather, wood/aluminium trim, heated/ventilated front seats, ambient LED illumination and touchscreen/Remote Touch equipment.
- The European newsroom describes the 2020 RX as a fourth-generation refresh and calls out the moved-forward central display, trackpad interface, vertical front-seat stitching and matching door-panel quilting. Market/grade differences remain important.

## Implications for the current AutoLab viewer

1. The current front-cabin GLB should be reviewed against official cockpit and console images before geometry changes are proposed.
2. Seat detail should be split into silhouette, panel boundaries, seam/stitch mask and leather microstructure. The reference package supports the latter two as material/shader work, not necessarily added geometry.
3. Console and dashboard should preserve separate material roles because the official imagery shows distinct upper dashboard, trim, screen surround, console and black control surfaces.
4. Door panels and rear seats require more exact-year, exact-grade references before new production geometry is generated.
5. A starlight headliner is an optional custom treatment, not an original 2020 RX factory-equipment reference; use installation references only to design a plausible AutoLab option and clearly label it as custom.

## Model-year controls

- Do not merge RX 350, RX 350L, RX 450h, RX 450hL and F SPORT imagery without recording the variant.
- Do not infer U.S. availability from European-market material.
- Do not infer exact leather colour, seat pattern or trim from an image without grade/market identification.
- Do not infer dimensions from perspective photographs.
