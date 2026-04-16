# Drafting → Publishing Convention

**Decision date:** 2026-04-16
**Status:** ACTIVE
**Pattern adopted:** **Option 4 — Copy at release, founder-mode frozen after**

---

## Decision

Papers are **drafted privately** in the founder-mode workspace. At "publication moment" — arXiv + Zenodo deposit — the final paper content is **copied** atomically into `hummbl-papers/papers/{slug}/`. After that point:

- `hummbl-papers` is the **canonical source** for that paper
- The founder-mode copy becomes an **archived draft** (preserved for historical context, not edited)
- Subsequent revisions (arXiv v2, journal response-to-reviewers, second Zenodo version) happen **in hummbl-papers only**

This is the standard academic pattern: drafting in private, publication to a public venue, post-publication updates flow through the public venue.

---

## Why not the alternatives

Five options considered; four rejected:

| # | Option | Why rejected |
|---|---|---|
| 1 | MOVE (delete from founder-mode) | Loses the hardening-session lineage; paper-hardening session history becomes unfindable when searching founder-mode |
| 2 | COPY + BOTH EDIT | Divergence guaranteed eventually; "which is canonical" question never goes away |
| 3 | SYMLINK / git submodule / git subtree | GitHub renders symlinks as links, not content; submodules have known friction for collaborators; subtree is complex for a one-way flow |
| **4** | **COPY AT RELEASE (chosen)** | Atomic cutover; canonical source clear per paper; preserves privacy during drafting; zero disruption to active sessions |
| 5 | hummbl-papers always canonical | Would require migrating ~20 in-flight drafts mid-hardening-session; disruption cost too high; also exposes half-formed ideas to the public repo |

Plain terms: we get to iterate hard in private while a paper is unstable, then publish a clean artifact when it's ready. After publication, history lives in git (on both repos), but edits only happen in one place.

---

## Per-paper lifecycle

```
┌──────────┐    ┌─────────┐    ┌─────────┐    ┌────────────┐    ┌─────────┐
│ PROPOSED │───▶│ SCOPED  │───▶│ DRAFTING│───▶│   REVIEW   │───▶│ PUBLISH │
└──────────┘    └─────────┘    └─────────┘    └────────────┘    └────┬────┘
                                                                      │
                                                                      ▼
                                                             ┌────────────────┐
                                                             │  (cutover)     │
                                                             │  founder-mode  │
                                                             │  → frozen      │
                                                             │  hummbl-papers │
                                                             │  → canonical   │
                                                             └────────┬───────┘
                                                                      │
                                                                      ▼
                                                              ┌───────────────┐
                                                              │ PUBLISHED     │
                                                              │ (arXiv +      │
                                                              │  Zenodo DOI)  │
                                                              └───────┬───────┘
                                                                      │
                                                                      ▼
                                                              ┌───────────────┐
                                                              │ REVISED(N)    │
                                                              │ (same concept │
                                                              │  DOI, new     │
                                                              │  version DOI) │
                                                              └───────────────┘
```

### State: PROPOSED
Pre-registered entry in `ROADMAP.md` backlog. Claim + method declared. No content yet. Location: this repo only.

### State: SCOPED
Entry elaborated with predictions, expected structure, dependencies. Still in `ROADMAP.md`. No content yet.

### State: DRAFTING
Content creation happens in **founder-mode** at `founder_mode/docs/publications/{SLUG}_DRAFT.md` (or .tex). Per-paper `.notebook.md` created alongside to capture observation/interpretation/dead-end log. This is the paper-hardening session's native workspace.

### State: REVIEW
Hostile review round(s) applied in founder-mode. Feedback annotated into the `.notebook.md`. Still private.

### State: PUBLISH (cutover moment)
One-shot migration from founder-mode to hummbl-papers. See *Publication migration procedure* below. After this commit lands in hummbl-papers, the founder-mode copy must not be edited.

### State: PUBLISHED
Paper has:
- Preprint on arXiv (or discipline-appropriate server)
- Zenodo deposit with concept DOI + version DOI
- `papers/{slug}/` directory in hummbl-papers as canonical source
- `ROADMAP.md` table row with both IDs

### State: REVISED
Post-publication changes (arXiv v2, journal response, second Zenodo version) happen on feature branches of hummbl-papers only. Each revision:
- Commit to `hummbl-papers/papers/{slug}/`
- Notebook gains observation entries (append-only, dated)
- If Zenodo revision: mint new version DOI under the existing concept DOI
- If arXiv revision: push new arXiv version (arXiv handles versioning natively)

---

## Publication migration procedure

When a paper transitions REVIEW → PUBLISHED, execute this procedure exactly once:

1. **In founder-mode:** final hostile-review pass complete. Verify bus MILESTONE posted: `Paper {SLUG} ready for publication`. No further edits to the founder-mode draft after this point.

