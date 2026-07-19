---
name: identify-search-maintenance
description: Identify and diagnose organic-search articles that need maintenance. Use when asked to find pages whose organic traffic declined mainly from ranking loss rather than search-demand decline, analyze Search Console or GA4 data across recent and year-over-year periods, prioritize a maintenance backlog, or compare target pages with current Google results. Do not use this skill to edit article content.
---

# Identify Search Maintenance

Find pages that merit search-maintenance work, with evidence that separates rank-driven losses from changes in demand. The deliverable is a ranked investigation backlog and diagnosis; it is never an article rewrite or publishing task.

## Scope and guardrails

- Confirm the property, traffic channel, dates, locale/device, and whether Google must be inspected through the user's signed-in Chrome session.
- Use both recent comparison (normally the latest 3 months vs. the preceding 3 months) and a year-over-year comparison (normally the same recent 3 months one year earlier). End periods on the latest Search Console date that is complete enough to compare, use equal day counts and comparable weekday mix, and state any unavailable baseline as `N/A`, never as zero.
- Fix the Search Console search type, country, device, property scope, canonical-URL handling, and any brand-query exclusion across each comparison. Record GA4 timezone, Organic Search channel definition, and landing-page URL normalization.
- Treat a page as a candidate only after checking page-level **and** query-level Search Console data. GA4 is corroborating traffic evidence, not a substitute for query and rank data.
- Do not attribute a loss to rankings from clicks alone. URL-filtered and property-wide Search Console impressions are affected by the site's own visibility and are not standalone demand measures. Check an independent demand proxy (for example Google Trends for the query/topic, Keyword Planner where available, or a documented market-data source), then use property-wide query data only as corroboration. Also check URL/query rank changes, cannibalization, and live SERP composition.
- Do not alter CMS content, metadata, internal links, or publish settings. If the user asks for changes, finish this investigation first and obtain a separate article-update scope.

## Workflow

### 1. Collect comparable evidence

1. Export Search Console performance by **page** for the two period pairs. Prefer an export/CSV over manually paging a truncated table.
2. Retain clicks, impressions, CTR, and average position for each period. Record filters, property, and export dates.
3. Obtain GA4 organic-search landing-page sessions or views for the same dates when available. Note that GA4 and Search Console count different things.
4. Normalize both the recent-pair and year-over-year page exports to the columns in [selection-rubric.md](references/selection-rubric.md). Run the bundled filter on each, take the union of the two candidate lists, and label the comparison(s) that surfaced each URL. A page that only passes one comparison still needs the full evidence checks in both.

```powershell
python "<skill-directory>/scripts/select_rank_led_candidates.py" normalized-pages.csv --format markdown
```

Replace `<skill-directory>` with the directory containing this `SKILL.md`. Use the script to screen candidates, not to make the final decision. Tune its thresholds only if the report explains why.

### 2. Separate causes before selecting pages

Classify each materially declining page into one of these mutually exclusive buckets:

| Bucket                               | Evidence                                                                                 | Action                                                                                 |
| ------------------------------------ | ---------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| Rank-led maintenance candidate       | Clicks materially down; impressions broadly stable; average position/query ranks worsen  | Investigate and prioritize                                                             |
| Demand/obsolescence decline          | Impressions and clicks fall together, or the task/query has ended                        | Exclude from the rank-led list                                                         |
| CTR/SERP change                      | Position broadly stable but CTR falls; SERP features or title/snippet changes explain it | Keep separate; do not call it rank-led                                                 |
| Technical/indexing issue             | Indexing, canonical, rendering, or availability evidence                                 | Escalate separately                                                                    |
| Cannibalization/internal competition | Another site URL gained the same query or intent                                         | Exclude from this content-maintenance list; route for consolidation/targeting decision |
| Insufficient evidence                | Low volume or no comparable baseline                                                     | Do not force into the top 10                                                           |

For every selected URL, verify at least three previously valuable declined queries. For each query, collect three views with identical search type/country/device/date filters: (a) the target URL's query metrics and position, (b) the **whole property** query metrics without a page filter, and (c) an independent demand proxy. Treat (c) as the demand evidence; use (b) only to understand the site's overall visibility. Use year-over-year data to catch longer-running changes. Check whether another URL in the property gained the same query; classify confirmed cannibalization in its own exclusion bucket. If the query mix changed, say so.

Before retaining a content-maintenance candidate, perform a minimum health check: URL Inspection/index status, user-selected canonical, HTTP availability, and rendered-page accessibility. Classify a failing page as a technical/indexing issue instead of diagnosing an editorial gap.

### 3. Diagnose each selected page in Google

When the user specifies Chrome or Google, use the Chrome browser, not a general web-search backend. For each selected URL:

1. Search at least three declined, historically valuable queries in Google, using the required locale/device context where possible.
2. Capture the target URL's visible rank or absence, the top competing URLs, and material SERP features (AI Overview, official result, video carousel, PAA, news, forums, etc.). Use fresh tabs and do not change account or site settings.
3. Compare the target and the leading pages on search intent, freshness, direct answer quality, task completion, factual completeness, first-party evidence, visual/media support, structure, and trust signals. Base observations on actual page content; distinguish observed facts from inference.
4. Identify the gap to investigate, not the edit itself. Examples: outdated UI steps, missing current constraints, poor intent match, weak original evidence, or a SERP now dominated by official sources.

If parallel agents are available, assign no more than two pages to each agent. Require each agent to return the period metrics, three or more queries, Google competitors, SERP features, observed content gaps, exclusions, and source URLs. Consolidate only after all agents return evidence.

### 4. Produce the maintenance report

Create or append to `report.md`; preserve earlier findings unless the user asks to replace them. Use this structure:

1. Scope, dates, data sources, filters, and limitations.
2. Selection method and explicit rank-led thresholds.
3. A prioritized table of up to the requested number of rank-led pages (default 10): URL, recent metrics, year-over-year metrics, property-wide query-demand evidence, ranking evidence, priority, and confidence. If fewer pages meet the evidence threshold, report fewer and explain the shortfall.
4. Per-page diagnosis: three or more declined queries, current Google competitors/SERP observations, and content gaps to investigate.
5. Excluded near-misses with the evidence for demand decline, obsolete intent, CTR-only loss, technical issue, cannibalization, or insufficient data.
6. A separate follow-up queue for work that needs a technical or editorial decision.

Before delivery, verify that every page in the final rank-led list has stable-enough independent demand evidence, a documented query-level rank deterioration, and a passing health check. Never fill a quota with demand-led losses.

## Resources

- [selection-rubric.md](references/selection-rubric.md): normalization schema, default thresholds, and report checklist.
- `scripts/select_rank_led_candidates.py`: deterministic first-pass filter for normalized Search Console page exports.
