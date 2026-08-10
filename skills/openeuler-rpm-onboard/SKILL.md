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

## Inputs

Require:

- a candidate JSON file containing exactly one normalized component, version, official release/source URLs, license evidence, checksum evidence or a safe way to fetch it, and discovery snapshot/run ID;
- repository root with `schemas/package.schema.json`, `schemas/sources.schema.json`, `schemas/build-result.schema.json`, and `schemas/operation-result.schema.json`; optional explicit `package_id`; and target branch name;
- locked openEuler 24.03 LTS SP3 `riscv64`/RVA23 OCI digest for build validation;
- build/runtime dependencies and an auditable dependency strategy;
- optional authorization and local `gh` authentication or explicitly authorized process-level `GH_TOKEN` for push and PR creation. Local commands may use the token, but no repository or public output may contain its value.

## Workflow

1. Inspect repository instructions, branch/commit, dirty state, available scripts and tests, and target package-ID collisions. Refuse an input containing multiple candidates. Keep shared CI/script changes in a separate infrastructure task.
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

5. Complete only `packages/$package_id/`: `package.yaml`, one SPEC, `sources.yaml`, `patches/series`, required local patch files, `tests/smoke.sh`, and package README. Use all required SPEC sections and a deterministic offline `rpmbuild` dependency strategy.
6. Keep source archives out of Git. Require SHA-256 or stronger verification and signature verification when available. Record provenance/license for borrowed packaging ideas or patches.
7. Add no patch when none is needed. Store every required RISC-V patch in this package's `patches/`, list it in stable order, apply it explicitly from the SPEC, and document source, root cause, versions, upstream status, and removal condition.
8. Validate metadata/source/patch policy and materialize the verified sources before exercising the exact locked target:

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

Run the dependency preparation plus offline/no-network container build exactly as `package-ci.yml` does; never run the target build directly on the host or give the build phase network access. Require source verification, `rpmbuild -ba`, RPM installation, and the committed smoke test. Interpret `needs-native-riscv` and `qemu-limitation` as target-validation states, not successful QEMU builds.
9. Require both metadata validation and build checks to pass. Confirm the diff changes only this package directory plus an explicitly permitted generated index. If a shared fix is needed, stop and propose a separate infrastructure PR.
10. For an authorized remote phase, run `scripts/github-credential-guard --repo-root . --require-auth --local-only` before mutation and again immediately before commit/push. A user-authorized process-level `GH_TOKEN` may authenticate local `gh`/GitHub operations; never put its value in arguments, files, commits, PR text, logs, artifacts, Actions configuration, Pages, or other public output. Create one branch and one PR for this package. Include upstream/version, discovery evidence, source verification, dependencies, RISC-V assessment, files, tests, and artifact expectations. Apply operation/source/package/status labels. Enable squash Auto-merge only when policy permits; never merge directly.
11. If authentication is absent, finish and validate the local package, then report branch/push/PR/label/Auto-merge as remote blockers without fabricating them.

## Outputs

Produce exactly one `packages/<package-id>/` tree, `create-plan.json`, `create-result.json`, and structured build result. Validate package metadata, sources, build result, and operation report against their committed schemas. Any source archives, RPMs, SRPMs, logs, and test reports are build outputs rather than committed package sources.

Return an operation report containing: operation type `onboard`; package ID; branch and job ID; discovery/upstream evidence; modified files; observed PR; CI/artifact links; current RISC-V status; patch creation/reason/validation; observed Auto-merge state; blockers and next action.

## Failure states

- `candidate-invalid`: multiple, ambiguous, pre-release, binary/VCS-only, stale-only, unverifiable, or license-incompatible input; create nothing.
- `package-id-conflict`: normalized ID collides with an existing package or case variant; stop without overwrite.
- `source-verification-failed`: URL, digest, or required signature fails; block PR/Auto-merge.
- `package-policy-failed`: schema, SPEC, dependency, patch, or smoke-test contract fails; keep local evidence and repair within package scope.
- `build-failed`: emit `build-result.json`; do not call it RISC-V-specific without classification.
- `needs-native-riscv`: keep the package/PR unmerged and do not schedule a self-hosted runner yet.
- `remote-blocked`: local result is valid but push/PR/labels/Auto-merge were not performed.

## Evaluation cases

- Onboard a fixed GNU Hello candidate; assert no patch, verified source, successful riscv64 build/install/smoke, and one-package diff.
- Request five candidates; assert this invocation refuses batching and requires five isolated runs/branches/PRs.
- Supply only an AUR `-bin` URL or unverifiable checksum; assert no package tree or PR.
- Supply a necessary RISC-V patch; assert the file exists under the package, is SPEC-applied, documented, and tested.
- Supply a kernel-module candidate; assert `needs-native-riscv`, no fake patch, and no Auto-merge.
