# Contributing to Autoresearch Reports

This repository carries generated research artifacts plus a small amount of operational configuration. CI is intentionally narrow and mechanical.

## Scope

This repo is a shared depot for the Autoresearch → distillation → proposal pipeline. Most changes are automated; manual contributions are limited to operational configuration.

## Manual Changes

If you need to modify operational configuration:

1. Update `research_queue.json` (topic queue with recurrence schedules)
2. Update shell or PowerShell helpers in the root
3. Ensure CI passes (syntax checks only)

## CI Posture

CI does not judge report quality, synthesis quality, or whether generated findings should be adopted. Those remain review decisions outside CI.

## Naming Convention

- Reports: `reports/YYYY-MM-DD-domain-query-slug.md`
- Findings: `findings/YYYY-MM-DD-domain.json`
- Proposals: `proposals/YYYY-MM-DD-target-description.md`

## License

By contributing, you agree that your contributions will be licensed under the Apache 2.0 license.
