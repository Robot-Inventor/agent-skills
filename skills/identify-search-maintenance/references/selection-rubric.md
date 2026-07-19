# Rank-led candidate selection rubric

## Normalize the export

Create a CSV with this exact header before using the script:

```csv
url,current_clicks,previous_clicks,current_impressions,previous_impressions,current_position,previous_position
```

`current_*` is the recent period and `previous_*` is its comparison period. Preserve the original Search Console exports as evidence. Do not combine GA4 and Search Console counts in the same columns. The normalized page CSV is only a ranking-loss screen; it cannot establish search demand.

For annual comparison, make a second normalized CSV where `previous_*` is the equivalent period one year earlier. Run the screen on both CSVs, union their candidates, and show which comparison surfaced each URL. If that page did not exist then or the data is unavailable, report `N/A`.

## Default first-pass thresholds

The bundled script selects a page only if all conditions hold:

| Signal                                  |                       Default | Reason                                   |
| --------------------------------------- | ----------------------------: | ---------------------------------------- |
| Previous-period clicks                  |                  at least 100 | Avoid low-volume noise                   |
| Click change                            |                 -20% or worse | Requires a material loss                 |
| Impression change                       |                   within ±25% | Excludes most demand-led losses          |
| Position change                         |                 +0.5 or worse | Requires a measurable rank deterioration |
| Click decline beyond impression decline | at least 10 percentage points | Requires loss beyond demand movement     |

These are screening defaults, not proof. A page can be excluded despite passing them when an independent demand proxy shows demand loss, a one-off event occurred, a competing URL gained the query, or the task is obsolete. A page can be included with explained threshold adjustments only when the report documents why.

## Interpret the metrics

- Position delta is `current_position - previous_position`; a positive number is worse.
- Page-level impressions are not demand: a lower rank can itself lower the page's impressions. Property-wide query impressions can also fall when the whole site loses visibility. Use Google Trends, Keyword Planner, or another documented independent source to assess demand. Compare property-wide (unfiltered-by-page) query impressions only as a corroborating visibility signal, then compare the target URL's rank/clicks separately.
- A stable page-level impression total can hide query-mix movement. Verify individual declined queries before calling the loss rank-led, and inspect pages that gained the query for cannibalization.
- A stable position with a falling CTR is a CTR/SERP case, not a rank-led case.
- A fall in impressions paired with a similar fall in clicks is normally demand-led or obsolescence-led until evidence proves otherwise.
- Search Console average position is an aggregate. Use live Google searches only as a point-in-time confirmation and label locale, device, signed-in state, and date.

## Completion checklist

- [ ] Recent and year-over-year comparisons were both attempted.
- [ ] Every final candidate has page-level metrics, at least three declined historic queries, and property-wide visibility checks for those queries.
- [ ] Every final candidate has independent demand evidence, a URL Inspection/index/canonical/availability health check, and no confirmed cannibalization.
- [ ] Google SERP checks list query, target visibility, competitors, and material SERP features.
- [ ] The report explicitly separates rank-led candidates from demand-led, CTR-only, technical, and insufficient-evidence cases.
- [ ] The report contains diagnoses and maintenance priorities, but no article edits.
