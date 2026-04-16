# papers/

One subdirectory per paper. Each paper directory follows this convention:

```
papers/{paper-slug}/
├── README.md              # one-sentence abstract + current status + link to notebook
├── paper.tex              # main manuscript
├── references.bib         # bibliography
├── figures/               # figure sources + renders
├── data/                  # (optional) paper-specific data
└── build/                 # (gitignored) LaTeX output
```

## Naming

- `paper-slug` is kebab-case, matches the notebook filename (`notebooks/{paper-slug}.notebook.md`)
- Examples: `kill-switch-formal`, `delegation-depth`, `tuple-atomic-record`

## Per-paper README template

```markdown
# {Paper Title}

**Abstract (one sentence):** ...

**Status:** PROPOSED | SCOPED | DRAFTING | REVIEW | SHIPPED
**Notebook:** [../../notebooks/{paper-slug}.notebook.md](../../notebooks/{paper-slug}.notebook.md)
**Authors:** Reuben Bowlby (ORCID 0009-0002-5620-1103)
**Venue (target / actual):** arXiv | PCI RR | PLOS ONE | ...
**DOI:** (minted on Zenodo release)
**License:** MIT (or per-release override)

## Build

```bash
cd papers/{paper-slug}
latexmk -pdf paper.tex
```
```

## Release workflow

1. Paper enters DRAFTING — directory created with scaffold
2. Notebook `notebooks/{paper-slug}.notebook.md` tracks reasoning chain
3. Paper moves to REVIEW — hostile review applied, feedback annotated in notebook
4. Paper SHIPPED — git tag `v{version}` triggers Zenodo DOI mint per release
5. ROADMAP.md table updated with DOI

## Paper directories here (to be populated)

_None yet — scaffolding only. First paper arrives once founder-mode paper-hardening sweep completes._
