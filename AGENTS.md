# AGENTS.md — hummbl-papers

## Project
**hummbl-papers** — HUMMBL Research governance infrastructure papers and reproducibility artifacts. Python repository with paper drafts, research notebooks, datasets, and figures. Each release receives a Zenodo DOI.

## Scope
- In scope: Research papers (one directory per paper), research notebooks (Pineau + Pitt-Wipf convention), methodology references, release validation tooling, Zenodo/CITATION.cff metadata
- Out of scope: Executable mental model operators, governance runtime code, skill definitions

## Setup
```bash
git clone https://github.com/hummbl-dev/hummbl-papers.git
cd hummbl-papers
pip install -e .  # if tools have dependencies
```

## Testing
```bash
# Validate repository structure (layout, metadata, artifacts)
python tools/validate_repository.py

# Release-readiness strict mode (fails until papers/notebooks have real artifacts)
python tools/validate_repository.py --release-artifacts
```

## Conventions
- One directory per paper under `papers/`; each has its own README with layout convention
- Research notebooks under `notebooks/` — one `.notebook.md` per paper
- CITATION.cff for automated citation; `.zenodo.json` for release metadata
- External contributions require prior coordination — open an issue first
- MIT license (repository scaffolding and code); individual papers may adopt per-release license via Zenodo
- Commit format: Conventional Commits
- Branch naming: type/agent/short-desc

## CI
GitHub Actions workflow `validate.yml` runs `tools/validate_repository.py`. Strict artifact mode runs on version tags and manual release-readiness dispatches.
