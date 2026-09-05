# Functional repetition audit

The user describes this corpus as synthetic. This is an offline analysis of its recorded page content, not evidence about a real incident or a count of executed HTTP requests.

## Findings

Repetition remains substantial after grouping by resource, requested result and operation. The earlier count of byte-identical adjacent page bodies does not measure functional repetition and cannot be used to reject retry loops.

All 14,591 revisions were scanned. There were 113,031 distinct-within-revision lexical URL occurrences. Removing 33,260 URLs carried unchanged from the immediately preceding held revision leaves 79,771 newly introduced references. These include first-held-revision references, references copied to other pages, and references removed and subsequently reintroduced. They are not necessarily attempts.

The declared-operation grouping produces 18,802 groups, of which 5,212 recur. There are 60,969 references beyond the first per group, including alternatives within the same revision. Independently of grouping, 56,165 introductions repeat an already encountered raw URL. These global counts do not establish which process, if any, executed a reference.

### Exact requested selections

All three rows below target `www.sec.gov/files/county.json`, request a jq selection of records whose code starts with `us-ma-`, and use the `retrieve-and-transform` operation. The year remains part of the requested result, so these are three separate groups.

| Year | Introductions | Distinct revisions | Pages | Distinct raw URLs | Transport descriptors | Reintroductions of an already-seen raw URL |
|---|---:|---:|---:|---:|---:|---:|
| 2019 | 859 | 378 | 87 | 50 | 29 | 809 |
| 2020 | 841 | 348 | 85 | 54 | 31 | 787 |
| 2021 | 823 | 338 | 81 | 54 | 30 | 769 |

The exact 2019 expression is `[.regCF_county_2019[]|select(.code|startswith("us-ma-"))]`. Each group's recorded span is 2026-06-18 15:16:47 through 2026-06-19 00:42:40 UTC. Counts of pages/revisions cannot be added across groups because they overlap.

Group IDs: 2019 `32e56f9e50c1bfc275de`; 2020 `e4441274ebcea72e7b1a`; 2021 `d9818687056ba13062a7`.

### Successive formulations on one page

For the 2019 group on `dse/AgentCountyGateway991`:

| Revision reference | June 18 UTC | Recorded change | Attached event |
|---|---|---|---|
| dse~AgentCountyGateway991@2 | 17:33:47 | jq service wrapping AllOrigins wrapping the source URL | save |
| dse~AgentCountyGateway991@20 | 19:23:35 | Same URL and selection, with `#x` appended | save |
| dse~AgentCountyGateway991@39 | 20:12:07 | Original URL reintroduced exactly | save |
| dse~AgentCountyGateway991@44 | 20:25:43 | Same selection and route; `jq` and `url` query parameters reordered | save |

These are successive introductions for this group on this page, not adjacent revisions or a demonstrated single execution run. No external response is attached to these records. Revision @8 at 18:23:02 contains the line “Third gateway Corsfix cached success”; that text does not supply the returned county records or identify a verified response for this sequence. A page-save event establishes a recorded page write, not a successful retrieval of its links.

## Grouping and transport rules

- Resource: lowercase hostname plus exact path. Case changes in paths, double slashes, encoded paths and different hostnames are not silently merged.
- Requested result: remaining query parameters and exact decoded transformation expressions. Years and filters are retained. Unknown parameters are retained; there is no general removal of digits or timestamps from text.
- Operation: retrieval reference, retrieval with transformation, rendered retrieval, wiki action, or the recognized counter mutation reference. These categories describe URL formulations, not inferred execution.
- Separate transport descriptor: schemes, authorities/ports, nested wrapper route, wrapper options, fragments, presumed delivery options and presumed nonce parameters. Raw URL spelling is also retained separately, including encoding and query order changes that a descriptor may coalesce.
- `max_tokens`, `format`, `output`, `callback` and similar parameters are preserved as delivery variants. This does not assert identical returned content. Nonce-like keys are likewise preserved, not deleted. Both key lists appear in summary.json.
- Known wrapper syntax is decoded offline. Wrapper behavior is not verified. Unresolved wrappers and shorteners stay unresolved; ambiguous wrapper query scope is flagged. No corpus URL was fetched.

The groups are candidate equivalence classes for declared operations, with transport and raw-wire variants available for inspection. They are not proof of server-side equivalence. Transport descriptor counts include options and nonce values; they are not counts of proxy services.

## What happened after each formulation?

The structured event schema contains no `status_code`, `http_status`, `response_body`, `response_hash`, `request_url`, `response_url` or `tool_result` fields. Its 14,591 save records do not establish retrieval success. Its 101 probe records all have `success_observed=false`; this is not a linked outcome for every retrieval formulation. The 5,217 deletes and four reverts have successful wiki-action observations, not successful external data retrievals.

The script extracts 2,209 newly appearing lines containing outcome-like words after masking URLs. They are candidates for review, not validated responses. A heading containing “correct” or “success” does not establish progress. This lexical extraction is incomplete: it can miss numeric-only answers and unfamiliar wording. Consequently the audit records external outcomes as unknown; it does not report zero real successes or assert that every reference failed.

What is established is repeated publication of unchanged requested selections, including exact URL reintroductions and variants in routing or spelling. This is compatible with redundant retry/fan-out behavior. This export does not identify runtime scheduling, race conditions, backoff timing or progress per executed request. Establishing those would require an execution trace connecting a request to its response, not a controlled experiment about intent.

## Reproduce

Requires Python 3, standard library only. Place the five expanded source files in one directory under their canonical names. Their SHA256 values are recorded in results/summary.json and match the supplied SHA256SUMS. Source files are not duplicated in this archive.

```sh
python test_grouping.py
python analyze.py /path/to/expanded-corpus ./rerun-results
```

Twelve focused tests cover year/selection separation, retained unknown parameters, path distinctions, transport changes, nested wrappers, unresolved targets and operation separation. All passed.

Outputs:

- `results/groups.csv`: inspectable aggregate table.
- `results/groups.json`: aggregates including sample revision references.
- `results/introductions.jsonl`: every counted reference, original URL, group, transport descriptor, revision, timestamp, label and attached event types.
- `results/claim_candidates.jsonl`: candidate outcome language with source references.
- `results/summary.json`: totals, classification options and input hashes.

The URL tokenizer is lexical. Literal whitespace, quotes or brackets end a token; malformed and unconventional URL syntax may therefore be missed or split. Ordering within one revision is not inferred. Cross-page timestamp order is used only for deterministic global recurrence counts. Labels are recorded labels, not verified identities. Source bodies and source files remain unchanged.

Confidence: high in the reported counts under the stated parser; actual request execution and retrieval outcomes unknown.
