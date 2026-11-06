<!-- SPDX-License-Identifier: Apache-2.0 -->
# libunistring

This directory packages the official stable GNU libunistring `1.4.2` release
for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. The GNU archive is pinned by
SHA-256 `e82664b170064e62331962126b259d452d53b227bb4a93ab20040d846fec01d8`.
Its 2,396 members have one `libunistring-1.4.2` root and no absolute path,
parent traversal, symlink, or hardlink. A detached signature is published
upstream; the package source contract keeps SHA-256 authoritative because the
review host had no OpenPGP verifier.

Snapshot `discovery-20260808T165000Z-9a89920c269462cd` freezes Arch core
`1.4.2-1`, AUR `android-riscv64-libunistring` `1.4.1-1`, Debian stable
`1.3-2`, Fedora 44 `1.1-11.fc44`, openSUSE Tumbleweed `1.4.2-1.4`, and Ubuntu
26.04 LTS `1.3-2build1`. AUR is metadata-only corroboration; no PKGBUILD or
distribution spec was executed. The library's upstream dual-license choice is
preserved as `GPL-2.0-or-later OR LGPL-3.0-or-later`.

The fixed target repodata contains every declared BuildRequires. `%check`
runs the complete upstream Unicode test target without omissions. The
installed smoke test compiles and links against the public API, then validates
the character length of a two-code-point UTF-8 string. Exact-head Package CI
run `33722565386` at commit
`416bceb39289eb8fe98a568a59876e55a7ce2bcd` entered `rpmbuild` with 3,087
seconds remaining, compiled normally without an error, and then exhausted the
former 60-minute package budget. Release 2 raises only the bounded QEMU timeout
to 180 minutes; it does not change the source or omit `%check`. No downstream
or RISC-V patch is currently required, and RISC-V build status remains
`unknown` pending fresh exact-head RPM and installed-smoke evidence.

External source licenses remain those of upstream. Apache-2.0 covers only the
original packaging metadata, test, and documentation in this directory.
