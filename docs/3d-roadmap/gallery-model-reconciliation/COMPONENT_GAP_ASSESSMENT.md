# Component gap assessment

Status: assessment only. Ranks the gaps in `MODEL_TO_PHOTO_RECONCILIATION.md` for the next implementation phase.

## Scoring

Each component is scored 1 (low) to 3 (high) on five criteria the brief names. Budget fit is the share of the remaining budget (13,740 triangles, 0 spare draw calls) the fix would consume.

| Component | Evidence quality | Customer importance | Current deficiency | Feasibility in budget | Validation ability | Total |
|---|---|---|---|---|---|---|
| Front seats (re-zone inserts/bolsters) | 3 | 3 | 3 | 3 — re-shape existing primitives, no new draw call | 3 — fixed cameras + photos 08/29/30 | **15** |
| Console top finish and parts | 3 | 2 | 3 | 2 — touchpad/knob need geometry inside existing primitives | 3 | 13 |
| Dash end cap colour | 3 | 2 | 2 | 3 — material change only | 3 | 13 |
| Steering wheel bezels/switches | 3 | 2 | 2 | 2 | 3 | 12 |
| Dashboard display hood/stack | 3 | 2 | 2 | 2 | 2 | 11 |
| Front door panels | 3 | 2 | 3 | 1 — new primitives exceed 24 draw calls | 2 | 11 |
| Floor/carpet | 2 | 1 | 3 | 1 — new draw call | 2 | 9 |
| Rear seats | 3 | 1 | 3 | 1 — large triangle and draw-call cost | 2 | 10 |
| Roof/headliner/pillars | 2 | 1 | 3 | 1 | 1 | 8 |
| Rear doors, rear vents, other details | 2 | 1 | 3 | 1 | 1 | 8 |

## Findings

1. **Front seats are the largest visible error and the main product.** Customers choose upholstery, colour, thread and treatment on the seat. The model's sport-bucket shape and its seam layout do not match the car in eight photos, so every treatment preview is shown on the wrong seat.
2. **Draw calls, not triangles, block the full cabin.** The model already uses all 24 draw calls. Doors, floor, roof and rear seats each need new primitives. They need either primitive merging or a measured budget increase, which the owner has said requires workshop-PC and mobile measurements.
3. **The Driver Hero grey block is a material/camera problem, not a missing-door problem alone.** The real dash end cap is black. Re-colouring it removes most of the distraction without new geometry; a door panel would hide it fully later.
4. **Some research claims are weaker than stated.** The four "official interior" JPGs are exterior shots; the research's door-part lead (67640-06P30-C8) is red/red/silver, not the donor's black. The gallery, not those sources, should drive geometry.
5. **Remaining evidence needed before seat geometry is final:** window sticker or VIN decode (leather vs NuLuxe, wood name), and, if the owner can, two measured seat dimensions (cushion width, backrest height) so the shape is not scaled from photos.
