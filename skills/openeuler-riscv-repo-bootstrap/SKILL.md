---
name: openeuler-riscv-repo-bootstrap
description: >-
  Bootstrap or audit the openEuler 24.03 LTS SP3 riscv64/RVA23 package repository, including schemas,
  shared scripts, pinned GitHub Actions, reproducible QEMU/OCI configuration, golden fixtures, Skills,
  Auto-merge policy, and Pages scaffolding. Use for initial repository creation, M0 readiness checks,
  or infrastructure-only repairs. Do not use to bulk-onboard real packages or claim remote resources
  were created when their creation was not observed.
---

# openEuler RISC-V Repository Bootstrap

Build and verify the infrastructure milestone before enabling M1 package onboarding. Define **M0 readiness** as locally valid repository contracts plus observed target-environment evidence; it does not mean GHCR, Pages, rulesets, or a GitHub repository exist unless those remote operations succeeded.

## Inputs

Require:

- target repository root and intended remote `yinjiayi/openeuler-riscv-packages`;
- target OS `openEuler 24.03 LTS SP3`, architecture `riscv64`, ISA profile `RVA23`;
- rootfs repository `https://repo.openeuler.org/openEuler-24.03-LTS-SP3/everything/riscv64/rva23/riscv64/`;
- image tag `ghcr.io/yinjiayi/openeuler-riscv64-rpmbuild:24.03-lts-sp3-rva23` and an immutable digest before package CI can consume it;
- execution mode: local-only by default, or explicitly authorized remote configuration with local `gh` authentication/process-level `GH_TOKEN`.

## Workflow

1. Before generation or an evidence-producing run, record host name/IP, disk and memory availability, CPU, OS/kernel, package manager, QEMU/container/RPM/Python/Git versions, current branch/commit, and dirty worktree. Inspect local `AGENTS.md`, rules, README, tests, and dependency conventions.
2. Isolate stale work/build/result directories. Preserve caches only when a test explicitly measures warm or incremental behavior.
3. Materialize or repair the required repository areas: the package, image, discovery, update, missed-schedule monitor, golden, Auto-merge, and dashboard workflows under `.github/workflows/`; PR template and CODEOWNERS; `packages/_template/`; `catalog/`; `ci/`; shared `scripts/`; versioned `schemas/`; all three `tests/golden/` fixtures; six `skills/`; and static `dashboard/`. Preserve unrelated user changes and use Apache-2.0 only for original repository code/documentation, not third-party sources or incompatible patches.
4. Keep target-defining values reviewable in `ci/build-config.yaml`, `ci/openeuler-rva23.repo`, and `ci/image.lock`. Reject RVA20, cross-compiled x86 containers, another distribution, a mutable tag without digest, or a repo URL substitution.
5. Verify each shared executable exposes the committed interface and never relies on hidden conversation state:

```bash
for tool in snapshot-catalog discover-packages resolve-upstream create-package validate-metadata \
  check-update build-rpm classify-failure watch-failed-prs claim-repair github-credential-guard generate-dashboard \
  golden-eval evaluate-golden; do
  "./scripts/$tool" --help
done
```

6. Validate JSON schemas, package fixtures, workflow syntax, script tests, and repository policy. Run `scripts/validate-metadata --repo-root . --output "$validation_dir/metadata.json"` and require a valid result. Require full-SHA pinning for third-party Actions, job-scoped least privilege, explicit timeouts/concurrency, and `retention-days: 7` on every applicable artifact upload. Do not introduce artifact size/total-budget policy yet.
7. Inspect every workflow for `OPENAI_API_KEY`, Codex secrets, Codex execution, write credentials in untrusted build jobs, `pull_request_target` misuse, and self-hosted runner scheduling. Fail the audit if any is present. Keep native-only packages in `needs-native-riscv`.
8. Build the CI rootfs only from the fixed RVA23 repository. Record `repomd.xml` digest, installed RPM manifest, Containerfile/build-config revisions, QEMU version, build time, image digest, and the results of `uname -m`, RPM arch, OS release, and representative RVA23 execution checks. Do not lower the ISA target when QEMU fails.
9. Exercise the locked environment through `scripts/build-rpm` and evaluate the fixed manifests after result files exist:

```bash
./scripts/evaluate-golden \
  --manifests-dir tests/golden \
  --results-dir "$golden_results_dir" \
  --archives-dir "$golden_archives_dir" \
  --stage auto \
  --output "$golden_results_dir/evaluation.json"
```

Require `golden-success-hello` to build/install/smoke without a patch, `golden-riscv-inline-asm` to fail first and pass only after the expected minimal local repair, and `golden-needs-native-kmod` to remain blocked for native validation without a fake patch.
10. Treat remote setup as a separate, externally visible phase. Proceed only when authorized and authenticated. An explicitly authorized `GH_TOKEN` may be used by local `gh`/GitHub commands through the current process; token use itself is permitted. Before mutation and again before commit/push, run `scripts/github-credential-guard --repo-root . --require-auth --local-only`. Never place the value in arguments, files, commits, PR text, logs, artifacts, Actions secrets/variables, Pages, or any other public output. Create/configure the public repo, branch ruleset with zero required approvals, squash Auto-merge, Pages, and public GHCR package, then verify each through independent reads. Do not report success from command intent alone.
11. Stop at the M0 gate until the exact OCI digest and target checks are observed. Begin M1 only after the golden cases, scheduled-update contracts, repair lease/head guard, and no-Codex-in-Actions checks pass.

## Outputs

Produce the complete local skeleton, validation/golden results, reproducibility records, and immutable image lock when available. Update the existing project tracking/plan documents rather than creating redundant reports.

Return an operation report with operation `bootstrap`, validated against `schemas/operation-result.schema.json`, containing: infrastructure target; branch and job ID; config/repository evidence; modified files; observed remote repo/PR/Pages/GHCR links or explicit remote blockers; CI/artifact links; golden RISC-V states; patch evidence; Auto-merge configuration state; blockers and next milestone.

## Failure states

- `local-contract-invalid`: schema, script, fixture, workflow, or license validation failed; M0 is not ready.
- `target-environment-mismatch`: any OS/arch/ISA/repo self-check differs; stop without fallback.
- `image-unlocked`: public image digest is missing or anonymous pull was not verified; package CI remains blocked.
- `golden-gate-failed`: any fixed case reaches the wrong state; preserve raw evidence and diagnose before M1.
- `remote-blocked`: authorization/authentication is absent; deliver verified local work and list repo/ruleset/Pages/GHCR/push blockers.
- `remote-partial`: a remote operation failed verification; report only the resources actually observed.

## Evaluation cases

- Run local-only with no token; assert the repository validates and no remote resource is claimed.
- Inject an RVA20 repo or mutable-only image reference; assert M0 fails.
- Add a Codex/OpenAI secret reference or unpinned third-party Action; assert policy validation fails.
- Evaluate all three golden manifests; assert their three distinct expected paths.
- After an authorized remote run, independently verify public repository, ruleset, Pages, anonymous GHCR pull, and digest-based CI use before marking each complete.
