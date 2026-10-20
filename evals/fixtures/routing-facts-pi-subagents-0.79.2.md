# Versioned fixture: pi-subagents routing facts (0.79.2)

**Fixture, not live truth.** Dated snapshot extracted 2026-10-20 from the upstream [pi-subagents](https://github.com/nicobailon/pi-subagents) documentation (`docs/models.md`, `docs/agents.md`, `docs/watchdog.md`) at pi-subagents 0.79.2, so the tabletop evals in `evals/evals.json` run offline. Runtime behavior is owned by upstream and changes between releases: for any real task, read the upstream docs matching your installed version and cite that version. Refresh this file when the pi-subagents version changes. No model rankings, scores, or prices live here.

## Precedence and identity (models.md)

- Precedence, strongest first: per-run override → provider-scoped role override (`agentOverridesByProvider.<parentProvider>.<role>`, fields layer over the ordinary override in the same settings file) → `agentOverrides.<name>.model` → agent frontmatter `model` → `subagents.defaultModel` → the parent session model. Project settings win over user settings.
- A fully qualified `provider/model` string wins exactly. A qualified provider query never silently switches providers; bare IDs can match fuzzily within the named provider or the current session's provider.

## One route per launch (models.md)

- Each launch resolves one model and starts the child once. Provider, authentication, quota, rate-limit, stream, empty-response, context-overflow, and provisioning failures — including HTTP 429 — return from that attempt. Trying another model requires a later explicit launch by the parent or operator.
- 0.79.x nuance: a verified compaction abort after useful progress may continue the retained child session once on the same resolved model. That lifecycle recovery preserves work and is not model fallback.

## Thinking axis (models.md)

- A thinking level travels on the model string as a `:level` suffix (example: `model=anthropic/claude-sonnet-4:high`).
- `subagents.defaultThinking` fills agents without a `thinking` value (project wins over user). Matching `agentOverrides.<name>.thinking` and per-run thinking overrides replace frontmatter; otherwise explicit frontmatter stays in effect. `thinking: false` is an explicit opt-out. `subagents.disableThinking: true` clears bundled builtin thinking defaults when a provider rejects thinking suffixes.
- `subagents.maxThinking` enforces a hard ceiling; supported levels, least to most: `off`, `minimal`, `low`, `medium`, `high`, `xhigh`, `max`. Requests above the ceiling fail before child startup.
- Watchdog (watchdog.md): the watchdog's `main` model and thinking govern the watchdog's own review call. The watchdog resolves one reviewer model and never switches automatically; it reports unavailability. Watchdog thinking does not change a child's effort.

## Fast mode (models.md)

- `fast: true` requests the OpenAI priority service tier for supported native OpenAI-Codex children. It can use a higher quota tier or cost more; off by default.
- Fast mode fails before launch unless the resolved model is a native `openai-codex/*` model; external runners, Anthropic models, and other providers do not use fast mode. Nothing in the docs establishes it as a remedy for a 429.

## Model scope (models.md)

- `subagents.modelScope` with `enforce: true` errors and aborts runs whose model was passed explicitly (tool-call `model`, `--model`, or a clarify pick). Models from agent frontmatter, `subagents.defaultModel`, or the inherited parent session model only warn by default; `strict: true` with `enforce: true` rejects every resolved out-of-scope model, including inherited ones.
- Model scope is policy only: it rejects or warns and never selects a cheaper model. Project `modelScope` replaces the complete user `modelScope` when the project is trusted.

## Overrides and external runners (models.md, agents.md)

- The same `agentOverrides.<name>` block can also change `tools`, `skills`, inherited context, prompt text, or disable an agent; matching custom-agent frontmatter is replaced for any field the override sets. Runtime-registered agents take only `model`, `defaultProvider`, `fast`, and `thinking` from overrides.
- The Claude Code adapters accept `model` plus a `:level` suffix as their own `--model` and `--effort`; every other external runner refuses both. External CLI agents are deliberate execution modes, not implicit recovery paths for a failed native subagent run; switching runners needs explicit owner approval after the exact failure state is recorded.
