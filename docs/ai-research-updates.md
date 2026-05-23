# AI Research Update Workflow

Use this workflow when an LLM agent periodically researches public SR-177 / West Davis Highway information and proposes site updates. The agent must treat this document as an operating contract, not a loose suggestion list.

## Required inputs

The operator or requesting prompt must provide these values before a research pass starts:

| Input | Required | How to choose it |
|---|---:|---|
| `last_research_date` | Yes | Use the most recent `content` entry in `src/_data/updates.json` that represents an AI-assisted research pass. Do not use purely `technical` entries. |
| `run_date` | Yes | Use the current local date and time in ISO timestamp format. |
| `issue_number` | Yes | Create or reuse a GitHub issue before editing site files. |
| `research_scope` | No | Use `routine monthly check` unless the request names a triggering event, source, or page. |

If any required input is missing, stop and ask for it or derive it from the repository when possible. Do not guess dates.

## Goals

- Find new public information about SR-177 / West Davis Highway since `last_research_date`.
- Check whether existing high-risk claims are now stale, contradicted, or overspecified.
- Update affected site pages only when claims are verifiable and cited.
- Preserve uncertainty instead of overstating rumors, early reports, public comments, or unsupported local commentary.
- Add a `What's Changed` entry for every research pass, even when no substantial updates are found.
- Leave a durable research record so a human can audit what was checked and why each publishing decision was made.

## Cadence

- **Routine check:** monthly while the State Environmental Study is active.
- **Event-driven check:** after UDOT publishes Draft SES materials, Final SES materials, alignment maps, public hearing notices, funding actions, West Haven/Hooper council actions, WFRC plan updates, or significant media coverage.

## Source search plan

Start with the watchlist below, then cast a wider internet search net. Local media, public comments, social posts, forums, and contractor databases may identify leads, but major site claims need official or directly verifiable support.

### Priority sources for publication

- UDOT SR-177 PublicInput page: `https://udotinput.utah.gov/sr177extension`
- UDOT West Davis / SR-177 project pages
- UDOT right-of-way and acquisition resources
- UDOT construction, funding, procurement, and public involvement notices
- West Haven City Council agendas, minutes, packets, records, and resolutions
- Hooper City notices, agendas, public updates, planning records, and council records
- Weber County planning, assessor, parcel, development, and commission records
- WFRC Regional Transportation Plan, TIP, board materials, and amendment records
- Utah Public Notice portal, when exact city/county links are unavailable
- State or federal transportation, environmental, funding, and procurement records

### Lead sources that require stronger verification

- Standard-Examiner, KSL, and other local reporting
- Contractor/procurement databases
- Public comments, hearing comments, letters to the editor, newsletters, transportation forums, and social posts
- Search result snippets, AI summaries, map annotations, and third-party aggregators

Do not publish a major factual change from a lead source alone when it affects alignment certainty, property-owner guidance, legal exposure, right-of-way expectations, funding status, construction timing, or environmental impacts.

## Required stale-claim sweep

Every research pass must review existing site claims in these categories, even if no new source appears:

- Timeline, schedule, public-comment period, hearing, and milestone claims.
- Alignment certainty, phase boundaries, maps, and corridor descriptions.
- Property-owner guidance, right-of-way acquisition, relocation, corridor preservation, and legal-process language.
- Funding status, procurement status, construction status, and project phasing.
- Environmental, noise, wetland, agricultural, floodplain, traffic, and utility-impact statements.
- West Haven, Hooper, Weber County, WFRC, and UDOT governance actions.
- `as of`, `currently`, `planned`, `expected`, `likely`, `may`, and `could` language that may have aged badly.

If a claim cannot be confirmed by current sources, preserve or add uncertainty language. Do not make it sound more certain.

## Date claims added to site content

When adding or updating factual data on site pages, include the relevant date when it helps readers judge freshness, sequence, or authority. This is separate from the `src/_data/updates.json` entry that feeds the `What's Changed` page.

Use dates for:

- Meeting actions, agenda items, public notices, public hearings, comment periods, resolutions, and votes.
- Construction, procurement, funding, environmental-study, and right-of-way milestones.
- Source status phrases such as `as of`, `last verified`, `published`, `approved`, `adopted`, `scheduled`, or `expected`.
- Time-sensitive guidance, especially property-owner, alignment, funding, legal-process, and schedule statements.

Do not force a date into evergreen explanatory text where it would add clutter or imply false precision. Prefer the date attached to the official record, meeting, packet, notice, publication, or last verification rather than the date the AI research pass found it.

## AI research prompt template

