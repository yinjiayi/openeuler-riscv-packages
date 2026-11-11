# GitHub Actions Runner fleet

This directory defines one persistent, isolated x86_64/QEMU Runner per audited
Ubuntu 26.04 host in `10.230.50.201-10.230.50.250`. Each Runner is named
`oe-rva23-qemu-<last-octet>` and installed below `/opt/openeuler-actions-runner`.
It accelerates the existing openEuler 24.03 LTS SP3 `riscv64`/RVA23 QEMU build;
it is not native RISC-V evidence and must never clear `needs-native-riscv`.

## Security boundary

A Runner with Docker socket access is effectively root-capable. Systemd
sandboxing reduces accidental host access but cannot make arbitrary workflow
code safe. GitHub explicitly warns that external contributors to public
repositories can compromise persistent self-hosted runners. This fleet is
therefore fail-closed:

- only `yinjiayi/openeuler-riscv-packages` protected `main` is allowed;
- only `.github/workflows/package-ci.yml@refs/heads/main` and
  `.github/workflows/rpm-repo-backfill.yml@refs/heads/main` are allowed;
- only `push` and `workflow_dispatch` are allowed;
- pull-request and `pull_request_target` events fail in the synchronous pre-job
  hook even if someone targets the labels directly; `merge_group` and
  `workflow_run` are also explicitly rejected;
- GitHub's default labels `self-hosted`, `linux`, and `x64` are retained, and
  custom `oe-rva23-qemu` routing is added;
- registration and activation are separate. A registered Runner remains
  stopped until the root-owned `policy.conf` is explicitly changed to
  `OE_RUNNER_ENROLLMENT_ENABLED=true` and `activate.sh` passes every check.

The service keeps `NoNewPrivileges=true` and empty capability sets, but
explicitly leaves `RestrictSUIDSGID` disabled. Ubuntu 26.04 implements that
directive under systemd 259 by denying GNU tar's safe `openat2` directory
resolution with `ENOSYS`, which prevents the Runner from extracting even a
pinned `actions/checkout` archive.
The systemd `ExecStartPre` now creates and extracts a local archive containing
an installed executable and verifies its bytes and executable bit. This
**action-extraction compatibility probe** means the service must prove the
same host tar operation needed during GitHub's pre-step setup before it can
come online; it does not relax the protected-main workflow/event gate.

## Trusted package dispatch

A **trusted package dispatch** is a maintainer-local `workflow_dispatch` of
the `main` version of `Package CI` that checks out one exact package PR head.
It is not a pull-request event and it is not an approval for arbitrary branch
code. `scripts/dispatch-trusted-package-ci` first requires local GitHub
authentication, verifies that the PR is open, same-repository, owner/member
authored, prefix-limited, based on `main`, and confined to one
`packages/<package-id>/` directory. It supplies the PR number, head, and base
to the pinned `main` workflow with publication disabled. Before any job checks
out that head, a GitHub-hosted authorization job checks out `github.sha` from
protected `main` and repeats the live PR, base/head, author, branch, and file
scope checks through the GitHub API. A direct workflow dispatch therefore
cannot bypass the local bridge by supplying an arbitrary SHA or enabling
publication. Required contexts are posted only after the final
`build-result.json` matches the requested package and commit. This lets a
trusted maintainer use the fleet for package PRs without allowing public PR
workflows onto persistent Docker-capable hosts. The separately protected
`rpm-repo-backfill.yml` reusable caller remains allowed by its exact `main`
workflow reference, so it can rebuild and publish already-merged packages.

Run it only from a reviewed checkout after `scripts/github-credential-guard`
has passed:

```bash
scripts/dispatch-trusted-package-ci \
  --pr 123 --package-id example \
  --output /private/tmp/example-pr123-dispatch.json
```

`--output` is a file contract, not a directory. The dispatcher atomically
writes one JSON evidence object after argument/output validation for a
successful run, a completed workflow failure, or a later local/API error. The
record binds the PR head and base, protected-main run ID/name/URL, last API
observation, polling bounds, required-job conclusions, status-update outcome,
and any tool error. Exit 0 means the required jobs and bound build result
passed; exit 1 means GitHub reached a verified terminal workflow failure; exit
2 means the bridge failed closed. A failed workflow therefore remains
`outcome=workflow-failed` with its real run/job conclusions instead of being
reported as a polling error. No output can be written when `--output` itself
names a directory or has a non-directory parent.

