# SR-177 Weber County Extension — Technical Analysis

A static site documenting the proposed SR-177 highway extension into Weber County, Utah. Built with [Eleventy (11ty)](https://www.11ty.dev/) and deployed via GitHub Pages.

**Live site:** https://xeroip.github.io/sr177-weber-analysis

---

## Editorial policy

- **Factual claims must cite a source** in `src/_data/references.json`. Use `{% cite "id" %}` inline.
- **Second-person framing is limited to action-guide content.** Technical report pages should stay neutral and source-backed; property-owner checklists may use direct `you/your` language when it improves clarity.
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

See [AI research update workflow](docs/ai-research-updates.md) for the recurring research prompt, source watchlist, changelog rules, and update checklist.

Key rule: every AI-assisted research pass should add an entry to `src/_data/updates.json`, even when no substantial updates are found.

Quick-start prompt:

```text
Use docs/ai-research-updates.md and perform a recurring SR-177 AI research update.

Last update date: YYYY-MM-DD.

Cast a wide internet search net for new public information about the SR-177 / West Davis Highway extension, then prioritize official/verifiable sources for publication. Identify any needed updates to site content, references, and src/_data/updates.json. If there are no substantial updates, still produce a no-update entry for src/_data/updates.json.

Do not edit files until research is complete. Save a research summary and then recommend exact site changes.
```

---

## License

Code: MIT. Prose: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
