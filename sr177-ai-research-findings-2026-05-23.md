# SR-177 AI Research Findings - 2026-05-23

## Run metadata

- Issue: #24
- Research date: 2026-05-23
- Research baseline: April 2026 substantive site content. The May 22 and earlier May 23 site update entries are not treated as the last substantive SR-177 research baseline because the user clarified the site had not been updated since creation in April 2026.
- Site context: SR-177 / West Davis Highway extension into Weber County, especially the Phase 3 segment from 1800 North in West Point to 4000 South in West Haven.
- Verification method: Tool-assisted web fetches opened official public pages and ArcGIS REST JSON endpoints. No interactive browser map inspection was available in this session.
- Publication standard: Do not publish parcel-level owner, contact, tax, acquisition, or parcel-specific ROW details. Use public GIS only as high-level technical context unless UDOT publishes formal environmental-study maps for public use.

## Executive summary

Official static UDOT and PublicInput materials still support the same formal project status: the Weber County segment is in State Environmental Study alternatives development/evaluation, the Draft State Environmental Study is expected in Fall 2026, construction remains unfunded, and no final approved preferred alignment or final parcel-level right-of-way boundary has been published through the formal public study materials.

The deep search found newer public ArcGIS material that should be acknowledged carefully. A public ArcGIS web map titled `UT-11199-25 SR-177 Map` was verified on 2026-05-23. Its map data includes a `Project Layers` map service and a visible `21158 Hybrid Concept Design` group with `Hybrid ROW Impacts`, `Polylines`, and `Polygons` layers. A separate public feature service titled `UT_11199_SR_177_AGOL` is tagged `ROW` and `R&D` and has the snippet `ROW layer populated by SharePoint Excel file`.

This is publishable only as technical-source context. It is not safe to describe the ArcGIS content as a final selected alignment, a final approved preferred alternative, a legal right-of-way boundary, or parcel-level acquisition guidance.

## Sources checked

| Source | URL | Date signal | Source strength | Result |
|---|---|---:|---|---|
| UDOT SR-177 PublicInput study page | `https://udotinput.utah.gov/sr177extension` | 2026 project page | Official project outreach page | Still the controlling public status source for schedule, SES process, and formal study milestone language. |
| UDOT 2026 construction announcement | `https://connect.udot.utah.gov/` | 2026 construction season | Official UDOT communications | Supports Davis County Phase 2 construction context only; does not change Weber County Phase 3 construction funding status. |
| ArcGIS web map item metadata | `https://www.arcgis.com/sharing/rest/content/items/06fff9f11bc84a3eb1db7504d53b854a?f=pjson` | Created 2025-09-09; modified 2026-05-21 17:56:13 UTC | Public ArcGIS item metadata | Verified title `UT-11199-25 SR-177 Map`, type `Web Map`, tag `UT-11199`, access `public`, owner `zachs_horrocks`. |
| ArcGIS web map data | `https://www.arcgis.com/sharing/rest/content/items/06fff9f11bc84a3eb1db7504d53b854a/data?f=pjson` | Verified 2026-05-23 | Public ArcGIS map configuration | Shows operational layers including `Project Layers`, `Comments`, and `ROW Parcels`. |
| ArcGIS project layers map service | `https://utility.arcgis.com/usrsvcs/servers/dfbe95055be447f9b6538bcf31c6ab7a/rest/services/UT_11199_25_SR177_Layers/MapServer?f=pjson` | Verified 2026-05-23 | Public ArcGIS map service metadata | Shows layer group `Concepts`, `21158 Hybrid Concept Design`, `Hybrid ROW Impacts`, `Polylines`, `Polygons`, 2013 alternatives, study area, agricultural, active-transportation, historic-architecture, and aquatic-resource layers. |
| ArcGIS ROW feature service metadata | `https://www.arcgis.com/sharing/rest/content/items/ebb32890c91d442aa50d2dde909ab7e2?f=pjson` | Created 2026-04-15; modified 2026-05-22 19:58:52 UTC | Public ArcGIS hosted feature-service metadata | Verified title `UT_11199_SR_177_AGOL`, tags `ROW` and `R&D`, snippet `ROW layer populated by SharePoint Excel file`, access `public`. |
| ArcGIS ROW feature service REST endpoint | `https://services1.arcgis.com/bZPGbreElTLjIAKW/arcgis/rest/services/UT_11199_SR_177_AGOL/FeatureServer?f=pjson` | Verified 2026-05-23 | Public ArcGIS feature-service metadata | Confirms a queryable feature layer named `ROW_Parcels_Join`. Do not republish parcel-level contents. |
| ArcGIS comments item metadata | `https://www.arcgis.com/sharing/rest/content/items/4807e698ed274f59ffb48137c4e7fce?f=pjson` | Verified 2026-05-23 | Public item lookup attempted | Item metadata was inaccessible or unavailable; mention only if needed as a layer present in the web map configuration, not as a standalone cited source. |
| WFRC Regional Transportation Plan | `https://wfrc.org/planning/transportation-plans` | 2023 adopted plan | Official regional plan | Continues to support 2043-2050 planning-window language. |
| Standard-Examiner and KSL sources | `https://www.standard.net/`, `https://ksl.com/` | April 2026 / 2026 | Media and public-record context | Useful background, but no stronger source than the newly found ArcGIS metadata for May 2026 technical context. |

