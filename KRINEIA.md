# KRINEIA.md — hummbl-papers

**krineia_manifest_version:** 0.1
**schema:** krineia-manifest@0.1

---
krineia_manifest_version: "0.1"
schema: "krineia-manifest@0.1"

repo:
  full_name: "hummbl-dev/hummbl-papers"
  default_branch: "main"
  visibility: "private"

authority:
  steward: "HUMMBL Research Institute"
  approving_human: "Reuben Bowlby"
  source_of_record: "git"
  receipt_authority: "external_observer"

governance_profile:
  status: "adopted"
  krineia_required: true
  trust_root_mode: "deployment_asserted"

chains:
  primary:
    chain_id: "hummbl-papers-primary"
    storage: "_receipts/krineia/primary.jsonl"
    genesis_policy: "repo_bootstrap"
    hash_algorithm: "sha256"
    canonicalization: "json.dumps(sort_keys=True,separators=(',',':'))"

operators:
  allowed: ["append", "project", "cut"]
  forbidden: ["update", "delete", "rewrite", "summarize_and_replace", "score_and_train"]

boundaries:
  no_reward_path_self_reference: true
  external_analysis_only: true
  observed_agent_may_write_receipts: false
  receipts_may_train_agents: false

verification:
  validator: "external"
  required_before_release: true

last_reviewed: "2026-06-22"
---

## Notes

The primary chain at `_receipts/krineia/primary.jsonl` is bootstrapped with a genesis receipt.
