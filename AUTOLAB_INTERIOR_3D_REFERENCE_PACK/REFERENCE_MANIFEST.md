# AutoLab Interior 3D Reference Manifest

This manifest documents all 16 approved AI-generated design references for the AutoLab premium SUV interior 3D asset pipeline.

---

## 1. Approved Component Classification Matrix

| Component | Approved Filename | Relative Repository Path | Source Identifier | Status | Intended Modelling Use | Known Limitations |
|---|---|---|---|---|---|---|
| **Master Cabin** | `AUTOLAB_SUV_MASTER_CABIN_3Q_SIDE_VIEW_01.jpg` | `00_MASTER_CABIN/PRIMARY/AUTOLAB_SUV_MASTER_CABIN_3Q_SIDE_VIEW_01.jpg` | 3Q perspective generation | **Primary** | Whole-cabin assembly, spatial adjacency between rows, pillar rake, and interior harmony. | Peripheral glass and exterior environment are illustrative; do not model external background. |
| **Master Cabin** | `AUTOLAB_SUV_MASTER_CABIN_REAR_FORWARD_VIEW_02.jpg` | `00_MASTER_CABIN/SECONDARY/AUTOLAB_SUV_MASTER_CABIN_REAR_FORWARD_VIEW_02.jpg` | Rear-forward perspective generation | **Secondary** | Symmetrical cabin width, center-tunnel alignment, roof console alignment, and headliner curvature. | Armrest is shown stowed; does not show internal cupholder deployment. |
| **Front Door Panel** | `AUTOLAB_SUV_FRONT_DOOR_PANEL_PRIMARY_01.jpg` | `01_FRONT_DOOR_PANELS/PRIMARY/AUTOLAB_SUV_FRONT_DOOR_PANEL_PRIMARY_01.jpg` | Straight-on multi-switch generation | **Primary** | Authoritative driver door card geometry, speaker grille shape, 4-window switch cluster, and leather insert. | Backside mounting clips and internal wiring are omitted; cosmetic inner face only. |
| **Front Door Panel** | `AUTOLAB_SUV_FRONT_DOOR_PANEL_ALTERNATE_02.jpg` | `01_FRONT_DOOR_PANELS/ALTERNATES/AUTOLAB_SUV_FRONT_DOOR_PANEL_ALTERNATE_02.jpg` | Oblique perspective generation | **Alternate** | Armrest ledge depth, pull-cup recess depth, and door handle clearance validation. | Lighting differs slightly from primary; do not use for base colour calibration. |
| **Rear Door Panel** | `AUTOLAB_SUV_REAR_DOOR_PANEL_PRIMARY_01.jpg` | `02_REAR_DOOR_PANELS/PRIMARY/AUTOLAB_SUV_REAR_DOOR_PANEL_PRIMARY_01.jpg` | Straight-on single-switch generation | **Primary** | Authoritative rear door card geometry, wheel-well clearance contour, single window switch, and speaker pod. | Mirror controls not present on rear door; do not confuse with front door card. |
| **Rear Door Panel** | `AUTOLAB_SUV_REAR_DOOR_PANEL_ALTERNATE_02.jpg` | `02_REAR_DOOR_PANELS/ALTERNATES/AUTOLAB_SUV_REAR_DOOR_PANEL_ALTERNATE_02.jpg` | Rear panel angle variant | **Alternate** | Cross-checking door card thickness, armrest contour, and lower pocket depth. | Subtle tone variation; subordinate to primary. |
| **Front Seat** | `AUTOLAB_SUV_FRONT_SEAT_PRIMARY_01.jpg` | `03_FRONT_SEATS/PRIMARY/AUTOLAB_SUV_FRONT_SEAT_PRIMARY_01.jpg` | `66cac` | **Primary** | Authoritative seat shell contour, bolster breaks, fluting/channel lines, perforation zone, and control valance. | Seat rail slider track mechanism is simplified for realtime budgets. |
| **Front Seat** | `AUTOLAB_SUV_FRONT_SEAT_ALTERNATE_02.jpg` | `03_FRONT_SEATS/ALTERNATES/AUTOLAB_SUV_FRONT_SEAT_ALTERNATE_02.jpg` | `5e24c` | **Alternate** | Headrest post extension height, headrest tilt angle, and side bolster transition profile. | Headrest posts are elevated; primary shows standard retracted configuration. |
| **Rear Bench** | `AUTOLAB_SUV_REAR_BENCH_PRIMARY_01.jpg` | `04_REAR_BENCH/PRIMARY/AUTOLAB_SUV_REAR_BENCH_PRIMARY_01.jpg` | `c328a` | **Primary** | Authoritative 60/40 bench geometry, center armrest pull loop, 3-headrest setup, and floor mount tabs. | Folding seat hinge mechanisms and rear cargo backboards are not visible. |
| **Rear Bench** | `AUTOLAB_SUV_REAR_BENCH_ALTERNATE_02.jpg` | `04_REAR_BENCH/ALTERNATES/AUTOLAB_SUV_REAR_BENCH_ALTERNATE_02.jpg` | Bench detail variant | **Alternate** | ISOFIX child-seat anchor point locations, shoulder belt guides, and side bolsters. | Shows raised outer headrests; use primary for default rest posture. |
| **Dashboard & Console** | `AUTOLAB_SUV_DASHBOARD_CONSOLE_PRIMARY_01.jpg` | `05_DASHBOARD_AND_CONSOLE/PRIMARY/AUTOLAB_SUV_DASHBOARD_CONSOLE_PRIMARY_01.jpg` | `de8a7` | **Primary** | Authoritative dashboard tiering, widescreen display hood, HVAC vents, console bridge, and shifter surround. | Steering wheel emblem is neutral/unbranded; do not add OEM badges. |
| **Dashboard & Console** | `AUTOLAB_SUV_DASHBOARD_CONSOLE_ALTERNATE_02.jpg` | `05_DASHBOARD_AND_CONSOLE/ALTERNATES/AUTOLAB_SUV_DASHBOARD_CONSOLE_ALTERNATE_02.jpg` | High-angle approved generation | **Alternate** | Top-down view of transmission tunnel controls, drive-mode dial, cupholder recess, and passenger airbag seam. | Steering wheel tilt angle is slightly higher; primary controls eye-level relationship. |
| **Cabin Shell** | `AUTOLAB_SUV_CABIN_SHELL_3Q_CUTAWAY_01.jpg` | `06_CABIN_SHELL/PRIMARY/AUTOLAB_SUV_CABIN_SHELL_3Q_CUTAWAY_01.jpg` | Cutaway structural generation | **Primary** | Body-in-white proportions, floorpan drop, transmission tunnel height, and pillar datum coordinates. | **STRUCTURAL REFERENCE ONLY.** Exposed metal, bare sheet stampings, and cutaway edges must NOT be rendered in finished cabin. |
| **Cabin Shell** | `AUTOLAB_SUV_CABIN_SHELL_REAR_FORWARD_02.jpg` | `06_CABIN_SHELL/SECONDARY/AUTOLAB_SUV_CABIN_SHELL_REAR_FORWARD_02.jpg` | Stripped rear-forward generation | **Secondary** | Cross-car dash crossbeam elevation, firewall bulkhead position, and carpet edge termination. | **STRUCTURAL REFERENCE ONLY.** Raw internal structures must remain covered by trim. |
| **Starlight Headliner** | `AUTOLAB_STARLIGHT_HEADLINER_CABIN_VIEW_01.jpg` | `07_STARLIGHT_HEADLINER/PRIMARY/AUTOLAB_STARLIGHT_HEADLINER_CABIN_VIEW_01.jpg` | `9c0d64cc` | **Primary** | Fibre optic star density, distribution pattern around moonroof cutout, and Alcantara material response. | Fibre stars must be implemented as configurable lighting elements, not flat baked glowing textures. |
| **Starlight Headliner** | `AUTOLAB_STARLIGHT_HEADLINER_DETAIL_02.jpg` | `07_STARLIGHT_HEADLINER/SECONDARY/AUTOLAB_STARLIGHT_HEADLINER_DETAIL_02.jpg` | `977d6cc4` | **Secondary** | Overhead view of roof console switches, overhead grab handles, visors, and perimeter star falloff. | High-angle perspective; complementary to primary forward view. |
| **Showroom Concepts** | *(None supplied)* | `99_EXCLUDED/SHOWROOM_CONCEPTS/` | White showroom hero prompts | **Excluded** | Application presentation direction only. | **EXCLUDED FROM MODELLING.** Bright white studio environment is a runtime stage lighting setup, not a 3D geometry target. |

