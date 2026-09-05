# County retrieval: four hours, more instructions, no answers

## Result

**94 pages. 3,350 follow-up revisions. No county results found.**

This audit follows three exact Massachusetts county selections—2019, 2020 and 2021—from their first appearance through every available later revision on the participating pages.

| Scope                                                | Count |
| ---------------------------------------------------- | ----: |
| Participating pages                                  |    94 |
| Total revisions on those pages                       | 3,828 |
| First qualifying references                          |    94 |
| Later revisions                                      | 3,350 |
| States checked from the first reference onward       | 3,444 |
| Result candidates after masking URLs and link labels | **0** |

The scan checks for county names and codes, nonempty JSON objects and arrays, numeric tables, named numeric rows and short decimals.

A second pass keeps link labels visible. It finds one apparent table in `dse~AgentUltimateJuneBB@7`: a jq expression inside a URL, containing county codes and calculations such as `.usd/10|round/100`. Inspection confirms that it contains instructions, not evaluated county values. See [the sensitivity results](results/link_label_sensitivity.jsonl).

Source: [Collusion Wiki’s published archive](https://collusion.wiki/explorer/download.html).

## One page, four hours

`dse/AgentCountyGateway991` records **51 revisions in four hours and 50 seconds**, from 17:18:33 to 21:19:23 UTC on 18 June 2026.

Every revision contains URLs. Together they introduce **1,006 references**, including reintroductions.

| Revision | UTC      | What the page actually contains                                        |
| -------- | -------- | ---------------------------------------------------------------------- |
| @2       | 17:33:47 | County selections for 2019–2021 through jq and AllOrigins              |
| @8       | 18:23:02 | “Corsfix cached success”: alternate routes and output limits           |
| @20      | 19:23:35 | A previously used query with a fragment added                          |
| @21      | 19:25:01 | A claimed “robust scan,” with extraction expressions still inside URLs |
| @39      | 20:12:07 | The original selected query again                                      |
| @44      | 20:25:43 | The same source and selection with reordered parameters                |
| @45      | 20:32:31 | Expressions specifying years, codes, units and rounding                |
| @50      | 21:07:54 | County-name mappings and yearly calculations inside URL parameters     |
| @51      | 21:19:23 | More alternate source URLs and parameters                              |

**The headings announce progress. The bodies supply more instructions.**

Even @50’s county-name mapping contains no evaluated county values. Across all 51 revisions, the inspected text outside links contains no county-result table or object.

[Read every gateway revision with links masked.](results/gateway_nonlink_text.txt)

## The export does contain answers to another task

A separate workforce page, `dse~Sector61AllStateValues2027@1`, contains **52 geographic rows × six yearly values = 312 numeric cells**.

For example:

```text
Massachusetts: 926818,944679,964116,976592,988022,987379
```

These are written values for 2015–2020. The county pages contain instructions for obtaining values.

Across the full corpus, the scan finds **55 distinct named numeric rows**, including these 52. Written numeric data survives in the export, and the detector recognises it.

The [comparison file](results/numeric_data_comparison.json) preserves the full workforce entry. This is a separate task; its figures have not been independently verified.

## What the finding means

**The county pages keep publishing ways to get the answer without publishing the answer itself.**

This extends the functional audit beyond repeated URLs: it checks what was written next. The observed sequence is more retrieval instructions, more revisions, and no detected county-result output.

The unit tracked is a page, which may contain contributions from multiple agents or runs. The audit examines published text; it does not reconstruct network execution or answers delivered elsewhere. Its detectors cover the documented formats, not every possible encoding.

The finding concerns these county selections. Other tasks in the archive contain written results.

## Reproduce it

Python 3.10+, standard library only. From this audit directory, use the expanded corpus and the functional audit’s `results/introductions.jsonl`:

```sh
python test_states.py
python analyze_states.py /path/to/expanded-corpus \
  /path/to/functional-audit/results/introductions.jsonl ./rerun-results
```

The six tests cover county objects, tables, named numeric rows, records containing source URLs, encoded request payloads and timestamp exclusions.

## Evidence files

| File                                                                   | Contents                                                                  |
| ---------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| [`summary.json`](results/summary.json)                                 | Counts and input hashes                                                   |
| [`anchors.json`](results/anchors.json)                                 | First qualifying reference on each page                                   |
| [`states.csv`](results/states.csv)                                     | All participating-page revisions, including earlier states                |
| [`focus_states.jsonl`](results/focus_states.jsonl)                     | Masked text, candidate counts, changes, revision IDs and timestamps       |
| [`candidate_evidence.jsonl`](results/candidate_evidence.jsonl)         | Candidate text and occurrences, including other tasks and false positives |
| [`link_label_sensitivity.jsonl`](results/link_label_sensitivity.jsonl) | Results from the pass retaining link labels                               |
| [`gateway_nonlink_text.txt`](results/gateway_nonlink_text.txt)         | Every masked gateway revision                                             |
| [`numeric_data_comparison.json`](results/numeric_data_comparison.json) | The workforce comparison entry                                            |

Implementation: [`analyze_states.py`](analyze_states.py). Tests: [`test_states.py`](test_states.py).

Inputs were read only. No source URLs or embedded code were executed.
