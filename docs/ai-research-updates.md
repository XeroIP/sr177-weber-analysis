# AI Research Update Workflow

Use this workflow when periodically asking AI to search for new SR-177 information and update the site.

## Goals

- Find new public information about SR-177 / West Davis Highway.
- Update affected site pages only when claims are verifiable.
- Preserve uncertainty instead of overstating rumors, early reports, or unsupported local commentary.
- Add a "What's Changed" entry for every research pass, even when no substantial updates are found.

## Cadence

- **Routine check:** monthly while the SES is active.
- **Event-driven check:** after UDOT publishes Draft SES materials, Final SES materials, alignment maps, public hearing notices, funding actions, West Haven/Hooper council actions, WFRC plan updates, or significant media coverage.

## Recommended source watchlist

Start with these sources, but do not stop here. The research prompt below explicitly asks AI to cast a wider internet search net before prioritizing sources for publication.

- UDOT SR-177 PublicInput page: `https://udotinput.utah.gov/sr177extension`
- UDOT West Davis / SR-177 project pages
- UDOT right-of-way and acquisition resources
- West Haven City Council agendas, minutes, records, and resolutions
- Hooper City notices, agendas, and public updates
- Weber County planning, assessor, and development records
- WFRC Regional Transportation Plan and TIP updates
- Utah Public Notice portal, when exact city/county links are unavailable
- Standard-Examiner, KSL, and other local reporting
- Contractor/procurement databases
- Public comments, hearing notices, community newsletters, and transportation forums

## AI research prompt template

```text
Research new public information about the SR-177 / West Davis Highway extension from the last update date: YYYY-MM-DD.

Cast a wide net across the internet for new information. Search official sources, local government records, planning documents, meeting agendas/minutes, news coverage, public comments, transportation forums, contractor/procurement databases, and any other publicly available source that may reveal new SR-177 information.

Prioritize official and verifiable sources when deciding what to publish: UDOT, West Haven City, Hooper City, Weber County, WFRC, Utah Public Notice, and state/federal transportation records. Use local media and other internet sources to identify leads, community context, or claims that need verification.

For each new finding:
1. State the claim.
2. Provide the source URL and publication/meeting date.
3. Identify which site page(s) need updates.
4. Identify whether the finding changes timelines, alignment certainty, property-owner guidance, environmental impacts, funding status, governance actions, or source references.
5. Classify the suggested `src/_data/updates.json` entry as `content` or `technical`. If an update includes both content and technical changes, classify it as `content`.
6. Flag uncertain or conflicting information instead of treating it as fact.

Return:
- New findings
- Pages to update
- Suggested citation entries for src/_data/references.json
- Suggested entry for src/_data/updates.json, even if there were no substantial updates
- Items that require human verification before publishing
```

## Update checklist

1. Create or reuse a GitHub issue for the research update.
2. Add any new sources to `src/_data/references.json`.
3. Update affected `.njk` pages with cited claims using `{% cite "id" %}`.
4. Add an entry to `src/_data/updates.json` for every AI research pass, even when no substantial updates were found, and include the correct `category`.
5. Run `npm run build`.
6. Review `/whats-changed.html` to confirm the entry appears in the correct `Content Changes` or `Technical Changes` section and is newest within that section.
7. Open or update a PR; do not merge directly to `main`.

## `updates.json` entry format

Use this shape for each entry:

```json
{
  "date": "2026-04-26T17:43:36-06:00",
  "displayDate": "2026-04-26",
  "category": "content",
  "title": "Short update title",
  "summary": "One- or two-sentence summary of what changed, or state that no substantial updates were found.",
  "pages": [
    { "title": "Overview", "url": "/index.html" }
  ],
  "sourceIds": ["udot-ses-schedule"]
}
```

Field guidance:

| Field | Required | Notes |
|---|---:|---|
| `date` | Yes | Use ISO timestamp format so same-day entries sort correctly. |
| `displayDate` | No | Use `YYYY-MM-DD` for display if the timestamp is too detailed for the public page. |
| `category` | Yes | Use `content` for research, source, disclosure, timeline, guidance, and no-update research checks. Use `technical` for navigation, layout, publishing, accessibility, or infrastructure updates. If both apply, use `content`. |
| `title` | Yes | Keep short and scannable. |
| `summary` | Yes | Mention either the content changes or that no substantial updates were found. |
| `pages` | Yes | Use an empty array only if no pages changed. |
| `sourceIds` | Yes | Use an empty array if no new or relevant source IDs apply. |

## No-update entry example

Use a no-update entry when AI research did not find substantial new information:

```json
{
  "date": "2026-05-26T09:00:00-06:00",
  "displayDate": "2026-05-26",
  "category": "content",
  "title": "Monthly research check found no substantial updates",
  "summary": "AI-assisted research checked official sources, local records, public notices, media coverage, and broader internet sources. No verifiable updates required changes to site content.",
  "pages": [],
  "sourceIds": []
}
```

## Publication rules

- Prefer official records for published factual claims.
- Use media and broad internet sources to identify leads, not as the sole basis for major property-owner guidance.
- If sources conflict, document the conflict and avoid updating the site as if one uncertain claim is settled.
- Do not remove uncertainty language unless an official source resolves it.
- Do not publish legal, property-value, or water-rights guidance without direct citation and cautious wording.
