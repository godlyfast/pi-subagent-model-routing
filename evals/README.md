# Eval notes

`evals.json` holds eight read-only tabletop scenarios: audit-mode gates, chart identity/effort, override precedence, primary-429 handling, subscription bridges, bridge-native tool safety, optional Advisor recommendations, and Advisor configuration precedence/side-call safety.

Each scenario is evaluated with a fresh agent and no tools, given exactly these inputs: `SKILL.md`, `references/operations.md`, `references/bridges.md`, `references/advisor.md`, the scenario's `prompt`, and every fixture file listed in the scenario's `files` array. Judge against the assertions, not keyword counts. Running the evaluator itself can consume model quota and needs authorization; the evaluator only describes the scenario and never executes its commands.

## Fixtures

Fixtures under `fixtures/` are explicitly dated, version-pinned snapshots of upstream implementation facts so the evals run offline. They are frozen test truth, not runtime truth: never treat one as evidence about a live installation or for real routing work.

- `fixtures/routing-facts-pi-subagents-0.79.2.md` — pi-subagents runtime facts, extracted 2026-10-20 from upstream pi-subagents 0.79.2 documentation.
- `fixtures/bridge-facts-claude-0.9.3-antigravity-1.8.4.md` — Claude Bridge 0.9.3 (source links at tag `v0.9.3`) and Antigravity Bridge 1.8.4 (source links at commit `fa2d7a3d3a3f234bad86877928aeef4797680082`) implementation facts, extracted 2026-10-20.
- `fixtures/advisor-facts-rpiv-advisor-2.13.9.md` — Advisor plugin implementation facts from a 2026-10-20 source review of the installed 2.13.9 recorded at repository baseline `73a5a3b8ae75003958f45193ee3d2e570c223e55`. Its upstream links track `main` and are navigation aids only, not a version pin.

Frozen inputs stay frozen. This supersedes the earlier instruction to refresh `routing-facts-pi-subagents-0.79.2.md` in place whenever the pi-subagents version changes: published cases keep the exact fixture versions listed in their `files`, and a newer upstream version gets a new fixture file with deliberately revised cases instead of an in-place refresh. The published `routing-facts-pi-subagents-0.79.2.md` itself remains unchanged.

## Offline regression

```
python3 -m unittest discover -s tests -v
python3 scripts/check_public_ready.py
```

The tests are standard library only and run offline. They read only each scenario's `prompt` plus its listed fixture files — the documented scenario input seam — for safety-fact checks, and pin the original ids, names, expected outputs, all 39 assertions, and the cases 1-5 records against pre-refactor baseline digests. The readiness checker validates frontmatter, package files, links, privacy markers, and eval structure.

## What these checks do not establish

They validate process decisions against fixtures, not live model quality, account entitlement, quota, or provider availability, and no pass rate is claimed for this published package. An earlier internal pre-publication baseline observed that core safety discipline passed without the skill and that the remaining gaps were retrieval gaps (documented runtime facts the agent did not know), which the fixture and upstream links now supply; that observation is advisory only and is not reproduced here as a pass claim.

## Re-running

Ask a fresh agent to read the skill files and the fixtures listed in each scenario's `files`, then answer each prompt without tools. Record per-assertion outcomes and the exact evidence for each.
