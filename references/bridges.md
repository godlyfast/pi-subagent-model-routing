# Subscription provider bridges

Read this before evaluating extension-provided Claude or Antigravity routes. These are Pi **providers**, not external CLI runner profiles, `AskClaude`, or `AskAntigravity`. Supporting their audit does not establish successful child execution or vendor authorization.

## Inventory before recommending

1. Record the installed bridge package/version, active engine, exact registered `provider/model` ID, model identity source, supported thinking map, and child extension-loading requirements. Inspect existing metadata and source without starting a bridge or refreshing its catalog: startup can discover models, write configuration, download binaries, or initiate sign-in.
2. Separate the registered bridge ID from the underlying vendor model ID and benchmark label. Preserve provider namespaces: a direct API route, a subscription bridge, and another provider with the same model name are distinct routes. Likewise, a new OpenAI provider does not silently replace a legacy route. Resolve exact IDs against the installed catalog; hold unresolved mappings rather than rewriting them.
3. Record dated owner confirmation of a subscription billing path as evidence for that route. Do not exclude it merely because the underlying model's direct API price is high. Independently mark effective billing configuration, per-model entitlement, and remaining shared quota verified or unknown. Zero catalog cost is not free or unlimited usage; subscription evidence for a bridge does not cover the direct API route. Inspect only allowlisted non-secret configuration or credential-presence metadata; never read token values or dump configuration/environment files.
4. Verify bridge-specific thinking translation, context limits, prompt/skill delivery, child hooks, session isolation, and native versus forwarded tools. A supported thinking label is not proof of equivalent benchmark effort. A registry entry, fallback catalog, or working parent session is not proof that a fresh/background child can use it.
5. In audit mode stop with the proposal. For a later authorized probe, enforce the [probe contract](operations.md#bounded-probes) across the bridge's native execution as well as Pi tools. Stop if tool containment, prompt delivery, model attribution, or token/time bounds cannot be established. Do not substitute an `Ask*` tool or external runner to pass a failed provider route.

## Version-scoped contracts

Source-reviewed **2026-10-20**: `pi-claude-bridge` **0.9.3** and `@estebanforge/pi-antigravity-bridge` **1.8.4**. These are documentation snapshots, not required pins or live compatibility tests. Recheck the installed implementation on version changes.

| Surface | Claude Bridge provider | Antigravity Bridge provider |
|---|---|---|
| Route | `claude-bridge/<registered-id>` | `antigravity/<registered-id>`; record ACP versus stream-json engine |
| Tools | Claude Code starts with native `tools: []`; exposed Pi tools round-trip through Pi. Native Claude hooks can still run. This alone is not isolation. | Native file/command tools execute outside Pi's forwarded-tool allowlist. Display/replay cards are not prior approval; a worktree or Pi allowlist is not a sandbox. |
| Read-only use | Conditional on verified child prompt projection, Pi tool boundaries, hooks, MCP configuration, and isolation. | Provider `readOnly`/`plan` turns refuse rather than provide safe review-only execution. Do not use a no-tools health probe or default read-only reviewer/scout assignment. A later write-capable task requires explicit write authorization and verified containment. |
| Thinking | Check the registered per-model thinking map and SDK translation; the provider and legacy AskClaude mappings differ. | Check the model's supported tiers and translation/clamping. In 1.8.4, high/xhigh/max can map to high; fixed-thinking entries may expose no toggle. |
| Context/billing | Plan settings, long-context Extra Usage, and inherited gateway/API environment can change effective context or billing. Flag uncertainty; do not toggle or unset anything without approval. | Shared subscription quota and engine-specific usage estimates are not API-dollar accounting or a verified balance. A fallback picker entry does not prove authentication or availability. |

For Claude Bridge, verify the installed subagent implementation's child extension/hook loading and portable prompt projection. Its README example for `@gotgenes/pi-subagents` is not configuration guidance for `nicobailon/pi-subagents`. Prompt rejection is a blocker, not permission to remove operating instructions or enable Extra Usage.

For Antigravity, `approvals.gateMode: auto` does not prove an active approval gate: detection and effective decisions must be verified. Its `activate_skill` catalog in 1.8.4 mirrors supported directory roots, not Pi package-manifest, settings-array, or `--skill` sources. Native Pi discovery does not prove AGY skill delivery; verify the actual delivery path before execution. Do not install another skill copy, change engine, disable refusal controls, enable skip-permissions, or start auth as an audit workaround.

## Evidence and account warnings

Report each route as **source/catalog-supported, execution untested**, **probe-verified within stated bounds**, or **blocked**, with the reason. Keep registration, entitlement, billing path, quota, and child execution as separate evidence. Surface upstream subscription/Extra Usage and terms/account-risk warnings with dates and attribution; community bridge documentation is not blanket vendor permission. Reassess current official terms before recommending operational use.

Primary implementation references:

- [Claude Bridge 0.9.3 README](https://github.com/elidickinson/pi-claude-bridge/blob/v0.9.3/README.md), [provider/tools/effort implementation](https://github.com/elidickinson/pi-claude-bridge/blob/v0.9.3/src/index.ts), [model projection](https://github.com/elidickinson/pi-claude-bridge/blob/v0.9.3/src/models.ts).
- [Antigravity Bridge 1.8.4 source snapshot](https://github.com/EstebanForge/pi-extensions/tree/fa2d7a3d3a3f234bad86877928aeef4797680082/packages/pi-antigravity-bridge): `README.md`, `src/provider.ts`, `src/models.ts`, and `src/approval-detect.ts`. The README links upstream permission limitations and terms warnings; its account-risk estimates are the author's position, not this skill's assurance.
