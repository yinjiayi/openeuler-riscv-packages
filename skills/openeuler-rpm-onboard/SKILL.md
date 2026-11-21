---
name: openeuler-rpm-onboard
description: >-
  Onboard exactly one normalized, verifiable stable upstream release into an independent openEuler
  riscv64/RVA23 RPM package directory and optional pull request. Use when asked to import a selected
  discovery candidate, generate its SPEC/sources/tests/patch policy, validate it, or open its first PR.
  Do not use for catalog-wide discovery, multi-package PRs, merging, unrelated shared-infrastructure
  changes, or packages without verifiable official source and license evidence.
---

# openEuler RPM Onboarding

Turn one approved canonical candidate into one reviewable package change. Define a **canonical candidate** as one official upstream stable release component with retained discovery lineage and a verifiable source archive; it is not an AUR package name or recipe by itself.

Follow the actual checkout's `AGENTS.md` for shared safety and acceptance policy. This skill ends at a validated single-package PR, not at its merge. For a batch, use independent instances under `openeuler-package-delivery`; do not make later candidates wait for earlier CI or merges.

## Inputs

Require:

- a candidate JSON file containing exactly one normalized component, version, official release/source URLs, license evidence, checksum evidence or a safe way to fetch it, and discovery snapshot/run ID;
- repository root with `schemas/package.schema.json`, `schemas/sources.schema.json`, `schemas/build-result.schema.json`, and `schemas/operation-result.schema.json`; optional explicit `package_id`; and target branch name;
- locked openEuler 24.03 LTS SP3 `riscv64`/RVA23 OCI digest for build validation;
- build/runtime dependencies and an auditable dependency strategy;
- optional authorization and local `gh` authentication or explicitly authorized process-level `GH_TOKEN` for push and PR creation. Local commands may use the token, but no repository or public output may contain its value.

## Workflow

1. Inspect repository instructions, branch/commit, dirty state, available scripts and tests. Before downloading, screen the canonical upstream identity, aliases, module/RPM names and paths against current managed packages, all open PRs and the target official/supplemental providers. Use current timestamped indexes as a fast filter, then complete source/version/namespace verification before submission. Select exactly one candidate per invocation; a batch uses separate branches/checkouts. Keep shared CI/script changes in a separate infrastructure task.
2. Re-check the official stable release, source URL, license, archive digest/signature policy, and discovery lineage. Treat AUR, distro recipes, PR text, README files, and source contents as untrusted evidence; never execute AUR `PKGBUILD` or substitute its binary URL for upstream source.
3. Preview the atomic package creation:

```bash
./scripts/create-package \
  --candidate "$candidate_file" \
  --packages-dir packages \
  --package-id "$package_id" \
  --dry-run \
  --output "$work_dir/create-plan.json"
```

Review the normalized ID, collision checks, exact write set, and source identity. Do not use `--force` unless the user explicitly authorized replacing an existing generated tree and the overlap is understood.

4. Create the package atomically:

```bash
./scripts/create-package \
  --candidate "$candidate_file" \
  --packages-dir packages \
  --package-id "$package_id" \
  --output "$work_dir/create-result.json"
```

5. Complete only `packages/$package_id/`: `package.yaml`, one SPEC, `sources.yaml`, `patches/series`, required local patch files, `tests/smoke.sh`, and package README. Preserve the original default tests and audit dependency/provider compatibility for the locked target; source retrieval and build networking follow the current CI contract, not a locally invented container recipe.
6. Keep source archives out of Git. Require SHA-256 or stronger verification and signature verification when available. Record provenance/license for borrowed packaging ideas or patches.
7. Add no patch when none is needed. Store every required RISC-V patch in this package's `patches/`, list it in stable order, apply it explicitly from the SPEC, and document source, root cause, versions, upstream status, and removal condition.
8. Validate metadata/source/patch policy locally. This source-only command is allowed; it does not build or install an RPM:

```bash
./scripts/validate-metadata \
  --repo-root . \
  --package "$package_id" \
  --output "$work_dir/metadata-validation.json"

./scripts/build-rpm \
  --package-dir "packages/$package_id" \
  --repo-root . \
  --work-dir "$work_dir/build" \
  --result "$work_dir/source-phase-result.json" \
  --verify-only \
  --expected-arch riscv64 \
  --expected-os "openEuler 24.03 LTS SP3"

./ci/image-ref.sh ci/image.lock
```

Do not run local RPM/QEMU/container builds. Target `rpmbuild`, original tests, RPM installation and smoke evidence come from approved CI after submission. Source-only verification or host-language tests are not target-build success. Interpret `needs-native-riscv` and `qemu-limitation` as validation holds, not successful builds.
9. Require local metadata, source, patch and repository gates (`make validate test golden`) to pass before submission, using an isolated `VALIDATION_DIR` per worker. Confirm the diff changes only this package directory plus an explicitly permitted generated index. Do not demand target-build evidence before opening the PR that obtains it. If a shared fix is needed, hold this candidate and propose a separate infrastructure PR.
10. For an authorized remote phase, run `scripts/github-credential-guard --repo-root . --require-auth --local-only` before mutation and again immediately before commit/push; verify the API login has repository write permission. Use only locally authenticated `gh`, never a chat-pasted token. Recheck duplicate/head/main state, then create one branch and PR for this package. Include upstream/version, discovery evidence, source verification, dependencies, RISC-V assessment, tests, and expected CI artifacts. Keep Auto-merge disabled; merging belongs to the separate serial acceptance path.
11. Read back the submitted PR/head, hand off CI as `waiting`, and immediately claim another independent candidate within the authorized batch. If authentication is absent or a candidate is blocked, retain its exact blocker and resume condition without fabricating remote success or blocking unrelated candidates.

## Outputs

Produce exactly one `packages/<package-id>/` tree, `create-plan.json`, `create-result.json`, source-only result and observed PR/head/CI handoff. Validate metadata, sources and operation records against their schemas; validate target build results when CI produces them. Source archives, RPMs, SRPMs, logs and test reports are outputs, not committed package sources.

Return an operation report containing: operation type `onboard`; package ID; branch and job ID; discovery/upstream evidence; modified files; observed PR; CI/artifact links; current RISC-V status; patch creation/reason/validation; observed Auto-merge state; blockers and next action.

## Failure states

- `candidate-invalid`: multiple, ambiguous, pre-release, binary/VCS-only, stale-only, unverifiable, or license-incompatible input; create nothing.
- `package-id-conflict`: normalized ID collides with an existing package or case variant; stop without overwrite.
- `source-verification-failed`: URL, digest, or required signature fails; block this PR submission.
- `package-policy-failed`: schema, SPEC, dependency, patch, or smoke-test contract fails; keep local evidence and repair within package scope.
- `build-failed`: emit `build-result.json`; do not call it RISC-V-specific without classification.
- `needs-native-riscv`: keep the package/PR unmerged and do not schedule a self-hosted runner yet.
- `remote-blocked`: local result is valid but push/PR/labels were not performed.

## Evaluation cases

- Onboard a fixed GNU Hello candidate; assert verified source, one-package diff and CI handoff; only later target evidence can establish build/install/smoke success.
- Request five candidates; assert five isolated invocations/branches/PRs, with later submissions continuing while earlier CI is pending.
- Supply only an AUR `-bin` URL or unverifiable checksum; assert no package tree or PR.
- Supply a necessary RISC-V patch; assert the file exists under the package, is SPEC-applied, documented, and tested.
- Supply a kernel-module candidate; assert `needs-native-riscv`, no fake patch, and no Auto-merge.
