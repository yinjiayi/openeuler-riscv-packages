<!-- SPDX-License-Identifier: Apache-2.0 -->
# acl

This directory packages the official stable ACL `2.4.0` release for openEuler
24.03 LTS SP3 on `riscv64`/RVA23. The Savannah archive is pinned by SHA-256
`e661131456d2708a01c614a0f400e11d7d1bfaeb6f3e74b75bb980b72f0161a3`.
Its 275 members have one `acl-2.4.0` root and no absolute path, parent
traversal, symlink, or hardlink. A detached signature is published upstream;
the package source contract keeps SHA-256 authoritative because the review
host had no OpenPGP verifier.

Snapshot `discovery-20260808T165000Z-9a89920c269462cd` freezes Arch core
`2.4.0-1`, Debian stable `2.3.2-2`, Fedora 44 `2.3.2-6.fc44`, openSUSE
Tumbleweed `2.4.0-1.2`, and Ubuntu 26.04 LTS `2.3.2-2`. The only matching AUR
clue was stale `acl-git` metadata; it was excluded and no PKGBUILD was read or
executed. Fedora 44 dist-git was reviewed only as text.

The fixed target repodata contains every declared BuildRequires, including
`libattr-devel` and the `runuser` provider. `%check` runs the complete upstream
test target without a skip or XFAIL path; the installed smoke test creates and
reads a real filesystem ACL. The protected root-build workspace is a host bind
mount whose transport rejects execution by the suite's unprivileged `bin`
identity even when the path modes and ACLs permit it. `%check` therefore copies
the exact built tree to container-local temporary storage while preserving its
timestamps, grants execute-only traversal on the `mktemp` parent and
read/traversal on only that copy, verifies both libtool wrappers as `bin`, and
runs the complete parallel upstream suite there. Preserving timestamps keeps
the generated `configure` script current, so `%check` does not invoke
maintainer-only Autoconf merely because the tree was copied.

Exact-head CI run `31472087683` was bound to commit
`ffac31793c9097ebad4162116842d26763718bab`. Its locally rehashed build artifact
has SHA-256 `6cf246af07395a12562d931b1a8ba26c07a2990eb3d49a3dba7fd00ad18645af`.
The artifact showed the synthetic block device returning EACCES before its ACL
grant and EPERM afterwards. Linux commit
`d58772d8520c7ef247c4b95c9bd76d3a25da9ff5` documents the relevant ordering in
`inode_permission`: POSIX ACL/DAC permission runs before the device-cgroup hook,
whose denial is EPERM. The package-local test patch therefore accepts only
ENXIO or EPERM after that ACL grant. The earlier EACCES assertion and all
character-device, FIFO, ownership, directory, and CAP_FOWNER checks are
unchanged. Remove the patch when upstream carries the same contract or the
locked CI allows synthetic block device `91:64` and consistently reaches ENXIO.

This is a test-environment adaptation, not evidence of a successful RISC-V
build. RISC-V build status remains `unknown` until the repaired exact head runs
the full suite in the locked QEMU CI image.

External source licenses remain those of upstream. Apache-2.0 covers only the
original packaging metadata, test, and documentation in this directory.
