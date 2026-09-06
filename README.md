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
- A **per-run dependency network** is a uniquely named, session-labelled Docker
  bridge used by exactly one BuildRequires container. CI first checks the live
  RPM baseline in a separate one-shot container whose network mode stays
  `none`; only a passed baseline and non-empty dependency plan permit creation
  of the externally routed bridge for the audited DNF transaction. Its endpoint
  is inspected from the network and container sides, then detached and removed
  by full object ID. It is not a shared runner network and does not weaken
  source checksum verification.
- A **bounded DNF transaction** is a dependency or installed-RPM transaction
  whose target-container process group has a finite deadline for every attempt
  and a smaller explicit budget than its surrounding CI step. The shared runner
  terminates the container-local DNF process group on timeout, retains the same
  per-container cache only for a finite retry, and atomically records each
  attempt's elapsed time, timeout state, and exit code. The root-owned target
  container publishes that non-secret JSON as mode `0644` so the hosted runner
  can validate and upload it after the transaction. It does not disable a
  repository, accept unresolved dependencies, share cache across runs, or turn
  a failed transaction into success.
- A **build-user policy** is the per-package `build.user` choice controlling the identity that executes `rpmbuild` and `%check`. Its compatible default is `root`; `unprivileged` opts into the fixed `rpmbuild` identity with UID/GID `10001:10001`. It does not change the root-only dependency-install stage or grant privileges to installed smoke tests.
- A **repair lease** is an expiring, owner-bound claim on one failed PR head SHA. It prevents two local Codex processes from overwriting each other.
- The **evaluation-only merge policy** is the existing `configure` job context emitted by the Auto Merge Policy workflow. It disarms any stale GitHub Auto-merge request, binds the live pull request to the event's exact head and current protected base, evaluates package eligibility, and proves Auto-merge remains disabled. It never arms or merges a pull request; an explicit maintainer squash merge is a separate operation. Reusing this established context preserves exact-head coverage for already-open pull requests; any audited coverage gap must be backfilled and verified before the ruleset is applied.
- A **required-context migration audit** is a read-only preflight that proves every currently open pull request's exact head already has a named GitHub Actions check from the expected workflow and app. It verifies availability and provenance, not a successful conclusion, and it fails rather than treating a legacy commit status, incomplete context page, or changing PR snapshot as coverage.
- A **default-branch freshness proof** compares the pull-request event's base commit with the repository's current default-branch ref. Before checkout, an inline API gate that needs no repository files performs this comparison. A PR based on an older `main` commit remains disarmed, because checking out that older base would also execute an older policy; refreshing the branch is required before its eligibility can be evaluated against the current policy.
- A **protected-main package overlay** is the trusted-dispatch workspace formed
  by checking out CI tooling from the protected `main` workflow commit and
  replacing exactly one `packages/<id>` tree with that tree from the authorized
  PR head. Its evidence binds the tooling commit, package commit, and package
  tree SHA; it does not merge shared tooling into the package PR or authorize
  any file outside that package tree. Git `HEAD` remains the protected tooling
  commit. Scope selection accepts the separate package commit only after it
  validates the overlay evidence and independently matches the committed,
  staged, and working-copy package trees.
- A **golden package** is a fixed end-to-end fixture with a pinned source/content digest, expected state, allowed changes, and assertions.
- A **repository generation** is an immutable binary/source RPM snapshot with a state-bound `repomd.xml` SHA-256. A build resolves the mutable `state.json` pointer once, then uses only that generation URL.
- A **backfill shard** is one of two deterministic, round-robin partitions of the active QEMU-buildable package list. Each shard stays below GitHub Actions' 256-entry matrix limit; the configured fleet-wide concurrency is divided equally between them, so the two matrices support up to 512 packages without doubling runner usage.
- An **official-repository-only fallback** is an evidence-recorded dependency mode used only when the fixed supplemental repository cannot be contacted. It disables that project repository and retains the HTTPS/GPG-checked official openEuler repository; it does not waive missing dependencies or convert a failed DNF transaction into success.
- A **package inventory** is the generated, machine-readable union of managed package directories, reviewed upstream releases, inferred package PRs, and deduplicated discovery names. It is a status index, not an authorization to build every discovered name.
- A **discovery key** is the stable `package_base`, `name`, or `component_id` fallback used to deduplicate raw catalog records. The immutable discovery snapshot remains the authoritative source for every raw record and lineage row.

