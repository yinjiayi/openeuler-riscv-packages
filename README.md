# openEuler RISC-V Packages

This repository is a reproducible, evidence-backed packaging pipeline for openEuler 24.03 LTS SP3 on `riscv64` with the RVA23 profile. It discovers stable upstream source releases, onboards one RPM per pull request, builds under QEMU user emulation, and keeps RISC-V fixes beside the affected package.

中文摘要：本仓库面向 openEuler 24.03 LTS SP3、`riscv64`、RVA23。它提供六个可组合 Codex Skill、确定性脚本、JSON Schema、GitHub Actions、三个黄金验收包和 GitHub Pages 静态看板。GitHub Actions 不运行 Codex，也不保存 OpenAI/Codex 密钥。

## Defined terms

- A **managed package** is a non-template directory below `packages/` whose `package.yaml` is schema-valid and is not `retired` or `update-disabled`.
- An **upstream release component** is a project unit with its own official stable release and version boundary. Discovery deduplicates this unit, not distribution package names.
- A **verified release source** is an HTTPS official stable release/tag archive whose exact bytes are pinned by a full SHA-256. Distribution package checksums and catalog metadata digests do not satisfy this definition.
- **Reviewed upstream evidence** is a schema-valid mapping from one component in an immutable discovery snapshot to its official stable release page, source repository, release feed/index, exact archive SHA-256, license evidence, and archive-safety inspection. It supplements missing catalog fields; it does not execute or trust distribution recipes. Document-level `reviewed_at` records completion of that overlay revision, while each release's `evidence.verified_at` records when its archive bytes were verified.
- A **lineage promotion** is a reviewed selector that maps one exact raw lineage row in an immutable snapshot to a canonical official upstream component. It records the frozen component key, distribution source, original name, package base, version, and relationship; it neither rewrites the snapshot nor turns AUR metadata or a functional provider into source evidence.
- A **build result** is the schema-valid `build-result.json` tied to an exact Git commit SHA. It is evidence, not a self-reported success claim.
- A **network-enabled target build** is a target-architecture build container with
  outbound Docker bridge networking. It may retrieve only the declared sources;
  each source remains bound to its committed SHA-256 and is verified before
  `rpmbuild` starts. Network availability does not make unpinned source bytes
  acceptable.
- A **build-user policy** is the per-package `build.user` choice controlling the identity that executes `rpmbuild` and `%check`. Its compatible default is `root`; `unprivileged` opts into the fixed `rpmbuild` identity with UID/GID `10001:10001`. It does not change the root-only dependency-install stage or grant privileges to installed smoke tests.
- A **repair lease** is an expiring, owner-bound claim on one failed PR head SHA. It prevents two local Codex processes from overwriting each other.
- A **golden package** is a fixed end-to-end fixture with a pinned source/content digest, expected state, allowed changes, and assertions.
- A **repository generation** is an immutable binary/source RPM snapshot with a state-bound `repomd.xml` SHA-256. A build resolves the mutable `state.json` pointer once, then uses only that generation URL.

## Safety and trust boundary

