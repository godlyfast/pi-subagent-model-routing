---
name: pi-subagent-model-routing
description: "Use when auditing, recommending, probing, or applying Pi subagent model and thinking-level assignments (pi-subagents agentOverrides, per-run overrides, profiles), when comparing benchmark charts against subscriptions and quotas for role routing, when a Pi role override did not take effect, or when checking/recommending an installed Advisor plugin model."
license: MIT
metadata:
  version: "1.0.2"
---

# Pi subagent model routing

Match each Pi subagent role to a usable, policy-compliant route, not a leaderboard winner. Reuse the native pi-subagents tooling; this skill adds no router, quota client, or benchmark scraper. Model generations, prices, scores, and provider namespaces are discovered fresh each run rather than pinned here.

## Choose the authorized mode

| Request | Scope |
|---|---|
| Audit / recommend / reevaluate | Allowlisted metadata and public evidence only; report a proposal. No inference, catalog refresh, profile generation, or edits. |
| Probe | Bounded inference on the approved routes only. Not by itself approval to apply. |
| Apply | Make the approved targeted settings changes and validate them. Live inference needs its own authorization. |

Preserve non-conflicting prior approvals. Installs, upgrades, purchases, and credential changes each need their own authorization.

## Runtime semantics come from upstream, at the installed version

pi-subagents owns the behavior facts that decide routing cases — precedence, thinking-level syntax, fast mode, modelScope, profile loading, external-runner support. They change between releases, so read the upstream pi-subagents documentation (`docs/models.md`, `docs/agents.md`, `docs/tool-reference.md`) matching the installed version before acting, and record that version beside any claim made from them. Workflow rules live in this skill; runtime semantics live upstream.

Two workflow requirements apply:

- **Attribute every route; no fallback-as-success.** Verify which route each run actually resolved. A fallback route's success never passes a failed primary; trying another model requires its own explicit, authorized launch. If a configured virtual router can switch physical models, inspect its behavior and record both requested and resolved routes before treating a probe as attributable.
- **Model and thinking level travel together.** Every recommendation and every applied change names a model and a deliberate thinking level.

## Operator policy

The deployment's provider allow/deny lists, budget rules, and data-handling policy outrank any routing preference. Derive Pi provider policy from Pi-sourced evidence at the installed version — never transplanted from another tool's configuration — and record the policy source beside each recommendation.

## Workflow

1. **Establish scope.** Record Pi and pi-subagents versions, user versus project settings paths, and concurrent edits. Check whether an Advisor plugin is installed: if present, inspect its current model/effort and recommend separately using [Advisor inventory](references/advisor.md); if absent report N/A without installation. Read allowlisted fields only — never raw settings, auth files, or environment dumps.
2. **Reconcile access.** Follow [inventory and access](references/operations.md#inventory-and-access). For extension providers such as Claude Bridge or Antigravity, also read [bridge contracts](references/bridges.md) before recommending: subscription billing, thinking translation, child prompt delivery, and native tool boundaries differ from direct APIs. Keep registry entry, saved auth, entitlement, quota, and probe results separate; an `enabledModels` entry is catalog presence, not entitlement.
3. **Refresh the comparison.** Fetch current primary benchmark pages — Artificial Analysis model and methodology pages plus vendor docs for the IDs, effort enums, and list prices you cite. Record each claim's URL, retrieval date, index version, and effort setting. Map chart display names to exact registry IDs; mark unmapped names unresolved. Compare like efforts only; native-harness agent scores are not Pi subagent scores; API list price is not subscription marginal cost.
4. **Recommend or probe.** Audit mode stops at the proposal. Probes require authorization and follow [bounded probes](references/operations.md#bounded-probes); stop if measurable bounds cannot be enforced. Never fall back to a shell/CLI execution lane when the governed subagent lane fails.
5. **Apply only approved changes.** Re-read live settings immediately before editing; stop if the target fields changed unexpectedly. Merge only approved fields; keep a private rollback copy. Approval for one file or role does not extend to others. Saved fields and the live `/subagents-models` mapping must agree; disk edits are not live until reload.
6. **Hand off.** Report changed files, old-to-new assignments, unknowns, and reload requirements.

## Required result shape

- **Evidence date and runtime versions.**
- **Access table:** provider/model, auth, catalog, entitlement, quota, probe — each verified or unknown.
- **Routing table:** role, current route+thinking, proposed route+thinking, billing rationale, confidence. Include a separate **advisor-plugin** row when installed (or N/A/unknown), distinguishing saved selection from active runtime and any native-CLI reviewer policy.
- **Verification and blockers:** native checks run, unresolved alias/entitlement gaps, reload guidance.