## Safety and trust boundary

- Arch stable `core`/`extra` and AUR are primary discovery indexes. AUR data is untrusted metadata: no workflow executes a `PKGBUILD`.
- Pure AUR `-bin` entries and entries older than 730 days are excluded by default. VCS/nightly variants are discovery clues only.
- Supplementary discovery resolves the current stable openSUSE Tumbleweed snapshot, latest Fedora GA, Debian `stable`, and latest Ubuntu GA release in standard support. Rawhide, testing/unstable, staging, multilib, development, and prerelease feeds are excluded.
- An importable source requires an HTTPS official stable release/tag URL and its full SHA-256; distribution package checksums do not substitute for upstream source checksums. Target build containers may retrieve the pinned source over HTTPS and verify that digest again before `rpmbuild` starts.
- Required native-kernel or hardware validation becomes `needs-native-riscv`. The self-hosted fleet accelerates protected-main QEMU user-mode builds on x86_64 only; it is never treated as native RISC-V validation, and pull-request/merge-queue jobs remain on disposable GitHub-hosted runners.
- Repair runs only on a maintainer's local Codex through local `gh` authentication or an explicitly authorized process-scoped `GH_TOKEN`. Using that token for local `gh`/Git operations is permitted; persisting or publishing its value in repository content, commits, PR text/comments, logs, artifacts, Actions configuration, or Pages is forbidden. `scripts/github-credential-guard` checks the active token against repository, staged, and publication content without printing it. CI only uploads structured failure evidence and labels a trusted internal PR `repair-queued`; a claimed lease changes that state to `codex-repairing`. These labels mean the exact head is awaiting or undergoing a maintainer repair, and both make the evaluation-only policy ineligible until a maintainer verifies the replacement head and explicitly releases the repair state.
- The only custom Actions secret is `RPM_REPO_SSH_PRIVATE_KEY`. It is a forced-command, write-only `rrsync` deployment identity for `/opt/openeuler-riscv-rpm-repo/incoming`; it cannot run a shell, delete or overwrite remote files, and is never available to build commands. It is not an OpenAI/Codex credential.
- Successful package output is published only after the exact package build and installed-RPM smoke pass on a protected `main` push (or an explicit trusted backfill call). Pull-request builds never publish RPMs.
- The supplemental project repository is served from the operator-provided HTTP endpoint `http://2.27.148.101:38080`. Its unsigned project RPMs use `gpgcheck=0`; CI compensates with a pinned SSH host key for publication, per-file upload SHA-256, immutable generations, no HTTP redirects, and a state-bound `repomd.xml` digest. The official openEuler HTTPS/GPG-checked repository remains enabled and authoritative.
- Automation never writes to upstream projects. RISC-V patches remain in `packages/<id>/patches/` and are referenced by the SPEC.

## Current catalog evidence

A **raw catalog record** is one package entry parsed from a distribution index; it is discovery input, not an importable source or a PR promise. A **reviewed cohort** is the smaller set whose official stable upstream archive, exact SHA-256, license evidence, archive safety, and distribution lineage have all been checked.

Snapshot `discovery-20260808T165000Z-9a89920c269462cd` records 251,506 raw records: Arch stable `core`/`extra` 15,163, AUR 117,191, openSUSE Tumbleweed 17,113, Fedora 44 GA 23,660, Debian 13.6 `stable` 38,068, and Ubuntu 26.04 LTS GA 40,311. It stores every official metadata URL and object digest plus the normalized-input digest. Two identical fixed-time runs produced gzip SHA-256 `bd79d0cd34f3d674c10736aa83d8f9f78f35531ae99cef53663b62bc74458fe0`.

