# Eval notes

`evals.json` holds six read-only tabletop scenarios: audit-mode command gates, chart identity/effort mapping, override precedence, primary-429 handling, subscription provider bridges, and bridge-native tool safety. Run each with a fresh agent given only `SKILL.md`, `references/operations.md`, `references/bridges.md`, and the fixture listed in the scenario's `files`, with no tools. Judge against the assertions, not keyword counts. Running the evaluator itself can consume model quota and needs authorization; the evaluator only describes the scenario and never executes its commands.

## Fixtures

`fixtures/routing-facts-pi-subagents-0.79.2.md` is an explicitly versioned snapshot of upstream pi-subagents runtime facts so the evals run offline. It is dated and fixture-only: refresh it from the upstream docs whenever the pi-subagents version changes, and never treat it as live truth for real routing work.

## What these checks do not establish

They validate process decisions against fixtures, not live model quality, account entitlement, quota, or provider availability, and no pass rate is claimed for this published package. An earlier internal pre-publication baseline observed that core safety discipline passed without the skill and that the remaining gaps were retrieval gaps (documented runtime facts the agent did not know), which the fixture and upstream links now supply; that observation is advisory only and is not reproduced here as a pass claim.

## Re-running

Ask a fresh agent to read the skill files and answer each prompt without tools. Record per-assertion outcomes and the exact evidence for each.
