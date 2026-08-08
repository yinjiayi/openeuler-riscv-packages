---
name: openeuler-rpm-update
description: >-
  Plan, shard, scan, aggregate, and apply official stable upstream release checks for every managed,
  non-retired RPM, producing idempotent one-package update changes and optional pull requests. Use for
  the daily default-branch schedule, missed-run backfill, a single-package stable update check, or scan
  summary diagnosis. Do not create empty PRs, select prerelease/nightly/VCS heads, duplicate a package-version
  PR, combine packages in one PR, or run Codex inside GitHub Actions.
---

# openEuler RPM Update

Check the complete eligible package snapshot and preserve enough evidence to distinguish no update, update, failure, skip, and missed coverage. Define an **idempotency key** as `update:package_id:target_version`; every update decision and PR must reuse it.

## Inputs

Require:

- repository root, all `packages/*/package.yaml` records, `schemas/update-run.schema.json`, and `schemas/operation-result.schema.json`;
- prior update state file, output/run directory, and unique `update_run_id`;
- shard size, default 100; per-host rate/concurrency limits; retry budget; and missed threshold, default 24 hours;
- stable upstream release policies and cached ETag/Last-Modified data when available;
- optional remote PR authorization available to the workflow/local process without Codex/OpenAI secrets.

## Workflow

1. Run only the scheduled workflow from the default branch for normal daily coverage. Record the visible UTC cron/time-zone convention and actual start time. Use `workflow_dispatch` only for backfill or diagnosis.
2. Build an immutable plan from every managed, non-retired package. Prioritize packages without a successful check in the last 24 hours:

```bash
./scripts/check-update plan \
  --packages-dir packages \
  --state "$state_file" \
  --output "$run_dir/plan.json" \
  --run-id "$update_run_id" \
  --shard-size "${update_shard_size:-100}" \
  --missed-after-hours 24
```

3. Scan each planned shard in an isolated output file. Apply bounded timeout, retry with exponential backoff, host rate limiting, and conditional HTTP caching. A single host/package failure must not stop other shards:

```bash
./scripts/check-update scan \
  --plan "$run_dir/plan.json" \
  --shard-index "$shard_index" \
  --output "$run_dir/shard-$shard_index.json" \
  --cache-dir "$cache_dir" \
  --requests-per-second "$requests_per_second" \
  --retries "$retry_count"
```

4. Select only the package's configured official stable release channel. Ignore prerelease, nightly, development branch, and VCS head unless an explicit reviewed package policy allows a nonstandard channel.
5. Aggregate every expected shard result; repeat `--result` once per shard:

```bash
./scripts/check-update aggregate \
  --plan "$run_dir/plan.json" \
  --result "$run_dir/shard-0.json" \
  --result "$run_dir/shard-1.json" \
  --output "$run_dir/summary.json" \
  --state-output "$state_file"
```

Generate the actual argument list from the plan; do not assume two shards. Assert counts for expected, checked, no-update, update, failed, skipped, missing, and backfill-needed packages.
6. For `no-update`, record `last_checked_at`, detected version, and evidence in run/dashboard state only. Do not modify the package directory and do not create a PR.
7. Before applying an update, query open/merged records by idempotency key. Skip an existing same-version update; serialize concurrent shards per package.
8. Apply each unique eligible result to only its package:

```bash
./scripts/check-update apply \
  --result "$package_update_result" \
  --package "$package_id" \
  --packages-dir packages \
  --output "$run_dir/apply-$package_id.json"
```

Review version/source URL/digest/changelog changes and patch applicability. Remove a local patch only when the new stable release demonstrably absorbs it; otherwise rebase and revalidate it.
9. Validate the changed package with `scripts/validate-metadata --repo-root . --package "$package_id" --output "$run_dir/metadata-$package_id.json"`, then build it with `scripts/build-rpm` and the locked riscv64/RVA23 image. For an authorized remote path, create one branch and PR per package/version, attach the idempotency key and labels, and enable policy-controlled Auto-merge. Never combine update changes.
10. Upload the plan, shard results, summary, apply results, failures, and logs with seven-day retention. CI failures may emit structured artifacts and mark trusted internal PRs `repair-queued`; Actions must not start Codex or receive Codex/OpenAI secrets.
11. Mark the daily run incomplete when any planned shard/result is missing. Surface delayed schedules, consecutive missed days, coverage, backfill queue, and the possibility that GitHub disabled an inactive public repository's schedule after 60 days; keep a reviewed re-enable/runbook path. Do not report 100% coverage from partial results.

## Outputs

Produce plan, per-shard results, aggregate summary, idempotent per-package apply results, and zero or more isolated package PRs. Validate the complete run and operation reports against the committed schemas. Emit one catalog-level report with `package_id: null`, then one package-scoped report for each applied update/PR. A zero-PR run is valid when everything is current, but it still requires a complete summary.

Return an operation report with operation `update` containing: affected package IDs or catalog-wide target; branch/job/update run ID; upstream evidence; modified files; observed PRs; CI/artifact links; per-package RISC-V state; patch changes and validation; Auto-merge state; coverage blockers and next backfill/action.

## Failure states

- `plan-invalid`: duplicate package IDs, invalid metadata, or inconsistent prior state; do not scan.
- `scan-partial`: host/package/shard failure; aggregate partial facts and queue missed packages.
- `unstable-release-rejected`: candidate is prerelease/nightly/VCS; record it without applying.
- `duplicate-update`: same idempotency key already exists; do not create another branch/PR.
- `apply-or-build-failed`: preserve structured result and route the trusted PR to normal CI/repair policy.
- `coverage-incomplete`: expected and checked sets differ; show the gap and prioritize it next run.
- `remote-blocked`: local plan/apply output exists but PR operations were not observed.

## Evaluation cases

- Scan an up-to-date package; assert no diff/PR and a refreshed check result.
- Scan one new stable release; assert one package-only update and one idempotency key/PR.
- Retry two shards for the same package/version; assert one apply result and at most one PR.
- Present a prerelease newer than stable; assert it is ignored.
- Omit/fail a shard; assert incomplete coverage, visible missing counts, and next-run backfill after 24 hours.
