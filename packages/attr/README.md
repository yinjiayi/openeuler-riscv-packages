<!-- SPDX-License-Identifier: Apache-2.0 -->
# attr

This directory packages the official stable attr `2.6.0` release for
openEuler 24.03 LTS SP3 on `riscv64`/RVA23. The Savannah archive is pinned by
SHA-256 `6c8a2148a7b85043b68492bce43316b0e2e214fc4e628c7ede078e76e216330b`.
Its 148 members have one `attr-2.6.0` root and no absolute path, parent
traversal, symlink, or hardlink. A detached signature is published upstream;
the package source contract keeps SHA-256 authoritative because the review
host had no OpenPGP verifier.

Snapshot `discovery-20260808T165000Z-9a89920c269462cd` freezes Arch core
`2.6.0-1`, Debian stable `1:2.5.2-3`, Fedora 44 `2.5.2-8.fc44`, openSUSE
Tumbleweed `2.6.0-1.2`, and Ubuntu 26.04 LTS `1:2.5.2-4`. AUR exposed only a
VCS `attr-git` clue for this component; it was excluded and no PKGBUILD was
read or executed. Fedora 44 dist-git was reviewed only as text.

The fixed target repodata contains every declared BuildRequires. `%check`
runs the complete upstream test target without deleting or conditionally
skipping its xattr tests. The installed smoke test writes, reads, removes, and
confirms removal of a real `user.*` extended attribute. No downstream or
RISC-V patch is currently required. Exact-head locked QEMU CI reached the full
test suite: `test/attr.run` passed, while the root-only `getfattr` and `restore`
tests received `EPERM` when writing `trusted.*` extended attributes to symbolic
links. Those operations require `CAP_SYS_ADMIN` and compatible filesystem
namespace semantics that the unprivileged container does not provide; this is
not a RISC-V instruction or QEMU CPU failure. The unchanged full suite is
therefore conservatively routed as `needs-native-riscv` and requires a
controlled privileged native RISC-V validation environment. Native hardware
alone does not guarantee the required privileges or filesystem behavior, and
RISC-V build status remains `unknown` until that validation is available.

External source licenses remain those of upstream. Apache-2.0 covers only the
original packaging metadata, test, and documentation in this directory.