```text
Use docs/ai-research-updates.md as the controlling workflow.

Research new public information about the SR-177 / West Davis Highway extension since last_research_date: YYYY-MM-DD.

Run date: YYYY-MM-DDTHH:MM:SS-06:00
GitHub issue: #NN
Research scope: routine monthly check or event-driven reason

Before researching, read src/_data/updates.json and existing relevant site pages. If the requested research window overlaps an existing AI-assisted research entry, compare findings against current site content and mark overlap-period items as new, already reflected, stale/needs wording update, conflicting, or not safe to publish. Do not recommend a duplicate What's Changed entry for already reflected findings unless source verification, wording, citations, or page content needs to change.

Cast a wide net across the internet for new information. Search official sources, local government records, planning documents, meeting agendas/minutes/packets, news coverage, public comments, transportation forums, contractor/procurement databases, and any other publicly available source that may reveal new SR-177 information.

Prioritize official and verifiable sources when deciding what to publish: UDOT, West Haven City, Hooper City, Weber County, WFRC, Utah Public Notice, and state/federal transportation records. Use local media and other internet sources to identify leads, community context, or claims that need verification.

Also perform the stale-claim sweep from docs/ai-research-updates.md. Check whether existing timeline, alignment, property-owner guidance, funding, governance, and environmental claims need softer wording, updated citations, or removal.

For each finding:
1. State the claim.
2. Provide the exact source URL and publication, meeting, agenda, packet, or last-verified date.
3. Classify source strength as official record, direct public record, media report, public comment, third-party database, or unverified lead.
4. Identify which site page(s) need updates.
5. Identify whether the finding changes timelines, alignment certainty, property-owner guidance, environmental impacts, funding status, governance actions, source references, or site structure.
6. Identify what date, if any, should appear with the data added to the site page. Keep this separate from the What's Changed entry date.
7. Classify the suggested src/_data/updates.json entry as content or technical. If an update includes both content and technical changes, classify it as content.
8. Flag uncertain or conflicting information instead of treating it as fact.
9. Mark whether a human has manually opened and verified the cited source before publishing.

Return these sections:
- Executive summary
- Inputs used
- Sources checked
- New findings
- Overlap-period findings already reflected or needing correction
- Existing claims that may be stale
- Pages to update
- Suggested citation entries for src/_data/references.json
- Suggested src/_data/updates.json entry, even if no substantial updates were found
- Claims not safe to publish yet
- Human verification checklist
- Exact file changes recommended

Export the findings to a self-contained Markdown file named sr177-ai-research-findings-YYYY-MM-DD.md, using the run date. The file must stand alone outside this chat and repository. Include prompt inputs, research scope, search methodology, exact source URLs, source dates, source-strength classifications, new findings, already reflected findings, stale-claim sweep results, rejected or deferred leads with reasons, conflicts, publication recommendations, suggested JSON entries, human verification status, and exact recommended file changes. If artifact or file export is unavailable, return the complete Markdown file content in the response with the filename clearly stated.
```

## Required research record

Before editing publication files, produce a research summary in the GitHub issue, PR body, or another durable review location. The summary must include:

- Research date and `last_research_date` used.
- Search terms and source categories checked.
- Exact URLs opened, with publication, meeting, agenda, packet, or last-verified dates when available.
- New findings and whether each is publishable.
- Existing claims reviewed during the stale-claim sweep.
- Leads rejected or deferred, with the reason.
- Conflicts between sources, if any.
- Human verification items that remain incomplete.

The preferred durable record is the self-contained Markdown export from the prompt template: `sr177-ai-research-findings-YYYY-MM-DD.md`. The Markdown file must be complete enough for a reviewer to audit the research without reading the chat transcript. Creating this research report is allowed during the research pass; editing publication files is not allowed until research and source verification are complete.

Do not update the site from an LLM-only research summary unless a human or tool-assisted browser check has opened and verified the cited sources.

## Update checklist

1. Create or reuse a GitHub issue for the research update.
2. Complete the self-contained Markdown research record before editing site files.
3. Add any new sources to `src/_data/references.json` with stable, unique, kebab-case IDs.
4. Prefer exact document, agenda, meeting packet, notice, or article URLs over broad landing pages when the exact URL is available.
5. Update affected `.njk` pages with cited claims using `{% cite "id" %}`.
6. Add source, event, meeting, publication, or `as of` dates to the site-page content when the data is time-sensitive or date-specific.
7. Keep cautious wording for preliminary, uncertain, conflicting, or lead-only information.
8. Add an entry to `src/_data/updates.json` for every AI research pass, even when no substantial updates were found, and include the correct `category`. This is the What's Changed record and does not replace dates in the page content itself.
9. Verify every `sourceIds` value in `src/_data/updates.json` exists in `src/_data/references.json`.
10. Review `src/references.njk` and any source-page date language if reference freshness changed.
11. Run `npm run build`.
12. Review `/whats-changed.html` to confirm the entry appears in the correct `Content Changes` or `Technical Changes` section and is newest within that section.
13. Open or update a PR; do not merge directly to `main`.

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

Validation note: `sourceIds` are rendered with reference numbers on `/whats-changed.html`. Unknown IDs render as `?`, so verify them manually before publishing.

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

Use `pages: []` and `sourceIds: []` only when the research pass found no content changes and no specific source became more relevant. The public update should still explain what kinds of sources were checked.

## Publication rules

- Prefer official records for published factual claims.
- Use media and broad internet sources to identify leads, not as the sole basis for major property-owner guidance.
- If sources conflict, document the conflict and avoid updating the site as if one uncertain claim is settled.
- Do not remove uncertainty language unless an official source resolves it.
- Do not publish legal, property-value, or water-rights guidance without direct citation and cautious wording.
- Do not publish AI-generated citations, summaries, or search-result snippets as sources.
- Do not cite inaccessible, paywalled, or login-gated material unless the public page clearly explains the access limitation.
- Do not treat conceptual exhibits as official maps or parcel determinations.
- Do not edit unrelated pages or perform broad rewrites during a routine research pass.