The dispatcher does not trust an early return from `gh run watch`. It polls
the exact Actions run through the API until `status=completed`, requires the
same run ID and display title, `workflow_dispatch` event, protected `main`
branch, a terminal conclusion, and a consistent completed job view. The
default run deadline is three hours; each polling request is capped at 30
seconds, and up to five consecutive transient API/view errors are tolerated.
Maintainers may tighten the deadline with `--run-timeout-seconds` and the
consecutive-error bound with `--max-transient-errors`; identity drift always
fails immediately rather than being retried.

On 2026-08-24 the repository's fork-workflow approval policy was set to GitHub's
least restrictive public-repository option,
`first_time_contributors_new_to_github`, and read back successfully. Established
contributors and the repository's approved automation can therefore run PR
workflows without repeated maintainer approval. GitHub still requires approval
for contributors whose accounts are new to GitHub; the public-repository API
does not offer a fully disabled approval policy. This setting does not replace
the Runner's protected-main event/workflow gate, and fork PR workflows remain
read-only and isolated from repository secrets.

## Fixed software

`runner-release.lock` pins official `actions/runner` v2.338.2 Linux x64:

- URL: `https://github.com/actions/runner/releases/download/v2.338.2/actions-runner-linux-x64-2.338.2.tar.gz`
- SHA-256: `baebf204307bac6193480852732f0aba2ae97b6c5597c244f4d5558390147c40`
- Official release asset size: `228071396` bytes
- Official release ID: `424372770`; Linux x64 asset ID: `678460500`

The version, digest, and size were freshly checked through GitHub's official
Releases API on 2026-11-06. The downloaded Linux x64 asset's size and SHA-256
were independently reproduced during canary source staging; staging is not a
successful deployment. Installation verifies the actual archive's size and
SHA-256 against the lock before extraction. Automatic Runner
updates are disabled; GitHub requires a manually pinned Runner to be updated
within 30 days of any new release.

The lock loader still approves one exact version/digest/size tuple; deriving
the archive name and official URL from that approved version does not permit
arbitrary releases. Registration, service preflight and audit all load the
same installed lock before comparing the observed Runner version. Keep the
lock, shared approval tuple, tests and this section in the same reviewed change.

Ubuntu 26.04 supplies static QEMU user binaries through `qemu-user` and binfmt
registration through `qemu-user-binfmt`; `qemu-user-static` is only a virtual
compatibility name. The installer also installs Ubuntu's `docker.io` package.
It explicitly installs the minimal `iptables` frontend while retaining
`--no-install-recommends`. Docker 29's iptables firewall backend directly
executes `/usr/sbin/iptables` when it creates bridge endpoints, including when
the package selects the nft-compatible implementation through alternatives.
Both installation and service preflight require that exact executable path, so
a host with incomplete package state remains offline instead of accepting a
job that cannot start a networked container. The installer also asks Debian
alternatives to restore the distribution-selected `iptables` master link; this
is required for an already-installed package whose `/usr/sbin/iptables` link
was lost, because a no-op `apt-get install` does not recreate it reliably.

### Host systemd package integrity

The **systemd package integrity gate** is the shared lifecycle check that binds
`/usr/bin/systemctl` to Ubuntu's installed `systemd` package before any
`systemctl` operation. It requires a root-owned, mode-0755, non-symlink regular
executable; the exact dpkg owner; an installed `systemd` package with a valid
version; and no output from `dpkg --verify systemd`. Dpkg can return zero
while printing a file checksum mismatch, so empty verification output—not the
return code alone—is the acceptance condition. The installer repeats this
gate after apt completes, and preflight, audit, registration, activation, and
uninstall inherit it from the shared platform check. Systemctl itself is then
called by absolute path with paging disabled.

A **compromised host** is one where package ownership or integrity no longer
matches that gate, even if a renamed executable can still submit a systemd job
or the requested unit later appears active. Lifecycle scripts stop without
executing the untrusted tool. They never move a renamed binary back, reinstall
a package, delete an indicator, or otherwise attempt in-place recovery.
Quarantine the host from Runner scheduling and the network, preserve forensic
evidence, rotate its SSH and Runner credentials, and reimage it from a trusted
source. Only a clean package-integrity audit plus the ordinary canary gates may
return a rebuilt host to the fleet.

## Credentials

Scripts reject `--token`, `--pat`, JIT configuration, and token-like command
arguments. `register.sh` reads a short-lived repository Runner registration
token from one stdin line, or from process-only
`OE_RUNNER_REGISTRATION_TOKEN`. `uninstall.sh` likewise uses stdin or
`OE_RUNNER_REMOVAL_TOKEN`. Long-lived GitHub-token prefixes are rejected.

