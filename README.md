# ResearchBotZ

**A story of the missing denominator.**

An offline audit of repeated retrieval instructions and the wiki revisions that followed.

Source: [Collusion Wiki’s published archive](https://collusion.wiki/explorer/download.html).

## What the records show

**94 county pages. 3,350 subsequent revisions. Zero county-result data found.**

The retrieval instructions just kept accumulating.

| Measurement                                                    |  Count |
| -------------------------------------------------------------- | -----: |
| Revisions scanned                                              | 14,591 |
| URL-reference introductions, excluding unchanged carry-forward | 79,771 |
| Introductions repeating an already-seen URL exactly            | 56,165 |
| Pages referencing the three Massachusetts county selections    |     94 |
| Subsequent revisions on those pages                            |  3,350 |
| Detected county-value rows or parsed result objects            |  **0** |

For the exact 2019 selection: **859 introductions. 50 distinct URLs.**

## One page, four hours

On 18 June 2026, `dse/AgentCountyGateway991` accumulated **51 revisions and 1,006 URL-reference introductions** over roughly four hours.

“Corsfix cached success” supplies proxy alternatives. “Final concise” supplies jq expressions. “Combined archived official” embeds calculations in URLs. The final revision supplies even more URLs.

**The instructions grow more elaborate, yet county values never appear in the inspected text outside the links.**

A separate workforce page contains **312 numeric cells**. Written results survive in this export.

Read the [functional audit](audits/functional/README.md), [write-state audit](audits/write-states/README.md), or [gateway text with links masked](audits/write-states/results/gateway_nonlink_text.txt).

## Then reproduce it

Python 3.10+, standard library only. From the repository root:

```sh
python scripts/reproduce.py
```

One command verifies hashes and checksums, runs **18 tests**, reruns both audits, and byte-compares regenerated results against frozen outputs. Generated files stay in `.work/`. You're welcome.

`data/SHA256SUMS` covers expanded sources; root `SHA256SUMS` covers published artefacts. No corpus URLs or embedded programs are executed.

## Method

References are grouped by **resource + requested result + operation**, preserving transport variants for inspection and treating each year separately. Request-side code does not count as returned data.

**Repeated instructions. Thousands of subsequent revisions. No county results found.**

Source data lives in [`data/`](data/), reports in [`audits/`](audits/), and complete results in [`bundles/`](bundles/). See [`PROVENANCE.md`](PROVENANCE.md) for source details.

And here’s how I’ll explain it to my 11-year-old daughter: AI was supposed to find facts. It kept posting links and instructions for finding answers. We checked thousands of updates on 94 pages and found none of the answers they were looking for. Looking busy isn’t the same as getting your homework done.

The existing MIT license is retained.
