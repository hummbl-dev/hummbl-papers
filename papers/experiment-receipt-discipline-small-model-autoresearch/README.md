# Experiment Receipt Discipline for Small-Model Autoresearch

**Abstract (one sentence):** This proposed case-study paper examines how experiment receipts — separating hypothesis, baseline, noise floor, measured outcome, and KEEP/DISCARD decision — make small-model autoresearch auditable, using the `autoresearch-pipeline` corpus (34 governed experiments, 2 kept patches, 32 preserved negative results) as the worked example.

**Status:** PROPOSED
**Notebook:** [../../notebooks/experiment-receipt-discipline-small-model-autoresearch.notebook.md](../../notebooks/experiment-receipt-discipline-small-model-autoresearch.notebook.md)
**Authors:** Reuben Bowlby (ORCID 0009-0002-5620-1103)
**Venue (target / actual):** arXiv or Zenodo-first technical report
**DOI:** pending
**License:** MIT

## Source packet

- [research-source-packets#9](https://github.com/hummbl-dev/research-source-packets/pull/9) — first-party experiment receipt corpus source packet (candidate-only)

## Build

This seed uses Markdown while the paper is scoped:

```bash
python ../../tools/validate_repository.py --release-artifacts
```

If the paper moves to review, convert `paper.md` to the venue-required format and update this README with the build command.

## Local Sources

- [paper.md](paper.md)
- [references.bib](references.bib)
- [research notebook](../../notebooks/experiment-receipt-discipline-small-model-autoresearch.notebook.md)