`credential_exec.py` passes the short-lived value to the official Runner only
through `ACTIONS_RUNNER_INPUT_TOKEN`, disables core dumps, drops to the
non-root `oegha` account before execution, and scans Runner identity/diagnostic
files for accidental persistence before erasing its mutable in-process copy.
No token is written into the repository, `/etc`, systemd, command line, or
operator log. Normal Runner registration necessarily creates its own local
machine credentials under the Runner directory; these are root-owned and
mode-restricted after configuration.

## Rollout

The audited guests expose 32 vCPUs, not 64, approximately 60.8 GiB RAM, and
about 951 GiB free under `/opt`. Phase 1 is exactly one Runner per host:

1. Canary: `.201-.205` (five Runners).
2. Clean expansion: the other 41 `systemd=running` hosts, reaching 46.
3. Conditional: `.211`, `.220`, `.224`, `.231`, which had only
   `fwupd-refresh.service` failed. These require an independent decision and
   `--allow-degraded`; they are never silently mixed into clean rollout.

`install.sh` persists `ALLOW_DEGRADED=true` in the root-owned `identity.conf`
only when both the explicit flag and one of those four addresses match.
Registration, activation, audit, and uninstall require their flag to match
that immutable installed identity, while systemd preflight reads the persisted
value. An idempotent reinstall cannot silently change it; changing this policy
requires explicit uninstall and reinstall.

Do not parallelize installation across all 50 hosts without a successful
canary and recorded load, memory, disk, QEMU throughput, Docker growth, and
network error evidence.

## Host commands

Run from a reviewed checkout copied to the specific target host. The `--host`
and `--name` pair is mandatory and must match the host's actual address.

```bash
ops/actions-runner-fleet/install.sh \
  --host 10.230.50.201 --name oe-rva23-qemu-201

printf '%s\n' "$SHORT_LIVED_REGISTRATION_TOKEN" \
  | ops/actions-runner-fleet/register.sh \
      --host 10.230.50.201 --name oe-rva23-qemu-201
```

Registration deliberately leaves the service offline. After the trusted
workflow routing and branch protection are independently verified, activate
the root-owned policy explicitly:

```bash
ops/actions-runner-fleet/activate.sh \
  --host 10.230.50.201 --name oe-rva23-qemu-201 \
  --enable-reviewed-policy

ops/actions-runner-fleet/audit.sh \
  --host 10.230.50.201 --name oe-rva23-qemu-201
```

To remove a registered host, obtain a fresh short-lived removal token and pipe
it to `uninstall.sh`. It stops/disables the service and removes only the managed
Runner directory; Docker and QEMU packages are retained because they may be
shared host dependencies.

## Idempotent fleet redeployment

A **reviewed fleet redeployment** is an idempotent rerun of `install.sh` from
one exact protected-main archive against an already registered host. It
refreshes the complete managed package and libexec contract—including
`preflight.sh`, `cleanup.sh`, `docker-cleanup.py`, and `audit.sh`—without
re-registering the Runner, replacing its locked payload, or resetting an
enabled policy. Copying one missing helper by hand is not a redeployment and
can leave the installed files at mutually incompatible revisions.

Redeployment is for a package-complete, integrity-valid host. It is not an
incident-response substitute: a systemd package-integrity failure requires
quarantine, credential rotation, and trusted reimaging rather than this flow.

Redeploy from a freshly verified protected-main archive. Start with one host;
after that complete canary passes, independent hosts may use disjoint bounded
batches, while each host keeps the following per-host state machine:

1. Require the exact GitHub Runner to be online with `busy=false`, then stop
   only its exact systemd unit. Wait for GitHub to report it offline and prove
   both `Runner.Worker=0` and no running Docker container before changing host
   packages or managed files.
2. Read the installed root-owned `identity.conf` and pass `--allow-degraded`
   only when its existing `ALLOW_DEGRADED=true`; never infer or rewrite that
   immutable choice from the host's rollout stage.
3. Run the archive's `install.sh` with the exact `--host` and `--name`. Its
   existing identity check, pinned Runner verification, and policy-preserving
   path make this the supported way to repair missing packages and stale or
   absent installed helpers.
4. Run `activate.sh --enable-reviewed-policy` with the same identity arguments.
   Activation anonymously caches and verifies the digest-locked cleanup image
   when it is absent, then performs bounded cleanup and preflight before
   starting the service. This prevents root-owned output from an older QEMU
   build from trapping a freshly redeployed runner in the unprivileged host
   fallback. Then require `audit.sh` success, the service active/enabled, the
   GitHub Runner online with `busy=false`, and an empty Docker container
   inventory before advancing to the next host.

Stop the rollout on any identity, package, cleanup, audit, or state mismatch.
Do not update a live/busy Runner and do not deploy individual files outside the
installer.