Strict discovery emits zero directly importable candidates because distribution indexes do not prove the bytes of an official upstream release archive. It retains 181,134 deduplicated rejection/hold decisions: 89,975 unverified upstreams, 46,870 stale entries, 17,752 license blocks, 12,949 VCS-only variants, 12,765 binary-only variants, and 823 prereleases. These are an auditable backlog, not silently discarded packages.

The reviewed overlay currently promotes 119 verified components. One hundred four have Arch stable lineage, 74 have AUR metadata lineage, 117 have cross-distribution corroboration, and 46 retain rows from all six configured sources: Arch stable, AUR, Debian, Fedora, openSUSE, and Ubuntu. `bftpd` and `libcap-ng` are explicitly retained with single-distribution raw lineage plus separately verified official upstream bytes. The newest promotions use exact frozen-row selectors where the snapshot split a package across component keys; GNU Which additionally marks Debian and Ubuntu `debianutils` rows as functional providers rather than GNU Which source/version evidence. All declared source URLs remain subject to the independent downloader/checksum verifier. No AUR recipe was trusted or executed.

The full package inventory is committed as `catalog/package-index.json.gz`, with a compact readback at `catalog/package-index-summary.json`. The current compressed index contains 151,852 entries: one entry for each of the 151,835 deduplicated discovery keys plus managed-package, reviewed-release, and pull-request records that are not already represented by a discovery key. It records 279 managed packages, 119 reviewed releases, and 439 observed pull requests (82 open and 357 merged at generation time). Its `source_snapshot` field points to the immutable 251,506-record snapshot above, so the index does not replace or silently rewrite raw catalog evidence. The inventory is a status index and onboarding queue input, not authorization to build every discovered name. Regenerate it only from a fresh `gh pr list --state all` JSON input and an explicit protected-main SHA; validate it with `scripts/validate-package-index`.

The GitHub Pages Dashboard presents that full inventory as its primary view and emits the browser-ready list as `inventory.json`. It overlays the committed inventory with managed package metadata from the checked-out `main`, current pull-request facts, and retained CI evidence. An **inventory status** is the strongest currently supported lifecycle fact for one inventory key: discovery/review/PR/managed metadata first, then an exact-head build result, and finally verified publication. `build-succeeded` means a schema-valid successful CI result matches a recorded package or PR commit; it does not mean the RPM repository contains the products. `published` means an RPM upload batch and public-generation verification match the same package, commit, and immutable generation. Only `published` rows receive direct `.../Packages/*.rpm` SRPM and RPM links. A CI run link is labeled as CI evidence and is never presented as a repository package address. Because Actions evidence is retained for seven days, missing historical evidence remains an explicit weaker status rather than a reconstructed or guessed link.

The full table searches package names, aliases, component IDs, and decision labels; status and evidence filters operate over the complete list. Rendering is paginated so the browser creates at most 250 table rows at once even though the JSON contains every inventory entry. `schemas/dashboard.schema.json` covers the summary/managed payload and `schemas/dashboard-inventory.schema.json` covers the full browser list.

## Repository map

| Path | Purpose |
|---|---|
| `skills/` | Six composable Codex Skills and their contracts |
| `scripts/` | Deterministic discovery, onboarding, build, update, repair, and dashboard tools |
| `schemas/` | Versioned machine contracts for packages, sources, builds, updates, repair leases, and dashboards |
| `ci/` | Exact openEuler repository config, rootfs-to-OCI build, QEMU/RVA23 checks, and image digest lock |
| `packages/` | One directory per managed package plus `_template` |
| `tests/golden/` | Fixed success, repair, and native-only acceptance fixtures |
| `catalog/` | Discovery source policy, immutable run snapshots, reviewed official-release evidence, and the full package inventory |
| `dashboard/` | Static Pages application and generated evidence |
| `ops/rpm-repo-server/` | Idempotent Nginx, restricted rsync, systemd, and atomic `createrepo_c` deployment |

## Local verification

Python 3.9 or newer is sufficient for repository metadata tests. Docker/QEMU is required only for the target-architecture build gate.

