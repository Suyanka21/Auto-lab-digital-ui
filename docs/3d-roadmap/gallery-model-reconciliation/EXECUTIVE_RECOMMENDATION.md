# Executive recommendation

**Verdict:** the gallery is good enough to correct the front cabin, starting with the driver seat. It is not enough on its own for a full cabin within the current budgets.

## Key findings

1. **The gallery is one real car, photographed thoroughly.** All 35 photos show the same silver, two-row, non-F SPORT RX 350 built 02/2020 in Canada (label in Gallery 11). 21 of the 35 photos show interior detail useful for modelling.
2. **The current model has the right parts list for the front, but the wrong seats.** Its seats are sport buckets; the car has comfort seats with separate perforated inserts. The console shows a light flat top instead of wood, a touchpad and a drive-mode knob. The dashboard lacks the large display hood and the silver trim strip.
3. **The large grey block in Driver Hero is the dashboard's end cap.** In the real car it is black and hidden by the closed door.
4. **The model already uses all 24 draw calls.** Doors, floor, roof and rear seats can't be added without merging parts or a measured budget increase.
5. **Three library images are mislabelled.** The "official cockpit, console and front-cabin" pictures (0049, 0051, 0052) are exterior photos. The research's cited door-part number is for a red interior.
6. **Rights for the 35 gallery photos were not recorded** in either rights register at the time of assessment. The owner has since stated them; see below.

## Recommendation

Approve the driver-seat re-zoning experiment in `FIRST_IMPLEMENTATION_EXPERIMENT.md` as the first 3D-1 step, within current budgets, after 3D-0 is accepted.

## Decisions for the owner

1. **Approve the first experiment** (driver seat only, no new draw calls, production GLBs untouched).
2. **Confirm the gallery's origin and rights:** are these AutoLab's own photos of the donor car?
3. **Supply the window sticker or a VIN decode** to settle leather vs NuLuxe, the wood trim name and AWD.
4. **Optional:** two measured seat dimensions (cushion width, backrest height) to check scale.
5. **Fix the library index** in a separate docs PR: relabel 0049, 0051 and 0052 as exterior shots.

## Owner decisions recorded 2026-11-16

These answer the list above. The findings and the recommendation are unchanged.

1. **Experiment approved, gated.** The driver-seat experiment is approved. Work must not start until [PR #3](https://github.com/Suyanka21/Auto-lab-digital-ui/pull/3) (3D-0) is accepted and merged. Scope stays `GEO_Seat_Front_Driver` and `GEO_Seat_Stitching_Front`, with scratch candidate GLBs only. The owner reviews the visual result before any candidate becomes the production baseline.
2. **Gallery rights.** The 35 photos are publicly accessible research photographs collected by a separate research agent, not AutoLab-owned. Photographer, licence and commercial reuse permission are unverified. Approved use is internal visual reference for modelling only. Customer-facing display, marketing use, redistribution and embedding in the commercial showroom are not approved. Recorded in `AUTOLAB_2020_LEXUS_RX350_REFERENCE_LIBRARY/00_GALLERY_ORIGINALS/RIGHTS_AND_USE.md` and both rights registers.
3. **Window sticker or VIN decode:** not supplied. Leather versus NuLuxe, the wood trim name and AWD stay unverified.
4. **Seat dimensions:** not supplied. Seat geometry from the experiment is a visual reconstruction from photographs and is provisional. No dimensional accuracy is claimed.
5. **Library index:** the three exterior images are corrected in a separate docs PR.
6. **Branding boundary.** The 2020 Lexus RX 350 is the vehicle-design reference; the showroom is an AutoLab product, not a Lexus product. No Lexus logos, badges, wordmarks, emblems, branded interface screens or marketing artwork may be introduced or reproduced. The steering-wheel centre stays neutral and unbranded. Gaps are filled with generic, original or appropriately licensed assets only, never with additional Lexus-branded assets.
