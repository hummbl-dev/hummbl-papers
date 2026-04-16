# notebooks/

Per-paper research diaries. One `.notebook.md` file per paper. The notebook is the *reasoning chain*; the paper is the *polished output*.

## Why notebooks exist

Top research institutes — wet lab, computational, and ML — all enforce some form of dated, append-only, observation/interpretation-separated reasoning log distinct from the final manuscript. Without this practice, research becomes unauditable: bugs hide for months (a recent example: a published formal-complexity paper in our portfolio claimed `n^log n` was polynomial — it is quasi-polynomial — the kind of error a notebook's *predictions vs observations* section catches immediately).

Sources informing this convention:

- **Pineau ML Reproducibility Checklist v2.0** — https://www.cs.mcgill.ca/~jpineau/ReproducibilityChecklist.pdf
- **NeurIPS Paper Checklist** — https://neurips.cc/public/guides/PaperChecklist
- **Pitt "Notebook & Report Guidelines"** on observation/interpretation separation — http://ccc.chem.pitt.edu/wipf/Courses/NoteBook&Report.html
- **OSF Pre-Registration Standards** — https://osf.io/zab38/wiki/home/
- **Registered Reports at PCI RR** — https://rr.peercommunityin.org/PCIRegisteredReports/help/guide_for_authors

## Template

```markdown
# {Paper Slug} — Research Notebook

## Question (pre-registered, dated)
[YYYY-MM-DD] What does this paper prove, and to whom?

## Method (pre-declared, before any data/derivation)
Proof structure · experiment protocol · argument form

## Predictions (timestamped BEFORE observations)
What I expect to find.

## Observations (append-only, dated)
[YYYY-MM-DD] Did X. Saw Y.
[YYYY-MM-DD] Did P. Saw Q.

## Interpretation (separated from Observations)
Why I think Y means Z — explicitly distinct from what was observed.

## Dead ends (failed attempts, also first-class)
- Tried framing A — reviewer flagged B — switched to C
- Considered proof structure D — doesn't generalize to N>5 — dropped

## Open questions
- ...

## Cross-references
- Related papers in portfolio
- Bus events / CLP ledger entries / PR numbers
- External references
```

## Naming

- `{paper-slug}.notebook.md` — one per paper, slug matches the `papers/{paper-slug}/` directory
- Examples: `kill-switch-formal.notebook.md`, `delegation-depth.notebook.md`

## Rules

- **Append-only.** Corrections are new entries pointing at old ones; do not silently edit observations.
- **Dated entries.** Every observation and interpretation carries an ISO date.
- **Separate observation from interpretation.** The classic Pitt-Wipf rule: "Write down what you see, not your interpretation of it." Interpretation goes in its own section.
- **Document failures equally.** Negative results go in `Dead ends`. Do not silently drop approaches that didn't work — future you and future readers need them.
- **Pre-register predictions.** Write what you expect BEFORE running the experiment or derivation. A prediction/observation mismatch is where real learning happens.

## Notebooks here (to be populated)

_None yet — scaffolding only. First notebook arrives with its paper._
