---
name: openeuler-package-dashboard
description: >-
  Aggregate package metadata, GitHub PR/check/workflow facts, build-result artifacts, and daily update
  summaries into a validated static GitHub Pages dashboard. Use to generate or refresh the package board,
  diagnose stale/partial dashboard data, audit status links, or prepare Pages output. Do not edit package
  build conclusions, infer success from Codex text, conceal incomplete coverage, or mutate PR/CI state.
---

# openEuler Package Dashboard

Generate a read-only view over authoritative facts. Define a **package lifecycle state** as the latest observable PR/check/workflow state for the relevant commit; define **RISC-V status** separately as architecture validation evidence. Neither may be inferred from narrative text.

## Inputs

Require:

- repository root with `packages/*/package.yaml` and `schemas/dashboard.schema.json`;
- optional read-only GitHub state snapshot for PRs, checks, workflow runs, URLs, timestamps, and head SHAs;
- directory of structured build results and the latest daily update summary;
- output directory, generation timestamp, and repository identity `yinjiayi/openeuler-riscv-packages`.

Authoritative sources are: GitHub PR API for PR state; Checks/Actions for CI state; package metadata/SPEC for packaged version; latest update result for upstream version; and required checks for the latest target commit for RISC-V build state.

## Workflow

1. Inspect repository instructions, committed schema, generator interface, output location, and prior dashboard artifacts. Generate into a fresh directory so stale files cannot masquerade as current output.
2. Collect GitHub data with read-only credentials or consume a versioned fixture/snapshot. Record fetch time, repository, API errors, pagination completeness, and the queried head SHA. Do not place tokens in files, logs, cache, or generated Pages.
3. Validate all input shapes and correlate facts by package ID, PR number, and head SHA. Ignore old successful checks when a newer head exists. Mark missing or conflicting evidence as stale/unknown rather than choosing a favorable result.
4. Generate the static site:

```bash
./scripts/generate-dashboard \
  --repo-root . \
  --output-dir "$dashboard_output_dir" \
  --github-state "$github_state_file" \
  --build-results "$build_results_dir" \
  --update-summary "$update_summary_file" \
  --now "$generated_at"
```

Omit an optional flag only when that data source is intentionally unavailable; require the generated site to show a partial/stale-data warning and source timestamp in that case.
5. Display lifecycle states `discovered`, `pr-open`, `ci-queued`, `building`, `repair-queued`, `codex-repairing`, `failed`, `needs-native-riscv`, `needs-human`, `passed`, and `merged`.
6. Display RISC-V status independently as `unknown`, `qemu-buildable`, `native-verified`, `patched-for-riscv`, `qemu-limitation`, or `unsupported`. Do not translate `needs-native-riscv` into `unsupported` or `passed`.
7. For every package, include name, packaged/latest upstream version, last successful upstream-check time, discovery sources, PR/check links, last build, RISC-V status, patch count, latest error, and update time. Support filters for lifecycle state, source, version lag, patch presence, failure category, and freshness.
8. Show daily-update health: scheduled/actual start/end, expected/checked counts, coverage, failed/missing shards, backfill count, last successful daily run, and consecutive missed days. Never claim full coverage when the summary is partial.
9. Validate generated JSON against `schemas/dashboard.schema.json`, parse every JSON asset, check internal files/links, and smoke-test the static index. A dashboard generation failure must not modify a package's build state.
10. Publish only through the repository's reviewed Pages workflow after validation. Treat publication as successful only when the Pages deployment and resulting public URL are observed. Without remote access, deliver local static output and report Pages as blocked.

## Outputs

Produce a static `index.html`, assets, machine-readable dashboard data, validation results, and source/freshness metadata. Validate dashboard data and the operation report against `schemas/dashboard.schema.json` and `schemas/operation-result.schema.json`. Keep raw API/build/update evidence outside the published site when it may contain untrusted or sensitive content; render it as escaped text or safe links only.

Return an operation report containing: operation type `dashboard`; catalog-wide target; branch/workflow/job ID; input evidence/fetch times; generated files; no package PR mutation; Pages/build artifact links; summarized RISC-V states; no Codex patch; Auto-merge facts only; data gaps and next refresh action.

## Failure states

- `input-invalid`: metadata, API snapshot, build result, or update summary fails validation; stop publication.
- `fact-conflict`: head SHA/status sources disagree; show unknown/stale and retain diagnostic evidence.
- `data-partial`: pagination, API, build, or shard evidence is missing; generate only with a visible incomplete-data warning.
- `output-invalid`: schema, JSON, link, or index smoke validation fails; do not deploy.
- `pages-blocked`: local output validates but deployment/URL was not observed.

## Evaluation cases

- Aggregate fixtures spanning all lifecycle and RISC-V statuses; assert independent rendering and working filters/links.
- Present an old successful check plus a failing latest head; assert the package is not shown passed/mergeable.
- Omit one daily shard; assert reduced coverage, missing-shard/backfill indicators, and no 100% claim.
- Omit GitHub input; assert local generation is marked partial/stale rather than inventing PR/CI facts.
- Inject HTML/script text into an upstream error; assert escaped rendering and no executable content.