A version change is not the same-version redeployment described above:
`install.sh` deliberately rejects an existing different Runner payload. It
requires the separately reviewed identity-preserving `upgrade.sh` sequence
below, not uninstall/re-registration or repeated installation over the old
payload. New code must pass complete CI and reach protected `main` before the
deployment archive is selected; then validate the canary before expansion.

## Per-job cleanup

GitHub-supported synchronous pre/post hooks run `job-guard.sh` and
`cleanup.sh` with a five-minute timeout. **Activation cleanup** is the full
workspace cleanup that runs before the Runner service starts. Activation first
requires the same digest-pinned base image to be locally cached; `audit.sh`
fails closed if that cache prerequisite is absent. **Job-start
cleanup** runs after the Runner has downloaded pinned actions, so it removes
only the exact configured repository workspace contents plus home and
Docker-client state; it deliberately preserves the sibling `_actions`,
`_temp`, and `_tool` directories required by the current job. **Completion
cleanup** first leaves the job workspace and then removes all verified Runner
work/home/Docker-state children. All phases share the same lock.

These hosts are dedicated to exactly one sequential Runner. A **managed
dependency container** is the temporary, long-running container created by
`prepare-build-deps.py` with the fixed recovery label, the bounded
`openeuler-builddeps-<pid>-<nonce>` name, the digest-pinned target image, and
the fixed sleep-loop command. At job start, cleanup inventories every running
container before its first mutation. It recovers the prior job's orphan only
when every running container exactly matches that complete managed identity;
one unknown, unlabeled, mutable-image, or command-mismatched container keeps
the original fail-closed behavior for the whole host. This does not authorize
a name-only or label-only deletion. When Docker is idle it removes all
stopped/created containers, dangling volumes, and unused custom networks, plus
only the workflow-defined `openeuler-builddeps:*` derived images. The digest-pinned
`ghcr.io/yinjiayi/openeuler-riscv64-rpmbuild` base image and all other image
caches are retained. The same locked base, with `--pull never`, is used as a
root cleanup container for root-owned QEMU build outputs in three exact bind
mounts; it has no network and cannot mount Runner credentials. Before the first
base pull, the empty/user-owned paths use host deletion. Every object list is
bounded to 512 entries and the hook itself is bounded to five minutes.

The **cleanup lock** is the persistent advisory lock that serializes root-run
activation cleanup with the non-root pre/post-job hooks. It lives at
`/opt/openeuler-actions-runner/.locks/<runner>.lock`, not inside the
Runner-writable `_state` tree. Its parent is `root:root:0755`, while the regular
lock file is `root:oegha:0660`; this lets both execution identities open the
same inode without letting workflow code replace it. Installation repairs the
exact owner/mode idempotently, and both cleanup and audit fail closed if the
directory, file type, ownership, or mode differs.

Persistent hardware is not equivalent to a clean JIT VM, so the public
repository routing restrictions remain mandatory.

If activation fails after changing enrollment from `false` to `true`, its EXIT
guard stops/disables the service and atomically restores `false`. A previously
enabled policy is never silently rewritten by a later audit or registration.

## Fleet audit

`fleet-audit.py` is read-only and requires an explicit stage:

```bash
python3 ops/actions-runner-fleet/fleet-audit.py \
  --stage canary --jobs 5 --output work/runner-audit/canary.json
```

The script never enrolls, installs, removes, or changes a host.

## Identity-preserving pinned Runner upgrade

This entrypoint supports only the reviewed **2.336.0 to 2.338.2** transition.
An upgrade replaces the official static payload, not the registered Runner
identity or a package workload. It preserves `.runner`, `.credentials`,
`.credentials_rsaparams`, `.env`, `.path`, `.service`, generated `svc.sh`, and
the `_work`, `_diag`, `_state` trees; it never reads credential values. Unknown
root entries or changed/missing/extra official payload files require review.

Use one exact, independently verified protected-main source archive. Place its
complete source tree and any pre-downloaded official Runner archives below a
root-owned non-writable ancestor such as `/root/runner-upgrade/`, not `/tmp` or
`/var/tmp`. Pre-downloaded archives are still checked against the hard-coded
official SHA-256 and size; neither an unverified cache nor a mutable release
URL is accepted. The old release is independently downloaded and compared
file-by-file, including modes and contained symlink targets, before replacement.
Extraction consumes the gzip archive once in physical member order, with
audited directories created first and safe symlinks created last. It rechecks
the exact member inventory and retains final byte/owner/mode verification;
it does not seek backwards through gzip to follow sorted filenames.
The supplied `--source-commit` is the coordinator's reviewed archive identity;
the host also fingerprints the entire fleet source directory between phases.