2. **Create** `hummbl-papers/papers/{slug}/` with this layout:
   ```
   papers/{slug}/
   ├── README.md         # one-sentence abstract, status, DOI when minted
   ├── paper.tex         # canonical manuscript (or .md if non-LaTeX)
   ├── references.bib    # paper-local bibliography
   ├── figures/          # figure sources + renders
   └── build/            # gitignored
   ```

3. **Copy** `notebooks/{slug}.notebook.md` from founder-mode or reconstruct post-hoc (see *Notebook migration* below).

4. **Commit** to hummbl-papers with message:
   ```
   publish(papers/{slug}): {Paper Title}

   Migration from founder-mode/docs/publications/{SLUG}_DRAFT.md.
   Founder-mode copy is archived at commit {HASH}; no further edits.

   Preprint: {arXiv ID}
   Zenodo deposit: {DOI or "pending"}
   ```

5. **Post preprint to arXiv** (if not done). Update `papers/{slug}/README.md` with the arXiv ID.

6. **Create Zenodo deposit** manually per `docs/method/doi-strategy.md`. Record the concept DOI + version DOI.

7. **Update** `papers/{slug}/README.md` with the DOI badge.

8. **Update** `ROADMAP.md` Shipped table row: title, arXiv ID, DOI.

9. **Bus MILESTONE:** `Paper {SLUG} PUBLISHED — arXiv {id}, Zenodo {DOI}, commit {hash}`.

10. **In founder-mode:** append to the draft file's first line or top:
    ```
    <!-- ARCHIVED DRAFT — published in hummbl-papers/papers/{slug}/ on {date}. Do not edit. -->
    ```
    Commit that annotation with message: `docs(archive): {SLUG} migrated to hummbl-papers`.

After step 10, **the founder-mode copy is frozen**. If anyone opens it in an editor, the archive header tells them to go to hummbl-papers.

---

## Notebook migration

### New papers (paper #21 onward)
Start the `.notebook.md` in founder-mode at the moment of pre-registration, before any drafting. When the paper publishes, copy the notebook to `hummbl-papers/notebooks/{slug}.notebook.md`. Future observations append there, not in founder-mode.

### Legacy papers (the ~20 currently being hardened)
These drafts were written without a notebook discipline. At publication time, reconstruct the notebook post-hoc with a best-effort reconstruction:
- Question & method sections: extract from the paper itself
- Observations: from founder-mode git log of the draft (commit messages narrate what was done when)
- Dead ends: extract from hostile-review MILESTONEs on the bus + git log of reverted commits
- Open questions: carried forward into the notebook for future revisions

A post-hoc notebook is a weaker artifact than a real-time notebook, but it's still the right shape for future revisions and cross-paper synthesis. Legacy-paper notebooks should carry a header: `<!-- Post-hoc reconstruction from drafting history. Future entries are real-time. -->`.

---

## What each repo is for

| Question | Answer |
|---|---|
| Where do new paper drafts go? | founder-mode `docs/publications/` until publication |
| Where is the canonical post-publication paper? | hummbl-papers `papers/{slug}/` |
| Where does the pre-registration entry live? | hummbl-papers `ROADMAP.md` (always — from PROPOSED onward) |
| Where does the research notebook live during drafting? | founder-mode `docs/publications/{slug}.notebook.md` |
| Where does the research notebook live post-publication? | hummbl-papers `notebooks/{slug}.notebook.md` (migrated) |
| Where do figures live during drafting? | founder-mode alongside the draft |
| Where do figures live post-publication? | hummbl-papers `papers/{slug}/figures/` |
| Where do references live? | per-paper `references.bib` (local to each directory, no shared portfolio bib yet — revisit at ~30 papers) |

---

## Open questions (revisit as portfolio grows)

- **Shared bibliography:** at what paper count does a portfolio-level `references.bib` become worth the coordination cost? (Current answer: not yet. Per-paper bibs are fine through ~30 papers.)
- **Cross-paper cross-references:** if paper B cites paper A (same portfolio), how? Answer today: cite paper A's Zenodo DOI like any external reference. Revisit if cross-references become frequent.
- **Figure reuse:** if the same figure appears in two papers, is it duplicated or linked? Default: duplicate. Revisit if this becomes painful.
- **Pre-publication peer review:** does any paper in this portfolio go through a formal pre-publication peer review (e.g., PCI Registered Reports)? If yes, the REVIEW state needs to split into INTERNAL-REVIEW and EXTERNAL-REVIEW.

## Revision

Revise this convention if:
- Portfolio exceeds ~30 papers and manual per-paper migration becomes bottleneck
- A paper needs to migrate back (hummbl-papers → founder-mode) for any reason — which would indicate the convention is wrong
- A contributor works on a paper who doesn't have founder-mode access — currently a one-author portfolio, so not yet an issue
