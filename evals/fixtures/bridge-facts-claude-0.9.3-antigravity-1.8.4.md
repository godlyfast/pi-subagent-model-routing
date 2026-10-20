# Versioned fixture: bridge implementation facts (pi-claude-bridge 0.9.3, pi-antigravity-bridge 1.8.4)

**Fixture, not live truth.** Frozen tabletop-eval input, extracted 2026-10-20 from the source-reviewed upstream bridge implementations linked below, so the evals in `evals/evals.json` run offline. Treat it as frozen test truth for the published cases only, never as runtime truth about a live installation: real tasks read the implementation matching the installed version and cite that version. A newer upstream version gets a deliberately revised fixture and cases; this file does not get refreshed in place.

## Claude Bridge provider (pi-claude-bridge 0.9.3)

- Claude Code starts with native `tools: []`; exposed Pi tools round-trip through Pi. Native Claude hooks can still run. `tools: []` alone is not isolation.
- Child delivery is conditional: child prompt projection and child extension/hook loading must be verified for the installed subagent implementation. Prompt rejection is a blocker.
- The README's subagent settings example targets `@gotgenes/pi-subagents`, a different subagent package; it is not configuration guidance for `nicobailon/pi-subagents`.

## Antigravity Bridge provider (pi-antigravity-bridge 1.8.4)

- Native file/command tools execute outside Pi's forwarded-tool allowlist. A Pi tool allowlist or Git worktree is not a sandbox; display/replay cards are not prior approval.
- Provider `readOnly`/`plan` turns refuse rather than provide safe review-only execution. Do not use a no-tools health probe or a default read-only reviewer assignment, and do not disable refusal controls to work around a refusal.
- `activate_skill` mirrors supported directory roots, not Pi package-manifest, settings-array, or `--skill` sources. Native Pi skill discovery does not prove AGY skill delivery; verify the actual delivery path before execution.
- `approvals.gateMode: auto` does not prove an active approval gate; detection and effective decisions must be verified.

## Source attribution

Source-reviewed 2026-10-20. Claude Bridge tag `v0.9.3`: [README](https://github.com/elidickinson/pi-claude-bridge/blob/v0.9.3/README.md), [provider/tools/effort implementation](https://github.com/elidickinson/pi-claude-bridge/blob/v0.9.3/src/index.ts), [model projection](https://github.com/elidickinson/pi-claude-bridge/blob/v0.9.3/src/models.ts). Antigravity Bridge source snapshot at commit `fa2d7a3d3a3f234bad86877928aeef4797680082`: [package README](https://github.com/EstebanForge/pi-extensions/tree/fa2d7a3d3a3f234bad86877928aeef4797680082/packages/pi-antigravity-bridge), `src/provider.ts`, `src/models.ts`, `src/approval-detect.ts`. These are documentation snapshots, not required pins or live compatibility tests; recheck the installed implementation on version changes.