- Arch stable `core`/`extra` and AUR are primary discovery indexes. AUR data is untrusted metadata: no workflow executes a `PKGBUILD`.
- Pure AUR `-bin` entries and entries older than 730 days are excluded by default. VCS/nightly variants are discovery clues only.
- Supplementary discovery resolves the current stable openSUSE Tumbleweed snapshot, latest Fedora GA, Debian `stable`, and latest Ubuntu GA release in standard support. Rawhide, testing/unstable, staging, multilib, development, and prerelease feeds are excluded.
- An importable source requires an HTTPS official stable release/tag URL and its full SHA-256; distribution package checksums do not substitute for upstream source checksums. Target build containers may retrieve the pinned source over HTTPS and verify that digest again before `rpmbuild` starts.
- Required native-kernel or hardware validation becomes `needs-native-riscv`. The self-hosted fleet accelerates protected-main QEMU user-mode builds on x86_64 only; it is never treated as native RISC-V validation, and pull-request/merge-queue jobs remain on disposable GitHub-hosted runners.
- Repair runs only on a maintainer's local Codex through local `gh` authentication or an explicitly authorized process-scoped `GH_TOKEN`. Using that token for local `gh`/Git operations is permitted; persisting or publishing its value in repository content, commits, PR text, logs, artifacts, Actions configuration, or Pages is forbidden. `scripts/github-credential-guard` checks the active token against repository, staged, and publication content without printing it. CI only uploads structured failure evidence and labels a trusted internal PR `repair-queued`.
- The only custom Actions secret is `RPM_REPO_SSH_PRIVATE_KEY`. It is a forced-command, write-only `rrsync` deployment identity for `/opt/openeuler-riscv-rpm-repo/incoming`; it cannot run a shell, delete or overwrite remote files, and is never available to build commands. It is not an OpenAI/Codex credential.
- Successful package output is published only after the exact package build and installed-RPM smoke pass on a protected `main` push (or an explicit trusted backfill call). Pull-request builds never publish RPMs.
- The supplemental project repository is served from the operator-provided HTTP endpoint `http://2.27.148.101:38080`. Its unsigned project RPMs use `gpgcheck=0`; CI compensates with a pinned SSH host key for publication, per-file upload SHA-256, immutable generations, no HTTP redirects, and a state-bound `repomd.xml` digest. The official openEuler HTTPS/GPG-checked repository remains enabled and authoritative.
- Automation never writes to upstream projects. RISC-V patches remain in `packages/<id>/patches/` and are referenced by the SPEC.

## Current catalog evidence

A **raw catalog record** is one package entry parsed from a distribution index; it is discovery input, not an importable source or a PR promise. A **reviewed cohort** is the smaller set whose official stable upstream archive, exact SHA-256, license evidence, archive safety, and distribution lineage have all been checked.

Snapshot `discovery-20260808T165000Z-9a89920c269462cd` records 251,506 raw records: Arch stable `core`/`extra` 15,163, AUR 117,191, openSUSE Tumbleweed 17,113, Fedora 44 GA 23,660, Debian 13.6 `stable` 38,068, and Ubuntu 26.04 LTS GA 40,311. It stores every official metadata URL and object digest plus the normalized-input digest. Two identical fixed-time runs produced gzip SHA-256 `bd79d0cd34f3d674c10736aa83d8f9f78f35531ae99cef53663b62bc74458fe0`.

Strict discovery emits zero directly importable candidates because distribution indexes do not prove the bytes of an official upstream release archive. It retains 181,134 deduplicated rejection/hold decisions: 89,975 unverified upstreams, 46,870 stale entries, 17,752 license blocks, 12,949 VCS-only variants, 12,765 binary-only variants, and 823 prereleases. These are an auditable backlog, not silently discarded packages.

The reviewed overlay currently promotes 100 verified components. Eighty-eight have Arch stable lineage, 68 have AUR metadata lineage, 98 have cross-distribution corroboration, and 44 retain rows from all six configured sources: Arch stable, AUR, Debian, Fedora, openSUSE, and Ubuntu. `bftpd` and `libcap-ng` are explicitly retained with single-distribution raw lineage plus separately verified official upstream bytes. The newest ten promotions use exact frozen-row selectors where the snapshot split a package across component keys; GNU Which additionally marks Debian and Ubuntu `debianutils` rows as functional providers rather than GNU Which source/version evidence. All declared source URLs remain subject to the independent downloader/checksum verifier. No AUR recipe was trusted or executed.

## Repository map

| Path | Purpose |
|---|---|
| `skills/` | Six composable Codex Skills and their contracts |
| `scripts/` | Deterministic discovery, onboarding, build, update, repair, and dashboard tools |
| `schemas/` | Versioned machine contracts for packages, sources, builds, updates, repair leases, and dashboards |
| `ci/` | Exact openEuler repository config, rootfs-to-OCI build, QEMU/RVA23 checks, and image digest lock |
| `packages/` | One directory per managed package plus `_template` |
| `tests/golden/` | Fixed success, repair, and native-only acceptance fixtures |
| `catalog/` | Discovery source policy, immutable run snapshots, and reviewed official-release evidence |
| `dashboard/` | Static Pages application and generated evidence |
| `ops/rpm-repo-server/` | Idempotent Nginx, restricted rsync, systemd, and atomic `createrepo_c` deployment |

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

