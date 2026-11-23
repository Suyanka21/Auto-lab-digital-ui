# Door visual discrepancy review
2026-11-20. R3 is a review candidate, not visual acceptance.

## Evidence and comparison method
Approved front/rear PRIMARY AI images from reference pack commit 0e68d56c8863b5890fdcd580e570a2910edeaf38 are the design authority. These are design images, not measured manufacturing drawings. Original files remain unchanged. The comparison sheet mirrors each reference horizontally to align the installed driver-side handing; it does not change the model or claim a camera/perspective match.

Inspected R2 source, existing R2 renders, and R3 front/rear straight and three-quarter renders. The previous R2 images use different lighting/material preview settings: the R2-versus-R3 sheet documents shape evolution, not a controlled material A/B test. All five new R3 inspection views share the same neutral lighting, exposure and material setup.

| Feature | R2 discrepancy / cause | R3 correction | Remaining mismatch |
|---|---|---|---|
| Silhouette | Extruded polygon shell, abrupt corners and nearly planar face | Rebuilt rounded outline and controlled depth rings; distinct tapered rear shell | Outer perimeter and rear wheel-arch curvature still more generic and blunt than the primary design |
| Upper padding | Thin rail reads as a separate bar | Broad convex upholstered roll, softened face transitions | End caps and highlight falloff still pinch; not a continuous production-quality upholstered edge |
| Release and trim | Flat bright plate with small isolated lever | Recessed fascia/bowl, thin perimeter reveal, separated decorative insert and lever | Bowl is shallow and surround angular; missing small lock/seat-memory markings |
| Leather insert | Flat pentagonal slab with sharp seam boundary | Curved perimeter, bulged face and a low-poly seam path | Still reads too planar in the centre; perimeter seam is a fine welt, not detailed sewn stitches |
| Pull attachment | Detached curved rod laid over a flat armrest | Variable-section swept pull continues into the palmrest, with a shaped support | Upper attachment still appears appended; the reference's clear under-grip opening and stitched joint are not yet matched |
| Armrest | Rectangular shelf with uniform thickness | Wider palm support and curved lower saddle with variable section | Too soft/sausage-like at the end; support volume and abrupt insert edge need further review |
| Storage pocket | Flat applied box/plate | Curved bin face, lip and lowered inner floor; no solid top cap | Opening reads as a narrow slit, particularly straight-on; depth and end returns remain less convincing than the reference |
| Speaker | Vertical bevelled bars and thick cylindrical rim | Thin circular disc/rim; procedural fine grille in the master | Disc still looks applied; master microperforation is not baked into runtime GLB |

## Material assessment
R3 master uses tan grain leather, dark padded leather/plastic, satin aluminium, illustrative walnut and a procedural speaker grille under neutral area lights. These are physically based shader settings, not a claim that appearance matches the primary image. Tan looks too pale under the current lighting, grain and stitching are too weak, and the wood reads too uniform at this distance.

The exported GLBs deliberately reuse the existing ten runtime material names and original KTX2 payloads. They do NOT contain the master's procedural walnut/grille textures. Runtime decorative trim remains existing carbon; door leather follows MAT_Seat_Secondary. Independent door colour is not implemented. Do not substitute these master renders for browser evidence or runtime material acceptance.

## Review verdict
Meaningful shape improvement over R2, but visual discrepancy remains. Door milestone stays OPEN. No pillars, roof, cockpit expansion, production replacement or performance-limit change is authorized by this report.
