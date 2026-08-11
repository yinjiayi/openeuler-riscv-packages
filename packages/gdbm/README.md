<!-- SPDX-License-Identifier: Apache-2.0 -->
# gdbm

This directory packages the official stable GNU GDBM `1.26` release for
openEuler 24.03 LTS SP3 on `riscv64`/RVA23. The GNU archive is pinned by
SHA-256 `6a24504a14de4a744103dcb936be976df6fbe88ccff26065e54c1c47946f4a5e`.
Its 271 members have one `gdbm-1.26` root and no absolute path, parent
traversal, symlink, or hardlink. A detached signature is published upstream;
the package source contract keeps SHA-256 authoritative because the review
host had no OpenPGP verifier.

Snapshot `discovery-20260808T165000Z-9a89920c269462cd` freezes Arch core
`1.26-2`, AUR `android-riscv64-gdbm` `1.26-1`, Debian stable `1.24-2`, Fedora
44 `1:1.23-11.fc44`, openSUSE Tumbleweed `1.26-1.5`, and Ubuntu 26.04 LTS
`1.26-1build1`. The AUR row is metadata-only corroboration; no PKGBUILD or
distribution spec was executed. Fedora's epoch is retained for upgrade
ordering while the source advances to official stable `1.26`.

The fixed target repodata contains every declared BuildRequires, including
`readline-devel`, `libtool`, and `texinfo`. `%check` runs the complete upstream
GDBM and ndbm compatibility suite. The installed smoke test stores and fetches
a persistent record, writes it to an explicit dump file, restores that dump,
and fetches the same record from the restored database. GDBM 1.26's generated
`gdbm_dump(1)` page says an omitted output file uses standard error, while the
authoritative Texinfo manual and the 1.26 implementation use standard output;
the explicit file avoids that documentation discrepancy. The ASCII dump also
Base64-encodes record data, so grepping it for the original plaintext key is
not a valid content check. No downstream or RISC-V patch is currently required.
RISC-V build status remains `unknown` until the locked QEMU CI image runs the
RPM build.

External source licenses remain those of upstream. Apache-2.0 covers only the
original packaging metadata, test, and documentation in this directory.
