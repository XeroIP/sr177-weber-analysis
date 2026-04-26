# SR-177 Weber County Extension — Technical Analysis

A static site documenting the proposed SR-177 highway extension into Weber County, Utah. Built with [Eleventy (11ty)](https://www.11ty.dev/) and deployed via GitHub Pages.

**Live site:** https://xeroip.github.io/sr177-weber-analysis

---

## Editorial policy

- **Factual claims must cite a source** in `src/_data/references.json`. Use `{% cite "id" %}` inline.
- **No second-person framing.** Write for all properties along 5100 West in Weber County, not a specific address.
- **No risk-color coding.** Status tags (`active`, `study`, `future`) are acceptable; threat-level framing is not.
- **No editorialization.** Remove any claim not directly traceable to `initial-research.md` and a source in `references.json`.
- **Phase-only grouping.** Phase 3: 1800 N → 4000 S (West Haven). Phase 4: 4000 S → Box Elder line.

---

## Development

**Prerequisites:** Node.js 20+ (see `.nvmrc`)

```bash
npm install
npm run dev      # local dev server at http://localhost:8080
npm run build    # production build to _site/
npm run clean    # remove _site/
```

---

## Project structure

```
src/
  _data/
    references.json   # references — single source for numbering and citation links
    updates.json      # What's Changed entries, sorted newest-first at render time
    nav.json          # ordered nav items
    site.json         # site metadata
  _includes/
    layouts/          # base.njk, page.njk
    partials/         # head.njk, nav.njk, footer.njk, page-nav.njk
  assets/
    css/
      main.css        # all styles
      print.css       # print-specific overrides
  *.njk               # content pages + sitemap + 404
```

---

## Adding a reference

1. Add an entry to `src/_data/references.json` with a unique kebab-case `id`.
2. Use `{% cite "your-id" %}` in the content page.
3. The citation number is assigned automatically by position in the array.

---

## Periodic AI-assisted research updates

Use this workflow when periodically asking AI to search for new SR-177 information and update the site.

### Cadence

- **Routine check:** monthly while the SES is active.
- **Event-driven check:** after UDOT publishes Draft SES materials, Final SES materials, alignment maps, public hearing notices, funding actions, West Haven/Hooper council actions, WFRC plan updates, or significant media coverage.

### Recommended source watchlist

- UDOT SR-177 PublicInput page: `https://udotinput.utah.gov/sr177extension`
- UDOT West Davis / SR-177 project pages
- UDOT right-of-way and acquisition resources
- West Haven City Council agendas, minutes, records, and resolutions
- Hooper City notices, agendas, and public updates
- Weber County planning, assessor, and development records
- WFRC Regional Transportation Plan and TIP updates
- Utah Public Notice portal, when exact city/county links are unavailable
- Standard-Examiner, KSL, and other local reporting

### AI research prompt template

```text
Research new public information about the SR-177 / West Davis Highway extension from the last update date: YYYY-MM-DD.

Focus on official and verifiable sources first: UDOT, West Haven City, Hooper City, Weber County, WFRC, Utah Public Notice, and state/federal transportation records. Use local media only to identify leads or community context.

For each new finding:
1. State the claim.
2. Provide the source URL and publication/meeting date.
3. Identify which site page(s) need updates.
4. Identify whether the finding changes timelines, alignment certainty, property-owner guidance, environmental impacts, funding status, governance actions, or source references.
5. Flag uncertain or conflicting information instead of treating it as fact.

Return:
- New findings
- Pages to update
- Suggested citation entries for src/_data/references.json
- Suggested entry for src/_data/updates.json
- Items that require human verification before publishing
```

### Update checklist

1. Create or reuse a GitHub issue for the research update.
2. Add any new sources to `src/_data/references.json`.
3. Update affected `.njk` pages with cited claims using `{% cite "id" %}`.
4. Add an entry to `src/_data/updates.json` with:
   - `date` in ISO timestamp format, such as `2026-04-26T17:43:36-06:00`, so same-day updates sort correctly
   - optional `displayDate` in `YYYY-MM-DD` format
   - short `title`
   - concise `summary`
   - `pages` array with changed page titles/URLs
   - `sourceIds` array for the most relevant citations
5. Run `npm run build`.
6. Review `/whats-changed.html` to confirm the newest entry appears on top.
7. Open or update a PR; do not merge directly to `main`.

---

## License

Code: MIT. Prose: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
