# Pi native operations runbook

Use only the section matching the authorized mode. Commands evolve: confirm against the upstream pi-subagents `docs/` (`models.md`, `agents.md`, `tool-reference.md`) at the installed version instead of treating examples as frozen.

## Inventory and access

### Allowlisted reads

- Settings routing keys only: `subagents.defaultModel`, `subagents.defaultProvider`, `subagents.defaultThinking`, `subagents.maxThinking`, `subagents.disableThinking`, `subagents.modelScope`, and within `subagents.agentOverrides` / `subagents.agentOverridesByProvider` only the nested `model`, `defaultProvider`, `thinking`, and `fast` fields — never the prompt, tools, skills, or context fields an override block can also carry. Plus top-level `defaultModel` and `enabledModels` IDs. Never print raw `settings.json`, auth files, `models.json` bodies, or environment dumps; record hashes when change-detection matters.
- `/subagents-models` (or tool `{ action: "models" }`) reports the live runtime mapping. It can differ from settings on disk until Pi reloads; record which one you read and reconcile discrepancies before recommending.
- Agent frontmatter in the installed package (`agents/*.md`) for builtin `model`/`thinking` pins; list the pi-subagents profiles directory under your Pi agent settings directory for saved profiles and cached provider catalogs.

### Commands that infer or mutate — never in audit mode

| Command | Effect |
|---|---|
| `/subagents-refresh-provider-models` | Writes the provider catalog cache; default path probes each model via `pi -p`. |
| `/subagents-generate-profiles` | Calls refresh, then writes `*.quota.json` / `*.quality.json` profiles. |
| `/subagents-load-profile` | Rewrites user `settings.json` `subagents.agentOverrides`. |
| `/subagents-check-profile` | Live-probes every assigned model in a saved profile. |
| `pi update --models` | Network catalog fetch plus cache write; not inference, but a mutation. |
| `/login`, `/logout`, agent `create`/`disable`/`enable`/`reset`/`update` | Credential or agent-file mutation. |

Their names do not establish metadata-only behavior; do not run them to "check" anything during an audit. Mark quota and entitlement unknown and ask for a redacted usage panel when the missing fact changes the recommendation.

### Keep evidence columns distinct

| Evidence | Establishes | Does not establish |
|---|---|---|
| Saved auth entry | A credential exists | Current plan, valid key, entitlement, quota, billing class |
| Registry/`enabledModels` entry | The client knows an exact route | That the account can call it |
| Owner's dated plan statement | A subscription existed then | Today's remaining allowance or model coverage |
| Successful bounded probe | That route worked at that time | Other model access, durable availability, unlimited quota |
| Registry cost of zero | Catalog metadata | Free usage under the actual plan |

## Benchmark evidence

1. Fetch current primary pages (Artificial Analysis model/release/comparison and methodology pages; official vendor docs for the IDs, context, effort enums, and list prices you cite). Record URL, retrieval date, and index version per claim. Search snippets are not numeric proof.
2. Keep only exact verified scores. Note which cells came from page JSON versus display versus secondary extracts, and mark un-verified cells as lower confidence.
3. Map every chart display name to an exact `provider/model` registry ID before recommending. Unmapped names stay unresolved; never route on a score whose registry ID is unproven. Local models without public benchmarks stay unverified.
4. Compare like with like: effort-specific scores only against the same effort; native coding-harness agent scores are not Pi subagent scores; API list prices are not subscription marginal costs; thinking-level names in Pi are not proven equal to a vendor's effort enum until the mapping is documented locally.

## Bounded probes

Live inference consumes quota and needs explicit authorization naming the routes and a budget. An audit request is not that authorization.

1. Launch through the governed subagent lane with an explicit per-run `provider/model:level` override, and confirm its precedence against the installed pi-subagents documentation. This pins the extension's selected route, not necessarily a virtual router's physical dispatch: inspect any configured virtual router and verify the resolved physical model and thinking level. Stop if route attribution cannot be established. If the lane fails, stop and report; do not fall back to shell/CLI execution-mode workarounds.
2. Bound every probe measurably before launching: a minimal fixed prompt, a small output cap the provider supports, a wall-clock bound, and at most one retry on transient transport errors. Stop if any bound cannot be enforced.
3. Isolate: launch with explicit `context: "fresh"` and verify the effective context-inheritance settings — an agent `defaultContext` or a global `defaultSubagentContext` can otherwise fork the parent transcript into the probe. Require an approved effective extension allowlist: background children load ambient parent extensions by default, and `subagentOnlyExtensions` or path-based entries load executable code alongside an explicit list. Allow no tools beyond the declared allowlist, no watchdog or nested children unless the probe explicitly targets them, and no inherited project settings surprises (project settings override user). Do not edit settings merely to enable a probe. Stop if context, extension, or tool isolation cannot be enforced.
4. Attribute: record the requested route, the resolved route as reported, outcome, and error class. A 429 proves a rate/quota rejection at that moment, not exhausted subscription quota. Stop and report on auth/quota failures; document alternative models only as unverified candidates for a separately approved explicit retry.
5. Record consumption only when reported or defensibly calculated; a displayed zero API cost is not zero plan credits.

## Apply and verify

1. Confirm the approved mapping and scope. Approval to edit user settings does not cover project settings, agent frontmatter, or per-run overrides; approval to probe is not approval to apply.
2. Re-read the live file immediately before editing. Capture a private rollback copy of the exact targeted state. If the target fields changed since approval (concurrent edits), stop and re-confirm.
3. Merge only the approved keys, preserving unrelated settings, comments, and file permissions. Keep route and thinking changes paired; a model change without a deliberate effort choice is incomplete. Respect `maxThinking` ceilings and `modelScope` as documented upstream at the installed version — with `enforce: true`, explicitly passed out-of-scope models are rejected, while inherited, frontmatter, and default models only warn unless `strict: true` is also set.
4. Verify without inference: re-read the saved fields, then compare against the live `/subagents-models` mapping after reload. Disk and live can differ until reload; report which was verified.
5. Report old-to-new assignments per role, untouched files, remaining unknowns, and the reload requirement. Do not terminate running sessions; existing sessions keep their resolved models.

## Source entry points

- Upstream [pi-subagents](https://github.com/nicobailon/pi-subagents) documentation at the installed version: `docs/models.md` (precedence, thinking, fast, modelScope, profiles), `docs/agents.md` (frontmatter, external adapters), `docs/tool-reference.md`, `docs/watchdog.md`.
- Pi core docs shipped inside the installed Pi release: `docs/skills.md` (skill discovery/loading), `docs/packages.md` (packaging and `pi install`), `docs/settings.md`, `docs/virtual-models.md`.
- [Artificial Analysis intelligence benchmarking methodology](https://artificialanalysis.ai/methodology/intelligence-benchmarking) and the model pages you cite; official vendor docs for the exact IDs, effort enums, and list prices in your recommendation.
