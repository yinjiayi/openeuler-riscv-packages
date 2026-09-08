<!-- SPDX-License-Identifier: Apache-2.0 -->
# libidn2

This directory packages the official stable GNU Libidn2 `2.3.8` release for
openEuler 24.03 LTS SP3 on `riscv64`/RVA23. The GNU archive is pinned by
SHA-256 `f557911bf6171621e1f72ff35f5b1825bb35b52ed45325dcdee931e5d3c0787a`.
Its 1,676 members have one `libidn2-2.3.8` root and no absolute path, parent
traversal, symlink, or hardlink. GNU publishes a detached signature under key
fingerprint `B1D2 BD13 75BE CB78 4CF4 F8C4 D73C F638 C53C 06BE`; the package
source contract keeps SHA-256 authoritative because the review host had no
OpenPGP verifier.

Snapshot `discovery-20260808T165000Z-9a89920c269462cd` accidentally merged
Libidn and Libidn2 under one component key, so this package deliberately keeps
only the Libidn2 rows: Arch core `2.3.8-1`, AUR
`android-riscv64-libidn2` `2.3.8-1`, Debian stable `2.3.8-2`, Fedora 44
`2.3.8-3.fc44`, openSUSE Tumbleweed `2.3.8-1.5`, and Ubuntu 26.04 LTS
`2.3.8-4build1`. AUR is metadata only; no PKGBUILD or Fedora spec was
executed.

The fixed target repodata contains every declared BuildRequires, including
`libunistring-devel` and `texinfo`. `%check` runs the complete upstream test
target. The installed smoke test performs real UTF-8 to Punycode and Punycode
to UTF-8 conversions. No downstream or RISC-V patch is currently required.
RISC-V build status remains `unknown` until the locked QEMU CI image runs the
RPM build.

External source licenses remain those of upstream. Apache-2.0 covers only the
original packaging metadata, test, and documentation in this directory.
