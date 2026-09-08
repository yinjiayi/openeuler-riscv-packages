<!-- SPDX-License-Identifier: Apache-2.0 -->
# libassuan

This directory packages the official stable libassuan `3.0.2` release for
openEuler 24.03 LTS SP3 on `riscv64`/RVA23. The GnuPG archive is pinned by
SHA-256 `d2931cdad266e633510f9970e1a2f346055e351bb19f9b78912475b8074c36f6`.
Its 122 members have one `libassuan-3.0.2` root and no absolute path, parent
traversal, symlink, or hardlink. Upstream also publishes a detached signature;
SHA-256 remains the source contract because the review host had no OpenPGP
verifier.

Snapshot `discovery-20260808T165000Z-9a89920c269462cd` freezes Arch core
`3.0.0-1`, AUR `android-riscv64-libassuan` `3.0.0-1`, Debian stable `3.0.2-2`,
Fedora 44 GA `2.5.7-5.fc44`, openSUSE Tumbleweed `3.0.2-1.6`, and Ubuntu
26.04 LTS `3.0.2-2build1`. The AUR row is metadata-only corroboration; no
PKGBUILD or distribution spec was executed. The independently reviewed
official index confirms stable `3.0.2`.

Version 3 changes the shared-library SONAME from `libassuan.so.0` to
`libassuan.so.9`. The runtime is therefore emitted as `libassuan9`, leaving the
target's existing ABI 0 package installed, while `libassuan-devel` points new
builds at ABI 9. The fixed target repodata provides all BuildRequires.
`%check` runs the complete upstream suite, and the installed smoke test creates
and releases a real Assuan context. No downstream or RISC-V patch is required;
RISC-V status remains `unknown` until locked QEMU CI runs.

External source licenses remain those of upstream. Apache-2.0 covers only the
original packaging metadata, test, and documentation in this directory.