## New findings

1. A public ArcGIS web map for `UT-11199-25 SR-177 Map` exists and was modified on 2026-05-21 according to item metadata.
2. The web map references a public `UT_11199_25_SR177_Layers` MapServer. Its layer list includes a `21158 Hybrid Concept Design` group and a `Hybrid ROW Impacts` layer.
3. The web map also references a public `ROW Parcels` feature layer. The related item metadata says it is a ROW layer populated by a SharePoint Excel file, with item metadata modified on 2026-05-22.
4. The public GIS material appears newer than the static public-facing UDOT study page, but it does not by itself establish a final approved preferred alignment or final legal right-of-way.
5. The site should replace absolute claims such as `No specific parcel data has been publicly released` with more precise language: no final public environmental-study parcel determinations or final parcel-level right-of-way boundary have been published through the controlling Draft/Final State Environmental Study materials.

## Pages to update

| Page/file | Recommended change |
|---|---|
| `src/_data/references.json` | Add ArcGIS web map, project layers map service, and ROW feature-service metadata as technical sources. |
| `src/index.njk` | Keep the active-study banner, but distinguish final UDOT approval from working public GIS context. |
| `src/project-status.njk` | Add a short technical-context callout after the current status paragraph. |
| `src/planning.njk` | Add a paragraph noting the May 2026 public GIS hybrid concept design as working technical context. |
| `src/property-owner-guide.njk` | Add a warning that public working GIS is not a parcel determination and should not replace Draft SES maps or legal advice. |
| `src/property.njk` | Replace the stale `No specific parcel data has been publicly released` claim with cautious final-ROW language and technical-source context. |
| `src/timeline.njk` | Optionally cite public GIS for Spring 2026 footprint mapping underway, while preserving Fall 2026 as the first formal public milestone. |
| `src/west-haven-context.njk` | Optionally soften `UDOT has not published a preferred alignment` to `UDOT has not formally approved or published a final preferred alignment`. |
| `src/references.njk` | Update the references page intro so last-accessed dates may be May 23, 2026. |
| `src/_data/updates.json` | Revise the May 23 content update entry. The previous `no new publishable facts` summary is now inaccurate. |

## Suggested citation entries

