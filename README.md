# HUMMBL Papers

Research portfolio and reproducibility artifacts for the HUMMBL governance infrastructure program.

## What's here

This repository is the public home of HUMMBL's research output — papers, accompanying research notebooks, datasets, and figures. Each release receives a [Zenodo](https://zenodo.org/) DOI for citation.

The papers target a single thesis: **governed AI infrastructure decomposes into a small set of composable primitives** — auditability (KRINEIA/TRACE), delegation (DCT, DELEGATION_DEPTH), coordination (COORDINATION_BUS), identity (AGENTIC_IDENTITY), safety (KILL_SWITCH), behavior (COMPLIANCE_THEATER, BKI), and measurement (BASE120, TRACE) — that together constitute a working substrate for AI governance.

## Layout

```
hummbl-papers/
├── README.md              # this file
├── CITATION.cff           # top-level citation metadata (Citation File Format)
├── .zenodo.json           # Zenodo release metadata
├── LICENSE                # MIT
├── ROADMAP.md             # shipped papers · in-flight · pre-registered backlog
├── papers/                # one directory per paper
│   └── README.md          # per-paper layout convention
├── notebooks/             # research diaries — one .notebook.md per paper
│   └── README.md          # notebook convention (Pineau + Pitt-Wipf)
└── docs/
    └── method/            # research methodology references
```

## How to cite

If you use this work, cite the specific paper's DOI (minted per-release via Zenodo) plus the top-level portfolio record using [CITATION.cff](CITATION.cff).

For ongoing papers that are pre-print only, see the paper's own `papers/<name>/README.md` for its arXiv or preprint server link.

## Contributing

This repository is maintained by HUMMBL Research. External contributions to existing paper drafts require prior coordination — open an issue first. Discussions, replication attempts, and negative-result reports are welcome.

Before opening a pull request, run:

```bash
python tools/validate_repository.py
```

Release readiness runs the same validator in strict artifact mode:

```bash
python tools/validate_repository.py --release-artifacts
```

That mode intentionally fails until `papers/` and `notebooks/` contain actual
paper/notebook artifacts beyond their layout README files. GitHub Actions runs
the strict gate on version tags and manual release-readiness dispatches.

## Author

**Reuben Bowlby** · [ORCID: 0009-0002-5620-1103](https://orcid.org/0009-0002-5620-1103) · HUMMBL

## License

MIT. See [LICENSE](LICENSE). Individual paper content may adopt a per-release license via the Zenodo deposit record if different; the MIT license applies to the repository scaffolding and code artifacts.
