<!-- SPDX-License-Identifier: Apache-2.0 -->
# libgpg-error

This directory packages the official stable libgpg-error `1.61` release for
openEuler 24.03 LTS SP3 on `riscv64`/RVA23. The GnuPG archive is pinned by
SHA-256 `7a85413f2bc354f4f8aa832b718af122e48965e9e0eb9012ee659c13c6385c93`.
Its 285 members have one `libgpg-error-1.61` root and no absolute path,
parent traversal, symlink, or hardlink. Upstream also publishes a detached
signature; SHA-256 remains the source contract because the review host had
no OpenPGP verifier.

Snapshot `discovery-20260808T165000Z-9a89920c269462cd` freezes Arch core
`1.61-1`, AUR `android-riscv64-libgpg-error` `1.58-1`, Debian stable
`1.51-4`, Fedora 44 GA `1.58-2.fc44`, openSUSE Tumbleweed `1.61-2.1`, and
Ubuntu 26.04 LTS `1.58-2`. The AUR row is metadata-only corroboration; no
PKGBUILD or distribution spec was executed. The independently reviewed
official index advances the source to stable `1.61`.

The fixed target repodata contains every declared BuildRequires, including
`gawk`, `gettext-devel`, and `texinfo`. `%check` runs the complete enabled C
library test suite. The installed smoke test queries the tools and links a
real error-code conversion program through `pkg-config`. No downstream or
RISC-V patch is currently required. RISC-V build status remains `unknown`
until the locked QEMU CI image builds and installs the RPMs.

External source licenses remain those of upstream. Apache-2.0 covers only the
original packaging metadata, test, and documentation in this directory.
