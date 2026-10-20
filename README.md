# pi-subagent-model-routing

A Pi skill for matching each pi-subagents role to a usable, policy-compliant model route. It covers three separately authorized modes — audit, bounded probe, guarded apply — around the pi-subagents extension's own configuration surfaces. It ships no routing engine, quota client, or benchmark scraper: model generations, prices, scores, and provider namespaces are discovered at run time, never frozen in this repository.

## Requirements

- Pi with package installation (`pi install`); see `docs/packages.md` in your installed Pi release.
- The [pi-subagents](https://github.com/nicobailon/pi-subagents) extension installed and working.
- At least one model provider configured in Pi.
- Python 3 (standard library only) to run the offline readiness check.

## Install

```bash
pi install git:github.com/godlyfast/pi-subagent-model-routing@v1.0.2
```

The package exposes `SKILL.md` through the `pi.skills` manifest in `package.json`. Reload or start a new Pi session; the skill appears as `pi-subagent-model-routing`.

## Use

Audit is the default: allowlisted metadata and public evidence only, proposal only, no inference.

```text
/skill:pi-subagent-model-routing audit my current subagent role assignments against current benchmark evidence. Propose only.
```

Probe needs explicit routes and a budget; it never changes routing.

```text
/skill:pi-subagent-model-routing probe acme/example-model:low on scout only: one minimal prompt, at most 64 output tokens, 60-second timeout, no retries. Do not change routing.
```

Apply needs an approved mapping; it verifies the live mapping after reload.

```text
/skill:pi-subagent-model-routing apply the approved agentOverrides mapping for worker and reviewer, then verify the live mapping after reload.
```

`acme/example-model:low` is a fictional example; substitute an exact registered route and supported thinking level. The probe stops if its requested bounds or isolation cannot be enforced.

## What the skill guides

- Audit, probe, and apply are separate authorizations; an audit never runs inference or mutates configuration.
- Access evidence stays in distinct columns: saved auth, catalog entry, entitlement, quota, probe result.
- Every recommendation names an explicit model and thinking level together, mapped from benchmark URL, retrieval date, and effort setting to exact registry IDs.
- API list price is never presented as subscription marginal cost.
- Apply is guarded: re-read before editing, a private rollback copy, scope limited to approved fields, and a fallback route's success never passes a failed primary.

## Optional Advisor recommendations

When an Advisor plugin is installed, the skill [checks its saved model, effort, and executor-disable rules](references/advisor.md) without consulting or changing it. It reports a separate current/proposed Advisor row—not the subagent `oracle` alias—and respects your model/effort and native-reviewer policies. When absent, it reports N/A without installing anything. Saved configuration does not establish active runtime state or provider health.

## Provider bridge support

[Claude Bridge and Antigravity Bridge contracts](references/bridges.md) cover extension-provider routes inside Pi, including subscription-backed billing evidence, exact model/thinking mappings, child prompt/skill delivery, and native tool boundaries. Subscription routes are eligible candidates—not automatically expensive direct API routes, free usage, or verified access.

Claude Bridge's forwarded Pi tools and Antigravity's native tool loop have different safety contracts. In particular, a Pi tool allowlist or worktree does not make AGY read-only. Audits do not launch bridges, change authentication, or enable paid usage. Bridge support is **source-reviewed guidance**, not a claim that either plugin has passed live subagent integration tests.

## Limitations

- Pi runtime semantics (precedence, thinking-level syntax, fast mode, modelScope, external runners) are version-dependent and documented upstream in pi-subagents. This skill links them instead of copying them; cite the installed version beside any claim made from them.
- The tabletop evals in `evals/` are process checks against explicitly versioned fixtures. They are not model benchmarks and prove nothing about live account access or quota.
- No model rankings, scores, or prices are frozen here; every quantitative fact must be re-derived at run time from primary sources.

## Offline check

```bash
python3 scripts/check_public_ready.py
```

Checks frontmatter, package files and relative links, common local-path and credential markers, and eval structure. Standard library only; no network access. This bounded check is not a comprehensive secret scanner; manually review every file before publication.

## Attribution

Built around [pi-subagents](https://github.com/nicobailon/pi-subagents) (MIT), whose extension provides the subagent lanes, settings surfaces, and documentation this skill defers to. Pi skill and packaging mechanics follow the docs of the installed Pi release. Not affiliated with the pi-subagents or Pi maintainers.

## License

MIT. Copyright (c) 2026 godlyfast. See [LICENSE](LICENSE).