---

## 2. Technical Asset Ledger

Every image file in this repository matches the verified inventory below:

| Relative Path | Format | Dimensions | File Size (Bytes) | Size (MB) | SHA-256 Checksum |
|---|---|---|---|---|---|
| `00_MASTER_CABIN/PRIMARY/AUTOLAB_SUV_MASTER_CABIN_3Q_SIDE_VIEW_01.jpg` | JPEG | 2752 × 1536 | 2,586,400 | 2.47 MB | `b78e068d1150493f1857c6bfe73f8ff2b15748805f6b3e9a7e0a2408c5c4e9cb` |
| `00_MASTER_CABIN/SECONDARY/AUTOLAB_SUV_MASTER_CABIN_REAR_FORWARD_VIEW_02.jpg` | JPEG | 2752 × 1536 | 2,532,050 | 2.41 MB | `e90cad8f4833a1e5aa4ec000e39546059d332d96c929dd5fbdd7f6074a36f56e` |
| `01_FRONT_DOOR_PANELS/PRIMARY/AUTOLAB_SUV_FRONT_DOOR_PANEL_PRIMARY_01.jpg` | JPEG | 2752 × 1536 | 2,205,797 | 2.10 MB | `3b7e1262e0e960fe7a4bc8344eebdb2ce5fc50f0003056093409ae2fc5b80d7d` |
| `01_FRONT_DOOR_PANELS/ALTERNATES/AUTOLAB_SUV_FRONT_DOOR_PANEL_ALTERNATE_02.jpg` | JPEG | 2752 × 1536 | 1,829,280 | 1.74 MB | `555801aafb8f526b38cffbf230a84f336e9ff979e27c19958bc59e358b53cf2d` |
| `02_REAR_DOOR_PANELS/PRIMARY/AUTOLAB_SUV_REAR_DOOR_PANEL_PRIMARY_01.jpg` | JPEG | 2752 × 1536 | 2,271,420 | 2.17 MB | `70531b1ed2d7a7f82c7414e126f90500b0d1f1a9722e56f0341c853f4043f728` |
| `02_REAR_DOOR_PANELS/ALTERNATES/AUTOLAB_SUV_REAR_DOOR_PANEL_ALTERNATE_02.jpg` | JPEG | 2752 × 1536 | 2,285,920 | 2.18 MB | `d923595715f591501cc611b39c266939118e472f9ff81998e731fc8e19532e69` |
| `03_FRONT_SEATS/PRIMARY/AUTOLAB_SUV_FRONT_SEAT_PRIMARY_01.jpg` | JPEG | 2752 × 1536 | 1,746,071 | 1.67 MB | `83cc5d47c43ad1679aa22668eeb6330386c965b2067e4168da1c54b201a084eb` |
| `03_FRONT_SEATS/ALTERNATES/AUTOLAB_SUV_FRONT_SEAT_ALTERNATE_02.jpg` | JPEG | 2752 × 1536 | 1,730,394 | 1.65 MB | `d9c91b5d6fc0ce3102ce62eb864ec282055694205aa86121b6d135c3cba00788` |
| `04_REAR_BENCH/PRIMARY/AUTOLAB_SUV_REAR_BENCH_PRIMARY_01.jpg` | JPEG | 2752 × 1536 | 2,221,009 | 2.12 MB | `b6c9e340fcaa42938a9d16a56c4aa637a2ccb9557bf807b0ba9952df7eaec3fb` |
| `04_REAR_BENCH/ALTERNATES/AUTOLAB_SUV_REAR_BENCH_ALTERNATE_02.jpg` | JPEG | 2752 × 1536 | 2,382,401 | 2.27 MB | `01b7da576a4392eeea0e5b7fbca96b27d35ce4a2ecfa6c13eb3ff9981e7d23a9` |
| `05_DASHBOARD_AND_CONSOLE/PRIMARY/AUTOLAB_SUV_DASHBOARD_CONSOLE_PRIMARY_01.jpg` | JPEG | 2752 × 1536 | 2,046,951 | 1.95 MB | `49c0c8f1d61e479a0980c58e8e747c3e536102f8dd6f3fcdaaa09673cc3598f1` |
| `05_DASHBOARD_AND_CONSOLE/ALTERNATES/AUTOLAB_SUV_DASHBOARD_CONSOLE_ALTERNATE_02.jpg` | JPEG | 2752 × 1536 | 2,011,993 | 1.92 MB | `d6a9cbe8d0061eec6d26732ea27072a71bf5ffea8e93235ffebf47f254ee8780` |
| `06_CABIN_SHELL/PRIMARY/AUTOLAB_SUV_CABIN_SHELL_3Q_CUTAWAY_01.jpg` | JPEG | 2752 × 1536 | 1,941,158 | 1.85 MB | `c8dbe6a2f573ef89073041ec3528b17b2b73ecb15f9ee73b6fe8cefc50a11681` |
| `06_CABIN_SHELL/SECONDARY/AUTOLAB_SUV_CABIN_SHELL_REAR_FORWARD_02.jpg` | JPEG | 2752 × 1536 | 2,604,668 | 2.48 MB | `9be5876c0b97b090e9d6d39366e44d3d81b4d37c94b79373f7c9e0d1d2834b92` |
| `07_STARLIGHT_HEADLINER/PRIMARY/AUTOLAB_STARLIGHT_HEADLINER_CABIN_VIEW_01.jpg` | JPEG | 2752 × 1536 | 2,463,723 | 2.35 MB | `afea10196a4ebb5180be6396821217db55225d30900e4e7fa0692d4f8286f788` |
| `07_STARLIGHT_HEADLINER/SECONDARY/AUTOLAB_STARLIGHT_HEADLINER_DETAIL_02.jpg` | JPEG | 2752 × 1536 | 2,716,953 | 2.59 MB | `24aa7a50db1631557bf0076a0fb4be07c87c0ff3be7e722512eece0eb13bc499` |

**Total Cumulative Pack Size:** 35,576,188 bytes (33.93 MiB / 35.58 MB)  
**Total Images:** 16  
**Format Consistency:** 100% JPEG (2752 × 1536, 16:9 ratio)