```sh
make validate
make test
make golden
make dashboard
# Read back the generated full inventory and its immutable snapshot link.
scripts/validate-package-index
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
  --output work/rpm-repository-resolution.json \
  --allow-unavailable
```

With `--allow-unavailable`, connection, timeout, and transient HTTP service
failures produce an explicit `unavailable` resolution and a disabled
supplemental repository file. Redirects, non-transient HTTP responses, JSON,
URL, generation, and checksum integrity failures still fail closed.

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

Package CI reads an immutable digest from `ci/image.lock`; a mutable tag is never accepted as build evidence. Image publication records the `repomd.xml` digest, installed RPM manifest, OCI digest, QEMU version, and RVA23 probe result. Large bootstrap metadata and signing-key RPM downloads use a **resumable authenticated download**: finite HTTPS Range attempts retain only the current partial file, and the completed bytes are not exposed at their final path until their SHA-256 matches the checksum authenticated by the fetched `repomd.xml`. Resume does not weaken GPG checking or accept partial data. The installed RPM manifest is a sorted, checksum-bound record of each package's identity, architecture, and RPM-defined SHA-1/SHA-256 immutable-header digests. Every row and digest is format-validated before use. These digests bind original package metadata across database implementations; they do not replace the gpgchecked DNF transaction or claim a second payload verification.

Audited BuildRequires are installed as root in a per-run, unpublished derived image. A separate networkless container first proves the immutable base image's live RPM baseline. A valid baseline and non-empty dependency plan permit creation of the per-run egress bridge; the long-lived dependency container is created directly on that bridge, and DNF starts only after exact exclusive attachment is verified. The bridge is detached and removed before the image is committed. An empty dependency plan creates the long-lived container with network mode `none` and never creates an egress network. Package metadata then selects the `rpmbuild` identity: existing and root-capability suites default to `root`, while packages whose upstream checks require ordinary filesystem permission semantics may explicitly select `unprivileged`. The latter path performs a symlink-refusing ownership handoff for the fresh generated work tree, verifies the exact UID/GID before execution, and preserves regular JSON/log/RPM evidence for the host-side artifact stager. A root-dependent suite must use the compatible root policy or an evidence-backed native route; CI never silently skips it.

## Auto-merge policy

Repository rules require the latest head SHA to pass `metadata-validate`, `source-verify`, `rpmbuild-riscv64`, `rpm-install-smoke`, `patch-policy`, `merge-policy`, and the established Auto Merge Policy `configure` evaluation context. Each required check is pinned to GitHub Actions App integration ID `15368`, so a same-named legacy status or another app cannot satisfy it. Strict status checks also require the pull request to remain up to date with `main` at GitHub's final merge decision. Required approvals are zero, but repository configuration sets `allow_auto_merge=false`: a maintainer must explicitly review the exact head and issue the squash merge. The workflow reports draft state, blocking labels, source/license/checksum failures, `needs-human`, `needs-native-riscv`, and out-of-scope changes as ineligible evidence; it does not convert eligibility into a merge operation.

Before `ci/configure-github.sh --apply` performs any repository write, it runs the required-context migration audit for the legacy `configure` context from the `Auto Merge Policy` workflow and `github-actions` app. The audit paginates every open pull request, binds each result to its exact head commit, then repeats the complete PR/head scan and requires an unchanged snapshot. Missing contexts, legacy `StatusContext` records, unexpected workflow/app provenance, head mismatches, API failures, and commit heads with more than 100 combined contexts all stop configuration and remain recorded in the requested JSON output. Repeated trusted CheckRuns are retained as evidence but are not a provenance failure. `--dry-run` reads only the committed configuration files and never invokes the audit or contacts GitHub.

The apply path repeats the complete audit immediately before changing the ruleset, after slower repository-setting, label, variable, and Pages reconciliation. Its administrator response must explicitly expose a list-valued `bypass_actors` field and the configured value must be empty; a missing field is never normalized into an empty list. A ruleset update snapshots the previous exact accepted policy, including every required check's integration ID, and restores plus verifies it after an update or readback failure. A newly created ruleset is considered removed only after a successful paginated listing proves its exact numeric ID absent; API failure is never treated as deletion evidence.

