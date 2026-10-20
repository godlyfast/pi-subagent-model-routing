# Versioned fixture: Advisor plugin implementation facts (rpiv-advisor 2.13.9)

**Fixture, not live truth.** Frozen tabletop-eval input, extracted 2026-10-20 from a source review of the installed `@juicesharp/rpiv-advisor` 2.13.9 recorded at repository baseline `73a5a3b8ae75003958f45193ee3d2e570c223e55`, so the evals in `evals/evals.json` run offline. Treat it as frozen test truth for the published cases only, never as runtime truth about a live installation: real tasks read the installed plugin's own source and cite its version. A newer plugin version gets a deliberately revised fixture and cases; this file does not get refreshed in place.

## Configuration source and precedence

- Configuration is `rpiv-advisor/advisor.json` under the plugin's XDG configuration root. An absolute or supported tilde-expanded `XDG_CONFIG_HOME` overrides that root; relative or blank values use the default. The legacy default-path file is read only if the primary is missing. A present malformed primary wins and yields a warning/empty result, not a legacy fallback. Report invalid/unreadable separately from an intentionally unset selection.

## Model key and effort

- `modelKey` stores the exact `provider/modelId` (the parser also accepts a documented legacy key format); `effort` is a separate field. Missing effort sends no reasoning option, not an explicit reasoning-off instruction. Restore validates a graded effort enum, and the interactive picker additionally filters the selected model's supported levels. Parsing a file alone proves neither compatibility nor successful restoration.

## Executor blocklist and saved state

- `disabledForModels` is a normalized executor blocklist, optionally with `minEffort` thresholds. It can make the tool inactive while an advisor selection remains saved; it does not exclude that candidate advisor model globally. Invalid entries and unknown thresholds follow the installed validator: report its warnings rather than inventing rules.
- Saved selection, loaded runtime selection, active tool, resolved route/effort, and successful execution are separate evidence; a saved key proves neither activation nor provider health.

## Inspection and side-call execution

- `/advisor` is an interactive configuration picker, not a read-only status command, and it can persist a selection (cancelling at the effort step can save the picked model without explicit effort). Do not invoke it to inspect status; read `modelKey`, `effort`, and normalized disable rules without calling save helpers.
- The side call forwards Pi's resolved conversation branch (including surviving compaction/branch summaries) plus a registered-tool inventory prefix to `completeSimple`, with a separate advisor system prompt and `tools: []`. It is not a native CLI reviewer with filesystem tools, and it is not guaranteed raw or redacted history. Weigh transcript disclosure, context capacity, latency, and repeated consultation quota before recommending.

## Source attribution

Reviewed 2026-10-20 against the installed 2.13.9 source, recorded at repository baseline `73a5a3b8ae75003958f45193ee3d2e570c223e55`. The upstream links below track `main` and are navigation aids only, not a 2.13.9 version pin: [rpiv-advisor documentation](https://github.com/juicesharp/rpiv-mono/tree/main/packages/rpiv-advisor), [docs/configuration.md](https://github.com/juicesharp/rpiv-mono/blob/main/packages/rpiv-advisor/docs/configuration.md), [docs/tool-reference.md](https://github.com/juicesharp/rpiv-mono/blob/main/packages/rpiv-advisor/docs/tool-reference.md). Use installed-version source for operational claims.
