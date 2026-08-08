# openEuler RISC-V Packages

This repository is a reproducible, evidence-backed packaging pipeline for openEuler 24.03 LTS SP3 on `riscv64` with the RVA23 profile. It discovers stable upstream source releases, onboards one RPM per pull request, builds under QEMU user emulation, and keeps RISC-V fixes beside the affected package.

中文摘要：本仓库面向 openEuler 24.03 LTS SP3、`riscv64`、RVA23。它提供六个可组合 Codex Skill、确定性脚本、JSON Schema、GitHub Actions、三个黄金验收包和 GitHub Pages 静态看板。GitHub Actions 不运行 Codex，也不保存 OpenAI/Codex 密钥。

## Defined terms

- A **managed package** is a non-template directory below `packages/` whose `package.yaml` is schema-valid and is not `retired` or `update-disabled`.
- An **upstream release component** is a project unit with its own official stable release and version boundary. Discovery deduplicates this unit, not distribution package names.
- A **build result** is the schema-valid `build-result.json` tied to an exact Git commit SHA. It is evidence, not a self-reported success claim.
- A **repair lease** is an expiring, owner-bound claim on one failed PR head SHA. It prevents two local Codex processes from overwriting each other.
- A **golden package** is a fixed end-to-end fixture with a pinned source/content digest, expected state, allowed changes, and assertions.

## Safety and trust boundary

- Arch stable `core`/`extra` and AUR are primary discovery indexes. AUR data is untrusted metadata: no workflow executes a `PKGBUILD`.
- Pure AUR `-bin` entries and entries older than 730 days are excluded by default. VCS/nightly variants are discovery clues only.
- Supplementary discovery resolves the current stable openSUSE Tumbleweed snapshot, latest Fedora GA, Debian `stable`, and latest Ubuntu GA release in standard support. Rawhide, testing/unstable, staging, multilib, development, and prerelease feeds are excluded.
- Sources come from verified official upstream release/tag URLs. `rpmbuild` runs without network after source verification.
- Required native-kernel or hardware validation becomes `needs-native-riscv`; no self-hosted runner is currently scheduled.
- Repair runs only on a maintainer's local Codex through local `gh` authentication or process-scoped `GH_TOKEN`. CI only uploads structured failure evidence and labels a trusted internal PR `repair-queued`.
- Automation never writes to upstream projects. RISC-V patches remain in `packages/<id>/patches/` and are referenced by the SPEC.

## Repository map

| Path | Purpose |
|---|---|
| `skills/` | Six composable Codex Skills and their contracts |
| `scripts/` | Deterministic discovery, onboarding, build, update, repair, and dashboard tools |
| `schemas/` | Versioned machine contracts for packages, sources, builds, updates, repair leases, and dashboards |
| `ci/` | Exact openEuler repository config, rootfs-to-OCI build, QEMU/RVA23 checks, and image digest lock |
| `packages/` | One directory per managed package plus `_template` |
| `tests/golden/` | Fixed success, repair, and native-only acceptance fixtures |
| `catalog/` | Discovery source policy and immutable run snapshots |
| `dashboard/` | Static Pages application and generated evidence |

## Local verification

Python 3.9 or newer is sufficient for repository metadata tests. Docker/QEMU is required only for the target-architecture build gate.

```sh
make validate
make test
make golden
make dashboard
```

Verify and materialize one package's pinned source without building it:

```sh
scripts/build-rpm \
  --package-dir packages/golden-success-hello \
  --repo-root . \
  --work-dir work/golden-success-hello \
  --result artifacts/golden-success-hello-source.json \
  --verify-only
```

The full build is intentionally run by `package-ci.yml` inside the locked RISC-V OCI, after a separate audited BuildRequires stage, with `--offline` and container networking disabled.

Replay discovery against saved fixture metadata without executing external packaging code:

```sh
scripts/discover-packages \
  --config catalog/sources.yaml \
  --input arch=tests/fixtures/discovery/arch.json \
  --input aur=tests/fixtures/discovery/aur.json \
  --input opensuse=tests/fixtures/discovery/opensuse.json \
  --input fedora=tests/fixtures/discovery/fedora.json \
  --input debian=tests/fixtures/discovery/debian.json \
  --input ubuntu=tests/fixtures/discovery/ubuntu.json \
  --as-of 2026-08-08T00:00:00Z \
  --output catalog/snapshots/local.json
```

For a live run, call `scripts/snapshot-catalog` first. It resolves each configured stable distribution, verifies and records the metadata URLs/digests, and writes frozen per-source JSON consumed by `scripts/discover-packages`. The `Catalog Discovery` workflow performs both stages.

Onboard and update commands are deliberately one-package/one-PR operations. Use `--dry-run` before remote writes.

## CI image invariant

The build image tag is `ghcr.io/yinjiayi/openeuler-riscv64-rpmbuild:24.03-lts-sp3-rva23`. Its root filesystem must be constructed only from:

```text
https://repo.openeuler.org/openEuler-24.03-LTS-SP3/everything/riscv64/rva23/riscv64/
```

Package CI reads an immutable digest from `ci/image.lock`; a mutable tag is never accepted as build evidence. Image publication records the `repomd.xml` digest, installed RPM manifest, OCI digest, QEMU version, and RVA23 probe result.

## Auto-merge policy

Repository rules require the latest head SHA to pass `metadata-validate`, `source-verify`, `rpmbuild-riscv64`, `rpm-install-smoke`, and `patch-policy`. Required approvals are zero. Blocking labels, source/license/checksum failures, `needs-human`, and `needs-native-riscv` prevent merge even if unrelated checks passed.

## License scope

Original repository code, Skills, workflows, schemas, and documentation are licensed under Apache-2.0; source files use `SPDX-License-Identifier: Apache-2.0` where their syntax permits. This does not relicense upstream sources or imported patches. Each third-party or derived patch must record its source, original license, root cause, applicable versions, upstream status, and removal condition in package metadata and its patch header.

## Current limits

QEMU user mode is not native hardware validation. Kernel modules, eBPF, boot/systemd, privileged syscall behavior, devices, timing-sensitive concurrency, and performance claims remain native-only. Artifacts are retained for 7 days; this MVP intentionally sets no custom per-artifact or aggregate storage budget beyond GitHub account limits.
