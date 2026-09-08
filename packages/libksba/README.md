<!-- SPDX-License-Identifier: Apache-2.0 -->
# libksba

This directory packages the official stable libksba `1.8.0` release for
openEuler 24.03 LTS SP3 on `riscv64`/RVA23. The GnuPG archive is pinned by
SHA-256 `296b9db9095749f2aa104202d7ab7fd09ad10710e00780a709c9754b1a1d9292`.
Its 179 members have one `libksba-1.8.0` root and no absolute path, parent
traversal, symlink, or hardlink. Upstream also publishes a detached signature;
SHA-256 remains the source contract because the review host had no OpenPGP
verifier.

Snapshot `discovery-20260808T165000Z-9a89920c269462cd` freezes Arch core
`1.8.0-1`, AUR `android-riscv64-libksba` `1.6.7-2`, Debian stable `1.6.7-2`,
Fedora 44 GA `1.6.7-5.fc44`, openSUSE Tumbleweed `1.8.0-1.3`, and Ubuntu
26.04 LTS `1.6.7-2build1`. The AUR row is metadata-only corroboration; no
PKGBUILD or distribution spec was executed. The independently reviewed
official index advances the source to stable `1.8.0`.

The fixed target repodata contains all declared BuildRequires, including
`libgpg-error-devel` and `libgcrypt-devel`. `%check` runs the complete
upstream certificate, CMS, reader, writer, and parser suite. The installed
smoke test links and runs `ksba_check_version` through the installed
`pkg-config` contract. No downstream or RISC-V patch is currently required.
RISC-V status remains `unknown` until the locked QEMU CI image runs.

External source licenses remain those of upstream. Apache-2.0 covers only the
original packaging metadata, test, and documentation in this directory.