Run the same read-only gate directly with an authenticated local `gh` session:

```sh
ci/audit-required-context.py \
  --repository yinjiayi/openeuler-riscv-packages \
  --context configure \
  --expected-workflow "Auto Merge Policy" \
  --expected-app github-actions \
  --output work/github-required-context-audit.json
```

Automatic merge is never armed by repository automation. This includes the Auto Merge Policy, daily package updater, catalog-snapshot PR creator, and CI-image digest-lock PR creator. Each creator may open a PR and bridge its required checks, but it reports that an explicit maintainer squash merge is required. Every listed pull-request event, including a retarget away from `main`, first attempts to disarm any stale Auto-merge request and accepts that operation only after API readback proves the exact open PR is unmerged and `auto_merge` is null. A non-default-branch or stale-base target ends as a successful disarmed no-op before checkout. Only a pull request whose event base equals the current default-branch head can check out that base as immutable policy. The workflow then evaluates the complete API file list and performs a final exact-head disabled-state proof. A current same-repository change confined to one `packages/<package-id>/` directory can be reported eligible; infrastructure, workflow, CI, script, schema, catalog, Dashboard, documentation, mixed-package, incomplete-file-list, and renamed-from-shared-path changes remain ineligible. Neither result invokes `gh pr merge --auto` or any merge command.

This boundary is required because GitHub suppresses new workflow runs for events created with the repository `GITHUB_TOKEN`. If `github-actions[bot]` arms Auto-merge, the resulting protected-main push can therefore have no Package CI run and no RPM/SRPM publication. Keeping GitHub Auto-merge disabled ensures that a separately authorized maintainer merge, rather than the workflow token, is the event source for the protected-main build and publication gate.

A **bot-PR required-check bridge** is the fail-closed protected-main dispatch used only when `github-actions[bot]` creates a PR and GitHub suppresses that PR's ordinary workflow event. The bridge binds the open PR's exact head, current base, same-repository branch, bot identity, complete one-file change, and a unique parent-run nonce. Its infrastructure allowlist contains only `infra/ci-image-<12 hex>` changing an existing `ci/image.lock`, or `catalog/discovery-<timestamp>-<run id>` adding the identically named immutable snapshot. Package CI itself is dispatched from `main`, never from the bot branch; the run title binds the PR number, candidate head, and nonce while the workflow head must equal the supplied protected-base SHA. Infrastructure mode exercises no package build or RPM publication, and each PR number has an independent concurrency key. Only after the exact Package CI run and all six package-policy jobs have a terminal `success`, and the live PR remains open, unmerged, exact-head/base bound, and Auto-merge-disabled, does this bridge publish the six package-policy contexts. Any orchestration or status-write failure overwrites all six with `error`. The separate protected-main `configure` check bridge creates a GitHub CheckRun rather than a commit status, only for an exact bot-created digest-lock PR whose suppressed Auto Merge Policy run, immutable image-lock contents, and current PR lease are fully attested; ordinary PRs continue to obtain `configure` directly from Auto Merge Policy. Catalog snapshot PRs remain fail-closed at `configure` until an equivalent catalog-content attestation is implemented.

## License scope

Original repository code, Skills, workflows, schemas, and documentation are licensed under Apache-2.0; source files use `SPDX-License-Identifier: Apache-2.0` where their syntax permits. This does not relicense upstream sources or imported patches. Each third-party or derived patch must record its source, original license, root cause, applicable versions, upstream status, and removal condition in package metadata and its patch header.

## Current limits

QEMU user mode is not native hardware validation. Kernel modules, eBPF, boot/systemd, privileged syscall behavior, devices, timing-sensitive concurrency, and performance claims remain native-only. Artifacts are retained for 7 days; this MVP intentionally sets no custom per-artifact or aggregate storage budget beyond GitHub account limits.