For this deprecated/offline fleet recovery, first require a fresh exact GitHub
Runner ID/name observation with `status=offline` and `busy=false`,
record resources and integrity, and run:

```bash
ops/actions-runner-fleet/upgrade.sh prepare \
  --host 10.230.50.201 --name oe-rva23-qemu-201 \
  --source-commit "$protected_main_sha" \
  --new-archive /root/runner-upgrade/actions-runner-linux-x64-2.338.2.tar.gz
```

Pass `--allow-degraded` only if the unchanged installed identity already
permits it. `prepare` refuses running Workers or containers before stopping,
disabling and runtime-masking the exact unit. It then requires no Listener,
Worker or running container, verifies the complete old payload, and stages
the new archive in root-only
`/var/lib/openeuler-actions-runner-upgrade/<name>/`. Already stopped units are
valid. Existing preparation state is not overwritten or silently replayed.

After `prepare` completes, the coordinator must re-read that exact Runner
through locally authenticated GitHub API and require `status=offline` and
`busy=false`. Write a root-owned mode-0600 JSON receipt with precisely these
fields (values below are examples; never fabricate an observation):

```json
{
  "schema_version": 1,
  "kind": "runner-upgrade-offline-observation",
  "repository": "yinjiayi/openeuler-riscv-packages",
  "host": "10.230.50.201",
  "name": "oe-rva23-qemu-201",
  "runner_id": 24,
  "prepared_nonce": "COPY_THE_NEW_PREPARE_NONCE",
  "source_commit": "COPY_THE_REVIEWED_PROTECTED_MAIN_SHA",
  "old_version": "2.336.0",
  "new_version": "2.338.2",
  "new_sha256": "baebf204307bac6193480852732f0aba2ae97b6c5597c244f4d5558390147c40",
  "status": "offline",
  "busy": false,
  "observed_at": "COPY_THE_FRESH_UTC_API_OBSERVATION_TIME"
}
```

This receipt is a trusted coordinator assertion, not a signature or an
independent GitHub authentication proof. Keep the underlying API response in
the operator evidence directory. It must postdate preparation, be no older
than five minutes immediately before mutation, and match the registered
Runner ID/name, host, repository, nonce, old/new release and source commit.

```bash
ops/actions-runner-fleet/upgrade.sh apply \
  --host 10.230.50.201 --name oe-rva23-qemu-201 \
  --source-commit "$protected_main_sha" \
  --github-receipt /root/runner-upgrade/offline-observation.json
```

`apply` rechecks quiescence and both payloads, creates a unique root-only backup
under `/var/backups/openeuler-actions-runner/`, consumes preparation once, and
replaces only the official payload roots. The backup contains the complete old
payload, release record, configuration/libexec contract and systemd template;
registration credentials remain in place and are never copied into evidence.
The complete same-source `install.sh` then refreshes all managed files. Final
checks require the new complete payload and unchanged registration identity,
runtime inodes/permissions, policy and degraded-host permission.
The runner, staged payload, backup and managed installation paths must be on
the same filesystem; cross-device layouts fail before the first payload rename
and require a separately reviewed deployment plan.
Before any service change or rollback guard is armed, read-only admission
requires an unconsumed prepared transaction, unchanged identity/source/policy
and the fresh receipt. A previous partial/completed transaction is rejected
unchanged; invoking `apply` again is not authorization to stop a recovered
Runner or roll back another attempt. A prepared host that restarted is likewise
rejected rather than silently stopped again.

Successful apply leaves the unit **disabled and stopped**, with its runtime
mask removed, awaiting the existing `activate.sh`/`audit.sh` sequence and a
fresh GitHub online, idle readback. Activation's ordinary documented cleanup
can remove CI workspace/cache state; the payload upgrade itself does not.
Do not count an upgrade or recovered capacity until those separate gates pass.

On an ordinary caught replacement/installer failure the complete old payload
and managed files are restored from the private backup; the service remains
disabled, stopped and runtime-masked. Restoration is **not success**, and the
deprecated old version must not be restarted. If restoration fails or power
loss/SIGKILL interrupts the transaction, keep the host stopped, retain the
state journal plus both old/failed payload trees, and perform a separately
reviewed restore of the exact backup and managed contract. Do not delete
preparation state, replay a consumed receipt, mix individual old/new files,
re-register, or automatically retry. Re-audit integrity and obtain a fresh
explicit recovery decision before another attempt. No backup/data cleanup is
performed automatically by this upgrade entrypoint.
