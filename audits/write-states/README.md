# County retrieval: subsequent write states

## Result

The requested shift from proxy/query lists to written county data was not found in the held revisions examined.

Starting with the three exact 2019/2020/2021 Massachusetts county-selection groups from the functional audit, 94 distinct pages participate. Their export contains 3,828 held revisions, of which 3,444 are at or after that page's first reference to one of the selections: 94 anchor revisions and 3,350 later revisions. A page is the sequencing unit; it is not assumed to be one execution run or one author's work.

After masking request URLs and link labels, the detector found no county-marker candidates, parsed nonempty JSON objects/arrays, numeric table candidates, named comma-separated numeric rows or short-decimal candidates in those 3,444 states. This is a defined lexical/structural scan, not a proof that arbitrary encodings or other output formats contain no data. Request URL query expressions are deliberately not decoded into supposed results.

The follow-up sensitivity pass retains link labels and masks only URLs. It finds one distinct apparent table in `dse~AgentUltimateJuneBB@7`. Manual inspection shows it is an unencoded jq expression containing a county-code list and transformations such as `.usd/10|round/100`, still within a URL. It supplies no evaluated county values. See `results/link_label_sensitivity.jsonl`.

The complete source export is user-reported synthetic. No incident attribution or runtime execution claim is made.

## Gateway chronology

`dse/AgentCountyGateway991` has 51 held revisions, from 2026-06-18 17:18:33 to 21:19:23 UTC, spanning 4 hours and 50 seconds. All 51 contain URL references. The earlier introduction rule counts 1,006 newly introduced references across these revisions, including reintroductions; this is not 1,006 executed fetches.

| Revision | UTC | Written state |
|---|---|---|
| @2 | 17:33:47 | Explicit county selections for 2019, 2020, 2021 through jq and AllOrigins |
| @8 | 18:23:02 | Heading says “Third gateway Corsfix cached success”; body lists alternate routes and output limits |
| @20 | 19:23:35 | Previously used selected query with fragment added |
| @21 | 19:25:01 | Heading claims a robust scan; extraction expressions remain inside URLs |
| @39 | 20:12:07 | Original selected query reintroduced |
| @44 | 20:25:43 | Query parameter order changes; source and selection recur |
| @45 | 20:32:31 | Expressions specify year, code, units and rounding, without evaluated values |
| @50 | 21:07:54 | Expressions contain a literal code-to-county-name mapping and computed yearly fields, still as URL parameters |
| @51 | 21:19:23 | Returns to alternate source URLs and parameters |

The code-to-name mapping in @50 is request-side scaffolding. Its presence does not establish that the USD fields have been populated. Across all 51 revisions, the examined nonlink text contains no evaluated county table or result object. `results/gateway_nonlink_text.txt` contains every masked write state for inspection.

## A data-bearing comparison exists

Elsewhere, `dse~Sector61AllStateValues2027@1` at 2026-06-16 20:01:20 UTC contains 52 named geographic rows with six numeric workforce values per row for 2015–2020: 312 numeric cells. Example:

```
Massachusetts: 926818,944679,964116,976592,988022,987379
```

That is written numeric content associated with named entities and years, unlike a URL asking a service to calculate those values. It is a separate task and is not evidence that the county retrieval succeeded. Its values are not independently authenticated. The full comparison body is retained in `results/numeric_data_comparison.json`.

The all-corpus scan finds 55 distinct named numeric-row lines, including these 52. Finding them shows that the scan can detect this form of written data in this export. It does not establish detector completeness for every possible result format.

## Interpretation

This extends the prior URL audit: the repeated county formulations are followed by further formulations without a detected pivot to stored county results on the participating pages. It supports stalled publication/retry-like behavior at the observable write-state level.

It does not identify which URLs executed, whether a result was obtained but never posted, whether a successful answer was written to an unlinked page, or which route caused any unrecorded result. A later numeric object would be a stronger progress proxy, but could itself be copied or fabricated; first appearance and recurrence fields retain that distinction. In this county subset there are no detected new result candidates to attribute.

The broader corpus contains multiple tasks and written numeric results. The county finding must not be generalized into “the entire corpus contains no progress.”

## Reproduce

Python 3, standard library only. Use the unchanged expanded corpus and `results/introductions.jsonl` from `functional-retry-audit.zip`.

```sh
python test_states.py
python analyze_states.py /path/to/expanded-corpus \
  /path/to/functional-audit/results/introductions.jsonl ./rerun-results
```

Six focused tests passed: detection of numeric county objects, tables and named rows; retention of source-linked data; exclusion of encoded query payloads; exclusion of long timestamp markers as short-decimal results.

Files:

- `analyze_states.py`, `test_states.py`: reproducible implementation and checks.
- `results/summary.json`: counts and exact input hashes.
- `results/anchors.json`: first qualifying reference on each of the 94 pages.
- `results/states.csv`: all participating-page states, including before the anchor.
- `results/focus_states.jsonl`: nonlink text, counts, new candidate content, original revision IDs and timestamps.
- `results/candidate_evidence.jsonl`: globally first candidate text plus participating-page occurrences; includes unrelated-task results and false positives for review.
- `results/link_label_sensitivity.jsonl`: candidates from retaining link labels.
- `results/gateway_nonlink_text.txt`: every gateway revision's masked body.
- `results/numeric_data_comparison.json`: the numeric-data comparison source.

Inputs were read only. No URLs or embedded code were executed. No external search was required to analyze the supplied synthetic records.

Confidence: high in counts and inspected gateway states; medium in generalizing the lexical absence finding to every conceivable county output format. Actual retrieval success remains unknown.
