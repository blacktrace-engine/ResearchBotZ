# Provenance

The source is [Collusion Wiki’s published archive](https://collusion.wiki/explorer/download.html) of observed agent activity. Its authors reconstructed deleted pages from wiki edit histories and redacted identifying information.

The archive contains five files:

* `pages.jsonl`
* `revisions.jsonl`
* `events.jsonl`
* `labels.jsonl`
* `manifest.json`

All five expanded files match the SHA-256 checksums published on the download page. Repository copies are gzip-compressed; decompression restores the original bytes unchanged.

Names, labels, URLs, dates and statements within these files are preserved source content.

This repository supplies the audit code, tests and frozen results alongside the source files. Run `python scripts/reproduce.py` to verify file integrity and reproduce the measurements. The audit reports document how references are grouped and written results identified.
