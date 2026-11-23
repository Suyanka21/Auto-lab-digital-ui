# Future configurator interfaces — proposals only
Updated 2026-11-19. No viewer, shader, UI, camera or runtime contract changes applied.

| Region | Current candidate assignment | Current consequence | Later requirement |
|---|---|---|---|
| Door middle + armrest/pull | MAT_Seat_Secondary | Recolours with secondary seats | If independent door colour is required, approve a dedicated door upholstery slot and adapter input; preserve panel provenance and UVs |
| Door decorative insert | MAT_Console_Carbon | Same finish as dash/console | Existing shared finish preview; separate door finish would require a further explicit contract |
| Door shell/pocket/speaker | MAT_Cockpit_Black | Structural black | Retain fixed finish |
| Upper door padding | MAT_Dashboard_Trim | Fixed leather tint | May be separated later if commercially required |
| Metal handle/rim | MAT_Console_Metal | Existing metallic behaviour | Retain |
| Headliner (not built) | None approved independently | Shared dashboard slot would not be independent | Propose MAT_Headliner, bounded normal/roughness texture and dedicated component; not added |
| Starlights (not built) | None | No independent lighting feature exists | Local roof-space anchor data plus visibility/intensity controls; optional instanced points at integration; no permanent emission bake |

Future starlight interface should distinguish enabled, intensity and optional twinkle, with a quiet reduced-motion state and no new permanent canvas. Roof opening exclusion zones and headliner mounting normals must accompany anchor data. Implementing this requires later viewer approval; no current runtime promise is made.
The bright white showroom belongs to later lighting/environment configuration, not model geometry. Current inspection lights do not establish final viewer appearance.
