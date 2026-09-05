# ResearchBotZ

**The missing denominator is completed work.**

An offline audit of repetitive retrieval formulations and subsequent wiki write states.

**Provenance: the corpus creator identifies these records as synthetic.** This repository reproduces measurements on that supplied corpus. It does not authenticate a real-world AI breakout, an OpenAI deployment, or the news story discussed alongside it.

## What the records show

The county work produces increasingly elaborate retrieval instructions without a detected transition to written county results on the participating pages.

| Measurement | Result |
|---|---:|
| Held revisions scanned | 14,591 |
| Newly introduced URL references, excluding unchanged carry-forward | 79,771 |
| Introductions repeating an already-seen raw URL | 56,165 |
| Pages carrying the three exact Massachusetts county selections | 94 |
| Later revisions on those pages after their first qualifying reference | 3,350 |
| Detected county-value rows or parsed result objects in those later states | 0 |

These are counts of published references and page states. They are not counts of executed HTTP requests. A missing written result does not establish that no result was obtained elsewhere.

For the exact 2019 selection alone: **859 introductions across 378 revisions and 87 pages, using 50 distinct URLs.** Of those introductions, 809 repeat an already-seen URL exactly.

Changing the page title, timestamp or surrounding prose does not make the requested county selection new.

## One page, four hours

`dse/AgentCountyGateway991` contains 51 revisions from 17:18:33 to 21:19:23 UTC on 18 June 2026. All 51 contain URL references. Together they introduce 1,006 references, including reintroductions.

| Write state | What appears |
|---|---|
| “Corsfix cached success” | Alternate proxy routes and output limits |
| “Final concise” | jq expressions specifying years, fields and rounding |
| “Combined archived official” | County mappings and calculations inside URL parameters |
| Final revision | Alternate source URLs again |

The expressions get more elaborate. Evaluated county values do not appear in the inspected nonlink text.

This export can contain written numeric data: a separate workforce page has **52 named geographic rows × six yearly values = 312 numeric cells**. That is a useful comparison, not a county-retrieval success.

Read the [functional audit](audits/functional/README.md), the [write-state audit](audits/write-states/README.md), or [every gateway write state with links masked](audits/write-states/results/gateway_nonlink_text.txt).

## Reproduce it

Python 3.10 or newer. Standard library only. Run from the repository root:

```sh
python scripts/reproduce.py
```

The script checks the published file hashes, expands the five source files, verifies their original SHA-256 checksums, runs 18 focused tests, reruns both audits and byte-compares every regenerated result file with the frozen bundles. Generated work stays in `.work/`.

For manual verification, `data/SHA256SUMS` hashes the **expanded files**, not the gzips. `SHA256SUMS` at the repository root hashes the published repository artifacts.

## How the grouping works

Group by **resource + requested result + operation**. Keep transport variants separately inspectable: proxy chain, scheme, port, fragments, output limits, encoding and original URL spelling.

The three years remain separate selections. Request-side jq code is not promoted into a returned JSON object. Subsequent write states are checked for data-bearing content, with source references and candidate text retained for inspection.

The detectors are explicit heuristics. They do not recognize every possible output encoding. The reports document ambiguous wrappers, link-label sensitivity, copied content and the absence of linked external responses.

## What this does not establish

No runtime trace establishes missing backoff, race conditions, an infinite loop, exponential growth or the cause of a failed fetch. The data also does not establish universal task failure, company intent, investor response or regulatory effects.

The supported finding is narrower: **repeated county retrieval formulations, followed by further formulations, without a detected county-data write state on the participating pages.**

Calling uncontrolled repetition “persistence” and an expanding footprint “coordination” can turn a failure into a capability story. That is the argument motivating the audit. The tables above are the measurements. Keep the two distinguishable.

## Files

- [`data/`](data/): five compressed source files and their expanded-file checksums.
- [`audits/`](audits/): readable reports, scripts, tests and compact result summaries.
- [`bundles/functional-retry-audit.zip`](bundles/functional-retry-audit.zip): complete functional-grouping results, including every counted reference.
- [`bundles/county-write-state-audit.zip`](bundles/county-write-state-audit.zip): complete subsequent-state results and comparison data.
- [`PROVENANCE.md`](PROVENANCE.md): source status and publication boundaries.

The existing MIT license is retained. No corpus URLs or embedded programs are executed by the audit.