```json
{
  "id": "arcgis-sr177-webmap-may2026",
  "group": "legal-technical",
  "org": "ArcGIS Online / Horrocks",
  "title": "UT-11199-25 SR-177 Map",
  "source": "arcgis.com",
  "date": "Modified May 21, 2026; verified May 23, 2026",
  "url": "https://www.arcgis.com/sharing/rest/content/items/06fff9f11bc84a3eb1db7504d53b854a?f=pjson"
}
```

```json
{
  "id": "arcgis-sr177-project-layers-may2026",
  "group": "legal-technical",
  "org": "ArcGIS Online / Horrocks",
  "title": "UT_11199_25_SR177_Layers MapServer",
  "source": "utility.arcgis.com",
  "date": "Verified May 23, 2026",
  "url": "https://utility.arcgis.com/usrsvcs/servers/dfbe95055be447f9b6538bcf31c6ab7a/rest/services/UT_11199_25_SR177_Layers/MapServer?f=pjson"
}
```

```json
{
  "id": "arcgis-sr177-row-service-may2026",
  "group": "legal-technical",
  "org": "ArcGIS Online / Horrocks",
  "title": "UT_11199_SR_177_AGOL ROW Feature Service Metadata",
  "source": "arcgis.com",
  "date": "Modified May 22, 2026; verified May 23, 2026",
  "url": "https://www.arcgis.com/sharing/rest/content/items/ebb32890c91d442aa50d2dde909ab7e2?f=pjson"
}
```

## Suggested updates.json entry

Revise the existing 2026-05-23 content entry rather than adding a competing same-day entry. Suggested summary:

`AI-assisted research checked official UDOT, local-government, WFRC, media, and public ArcGIS sources. The update adds cautious May 2026 technical-source context for a public SR-177 ArcGIS web map, project layers, and ROW feature-service metadata while preserving the key warning that no final approved preferred alignment or final parcel-level right-of-way boundary has been published through the formal State Environmental Study materials.`

Related source IDs should include `udot-ses-schedule`, `udot-ses-build`, `wfrc-rtp-2023-2050`, `arcgis-sr177-webmap-may2026`, `arcgis-sr177-project-layers-may2026`, and `arcgis-sr177-row-service-may2026`.

## Claims not safe to publish yet

- That `21158 Hybrid Concept Design` is the final selected alignment.
- That any individual parcel is definitely acquired, displaced, partially acquired, or outside impact.
- Owner names, parcel numbers, contact fields, tax IDs, acquisition status fields, appraised values, or comments from the ROW feature service.
- That the project is funded for construction before the WFRC/UDOT funding record changes.
- That Fall 2026 Draft SES maps are already available.
- That the ArcGIS map is the legally controlling environmental-study publication.

## Human verification checklist

- Tool-assisted source fetch completed: yes.
- Official static UDOT/PublicInput source opened: yes.
- ArcGIS web map metadata opened: yes.
- ArcGIS web map data opened: yes.
- ArcGIS MapServer opened: yes.
- ArcGIS ROW feature-service metadata opened: yes.
- Dynamic browser inspection of the interactive map completed: no, not available in this session.
- Parcel-level content reviewed for publication: no, intentionally avoided beyond metadata-level verification.
- Recommendation: after publishing, a human should open the interactive ArcGIS web map and UDOT SR-177 PublicInput page in a browser to confirm no public-facing official notice contradicts the cautious wording.

## Exact file changes recommended

1. Add the three ArcGIS source IDs to `src/_data/references.json` under `legal-technical`.
2. Revise the May 23 entry in `src/_data/updates.json` so it no longer says no new publishable facts were found.
3. Update `src/index.njk`, `src/project-status.njk`, `src/planning.njk`, `src/property-owner-guide.njk`, and `src/property.njk` with high-level public GIS caveats.
4. Update `src/timeline.njk` only where it already discusses footprint mapping underway.
5. Update `src/west-haven-context.njk` only to distinguish final approval from working technical context.
6. Update `src/references.njk` date/freshness language to cover sources verified on May 23, 2026.
7. Run source-ID validation and `npm run build`.
