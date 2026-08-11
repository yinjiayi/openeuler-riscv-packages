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
`libattr-devel`. `%check` runs the complete upstream test target without a
skip path; the installed smoke test creates and reads a real filesystem ACL.
No downstream or RISC-V patch is currently required. RISC-V build status
remains `unknown` until the locked QEMU CI image runs the RPM build.

External source licenses remain those of upstream. Apache-2.0 covers only the
original packaging metadata, test, and documentation in this directory.