The full build is intentionally run by `package-ci.yml` inside the locked RISC-V OCI after a separate audited BuildRequires stage. The target build container has network access so it can retrieve declared sources, and `scripts/build-rpm` verifies every pinned SHA-256 before invoking `rpmbuild`.

Resolve and verify the exact supplemental repository generation that would be
mounted into dependency installation and installed-RPM smoke:

```sh
ci/rpm-repo-client.py resolve \
  --state-url http://2.27.148.101:38080/state.json \
  --repo-file work/openeuler-riscv-project.repo \
  --output work/rpm-repository-resolution.json
```

`RPM Repository Backfill` builds every active non-golden package whose policy
does not require native RISC-V hardware. It runs up to 20 independent package
builds in parallel, publishes both RPM and SRPM products, and records native,
retired, and golden exclusions in its seven-day plan artifact.

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
  --output catalog/snapshots/local.json.gz
```

For a live run, call `scripts/snapshot-catalog` first. It resolves each configured stable distribution, verifies and records the metadata URLs/digests, and writes frozen per-source JSON consumed by `scripts/discover-packages`. The `Catalog Discovery` workflow performs both stages.

Complete discovery snapshots use deterministic `*.json.gz` storage (gzip mtime `0`) so the full six-distribution decision set remains below GitHub's single-file limit. Repository tools accept both uncompressed `*.json` and compressed `*.json.gz` snapshots.

When safe distribution metadata identifies a component but cannot prove its official release bytes, layer the reviewed registry over the immutable snapshot without modifying that snapshot:

```sh
scripts/resolve-upstream \
  --input catalog/snapshots/discovery-20260808T165000Z-9a89920c269462cd.json.gz \
  --reviewed-evidence catalog/upstream-releases.yaml \
  --output work/upstream-resolution.json \
  --evidence-output work/upstream-resolution-evidence.json
```

`catalog/upstream-releases.yaml` is validated against `schemas/upstream-release-evidence.schema.json`. The resolver rejects unknown components, version regressions, prereleases, non-HTTPS endpoints, incomplete SHA-256 values, and archives whose recorded member/link inspection is unsafe.

Onboard and update commands are deliberately one-package/one-PR operations. Use `--dry-run` before remote writes.

## CI image invariant

The build image tag is `ghcr.io/yinjiayi/openeuler-riscv64-rpmbuild:24.03-lts-sp3-rva23`. Its root filesystem must be constructed only from:

```text
https://repo.openeuler.org/openEuler-24.03-LTS-SP3/everything/riscv64/rva23/riscv64/
```

Package CI reads an immutable digest from `ci/image.lock`; a mutable tag is never accepted as build evidence. Image publication records the `repomd.xml` digest, installed RPM manifest, OCI digest, QEMU version, and RVA23 probe result.

Audited BuildRequires are installed as root in a per-run, unpublished derived image. Package metadata then selects the `rpmbuild` identity: existing and root-capability suites default to `root`, while packages whose upstream checks require ordinary filesystem permission semantics may explicitly select `unprivileged`. The latter path performs a symlink-refusing ownership handoff for the fresh generated work tree, verifies the exact UID/GID before execution, and preserves regular JSON/log/RPM evidence for the host-side artifact stager. A root-dependent suite must use the compatible root policy or an evidence-backed native route; CI never silently skips it.

## Auto-merge policy

Repository rules require the latest head SHA to pass `metadata-validate`, `source-verify`, `rpmbuild-riscv64`, `rpm-install-smoke`, `patch-policy`, and `merge-policy`. Required approvals are zero. Blocking labels, source/license/checksum failures, `needs-human`, and `needs-native-riscv` prevent merge even if unrelated checks passed.

## License scope

Original repository code, Skills, workflows, schemas, and documentation are licensed under Apache-2.0; source files use `SPDX-License-Identifier: Apache-2.0` where their syntax permits. This does not relicense upstream sources or imported patches. Each third-party or derived patch must record its source, original license, root cause, applicable versions, upstream status, and removal condition in package metadata and its patch header.

## Current limits

QEMU user mode is not native hardware validation. Kernel modules, eBPF, boot/systemd, privileged syscall behavior, devices, timing-sensitive concurrency, and performance claims remain native-only. Artifacts are retained for 7 days; this MVP intentionally sets no custom per-artifact or aggregate storage budget beyond GitHub account limits.
