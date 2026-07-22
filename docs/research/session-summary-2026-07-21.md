# Session Summary — SR-177 Research Pass, 2026-07-21

**Session type:** AI-assisted research pass per `docs/ai-research-updates.md`
**Formal research record:** [`docs/research/findings/2026-07-21.md`](findings/2026-07-21.md) (the auditable, self-contained record; this file is a readable companion summary)
**GitHub issue:** [#36](https://github.com/XeroIP/sr177-weber-analysis/issues/36) (reused — opened for the 07-07 pass, still covers this window)
**Window researched:** 2026-05-23 → 2026-07-21

---

## Bottom line

The site's core message is **still correct and must not be softened**: the Weber County segment (1800 N → ~4000 S) remains in the State Environmental Study alternatives phase. As of July 21, 2026 there is **no Draft SES, no preferred alternative, and no parcel-level right-of-way determination** — verified live against UDOT's study page.

What *has* changed is everything around it: Phase 2 construction in Davis County has officially started, a contractor is under contract, WFRC has an **active public comment window closing August 2, 2026**, and Weber County has taken its first formal position on where the corridor's Weber County continuation should run.

---

## Headline findings

### 1. Phase 2 construction has started (official)
UDOT's West Davis site now says: *"Construction activities beginning this July! SR-177 (West Davis Highway) extension is moving from design into construction!"*
- Preliminary work (vegetation/brush clearing, fencing, environmental mitigation, site prep) through end of July 2026
- Full construction anticipated **first week of August 2026**, beginning with pile driving near 700 South (bridge work)
- This supersedes the site's "Construction Commencing Summer 2026" anticipatory language and resolves the 07-07 pass's "not safe to publish yet" hold on a construction-start claim

### 2. WFRC Draft 2027–2032 TIP — comment period OPEN, time-sensitive
- Released **July 6, 2026**; public comment through **August 2, 2026** at `wfrc.utah.gov/tip-comment`
- In-person open house at **Lindquist Field, Ogden — July 28, 2026, 4:30–7:00 p.m.** (directly relevant to the site's Weber County audience)
- Draft includes the WDC SR-193 → 1800 N extension
- **Unverified:** whether the 1800 N & 4500 W intersection project made the draft — tables are only in an interactive map (human verification item)
- Publication urgency: this item loses most of its value after Aug 2

### 3. Weber County approved a west-of-the-river alignment letter to UDOT (official)
- **June 29, 2026 Commission work session (approved minutes):** staff reported developers, landowners, and the Planning Commission all agreed the corridor should stay **west of the river**; Commissioners approved gathering stakeholder signatures and sending a letter to UDOT and State Transportation officials. Minutes approved unanimously July 6.
- Minutes: `https://www.webercountyutah.gov/commission/documents/work_session/min_pdf/min_06292026.pdf` (approval: `.../min_07062026.pdf`)
- The county's records call the corridor the **"West Weber Freeway"** / **"North Legacy Highway"** — never "SR-177" or "West Davis."
- A county **request**, not a decision — UDOT retains alignment authority. No public record yet of the letter being sent.

### 4. UDOT Region 1 verbally indicated an eastern-alignment preference (official minutes)
- **March 3, 2026 joint Commission/Planning Commission minutes:** UDOT Region 1 "indicated they prefer an eastern alignment for North Legacy Highway rather than the western alignment currently shown in County plans, citing environmental concerns and traffic projections." County initiated a General Plan refresh.
- Minutes (standalone approved copy, marked "APPROVED 4.7.2026" — preferred citation): `https://www.webercountyutah.gov/planning/documents/uploads/03-03-26%20minutes_%20Approved.pdf` (alternate: April 7 packet p.3, `https://www.utah.gov/pmn/files/1413703.pdf`)
- Together with finding 3, this documents a county-vs-UDOT alignment tension — publishable as two attributed positions, **not** as any UDOT decision.

### 5. Public working GIS still actively maintained
- ROW feature service (`UT_11199_SR_177_AGOL`) modified **2026-07-21 08:13 — the morning of this pass**
- Web map modified 2026-06-26
- Web map layer inventory (from item data JSON): SouthImage, NorthImage, **"5500 S Image"**, Project Layers, Existing Utilities, Comments, **ROW Parcels**
- All timestamps verified from raw JSON with programmatic epoch conversion (AI-summarized fetches have mis-converted these before)

### 6. A cited reference went dark (stale-reference finding)
The MapServer endpoint cited as `arcgis-sr177-project-layers-may2026` now returns **HTTP 500 ("Error generating token")** — confirmed twice plus a `/layers` path attempt. Consequences:
- The 4000 S / 5500 S tie-in layer names recorded on 07-07 can no longer be re-verified live
- Site must annotate the access limitation per publication rules (no citing inaccessible material without explanation)
- Fallback verification path documented: the web map item's `/data?f=json` endpoint still exposes the layer inventory

### 7. Draft SES status re-verified — no change
Schedule unchanged on UDOT's page: Draft SES (public hearing + 30-day comment) spring–fall 2026; Final SES late 2026. All "as of May 23, 2026" site language can refresh to July 21, 2026 with wording intact.

---

## Reconciliation: the un-applied 2026-07-07 pass

The 07-07 findings file existed but was **uncommitted, and none of its recommended site changes were ever applied** (no 07-07 entry in `updates.json`). Every item was re-verified this session rather than trusted:

| 07-07 item | Status at 07-21 |
|---|---|
| Granite Construction ~$116.9M Phase 2 contract (June 24) | Re-verified live from Granite newsroom — publishable |
| WFRC May 28 packet: 1800 N & 4500 W TIP submission ("will fail" on SR-177 opening day) | PDF still accessible (range-request check); content verified programmatically on 07-07 — publishable as a submission, not an approved project |
| 2028 vs mid-2029 Phase 2 completion conflict | **Now intra-official** — an official UDOT project-preview page (PIN 20927, updated Oct 14, 2025) says "Summer 2028," while UDOT's March 26, 2026 announcement says mid-2029; WFRC's July 6 blog and April media also say 2028. Lead with mid-2029, attribute the rest |
| Tie-in layers (4000 S / 5500 S) | Endpoint now dead; attribute layer names to the 07-07 verification date if published |
| Uncited West Haven utility-relocation sentence (`engineering.njk:112`) | Still present, still unsupported — fix stands |

## What turned up nothing

- **West Haven City Council** (June–July agendas via Utah PMN): budget, energy tax, RMP franchise — no SR-177/5100 W/UDOT items
- **Hooper City:** nothing
- **Weber County news page:** no SR-177-named items; two adjacent leads deferred as not SR-177-specific:
  - July 2, 2026 — 0.20% sales tax approved for public safety + transportation infrastructure
  - June 15, 2026 — UIPA West Weber Project Area Plan amendment
- **UDOT Region One blog:** nothing tagged West Davis since Jan 2025
- **Media:** nothing new since the April 21 roundup / April 24 opposition letter (both already cited); Granite award coverage is all secondary to the PR

## Guardrails — not safe to publish

1. Any **interpretation** of the "5500 S Image" / tie-in layers (names and dates only)
2. Granite's "~three miles" (UDOT official: 2.5 miles)
3. "Opening 2028" as settled (UDOT says mid-2029 — present as cited conflict or UDOT only)
4. 1800 N & 4500 W inclusion in the *draft* TIP (unverified)
5. The county letter's specific recipients (not in the minutes; verify from the meeting recording), or that the letter has been sent
6. Mapping "west of the river" to a specific site phase or alignment (the minutes define no segment boundaries)
7. Equating UDOT Region 1's verbal eastern preference with an SES outcome
8. The Weber County sales tax as SR-177-related (no linkage in the notice)
9. Any softening of the core alignment/ROW uncertainty warnings

## Notable stale claims on the live site

Worst offender: `src/hooper-context.njk:116` — *"2028 — Phase 2 construction begins"* (construction began July 2026). Full stale-claim table with file:line references is in the formal findings record.

---

## Session workflow notes

- **Inputs:** `last_research_date` 2026-05-23 · `run_date` 2026-07-21T23:11:59-06:00 · issue #36 reused · scope: routine + 07-07 reconciliation
- **Verification methods:** live WebFetch of every publication-candidate source; raw-JSON curl + Python epoch conversion for ArcGIS metadata; HTTP range request for PDF liveness; two-attempt confirmation of the MapServer failure; direct download and programmatic keyword-scan of county minutes and packets (one packet: 666 pages / 17 MB)
- **Publication gate:** satisfied — all sources recommended for publication were opened and verified live this pass (tool-assisted check per the workflow); remaining human-verification items are listed in the findings record
- **Independent cross-verification:** a second AI research pass (`docs/research/findings/2026-07-22.md`) was reconciled into the formal record on 2026-07-22 — every new claim re-verified live before integration. Verified additions: the UDOT project-preview page (making the 2028/mid-2029 conflict intra-official), the standalone approved March 3 minutes URL, Granite Wells Pit quantities, expanded GIS metadata, and the Ogden open-house address. Errors corrected: it audited `cityofwesthaven.com`, which is West Haven, **Connecticut** (Utah's is `westhavenut.gov`). One combined `updates.json` entry should represent the whole cycle
- **Methodology fixes for future passes:** probe `webercountyutah.gov/commission/documents/work_session/min_pdf/min_MMDDYYYY.pdf` directly (not search-indexed), and add the county's corridor names — "West Weber Freeway", "North Legacy Highway" — to all search plans; SR-177/West Davis keywords alone miss county governance actions
- **Files produced this session:**
  - `docs/research/findings/2026-07-21.md` (formal record)
  - `docs/research/session-summary-2026-07-21.md` (this file)
  - Both this file's companion record and the still-uncommitted `findings/2026-07-07.md` should be committed together with any site changes

## Recommended next steps

1. Branch + apply the site update per the findings record (references, updates.json, content pages including Governance and Phase 4 Long-Range, references page)
2. `npm run build` + verify `/whats-changed.html` ordering
3. PR referencing #36 (`Refs #36` until the site changes merge, then close)
4. **Do it before July 28** if the Ogden open house / Aug 2 comment deadline is to be useful to readers
