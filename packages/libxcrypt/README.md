<!-- SPDX-License-Identifier: Apache-2.0 -->
# libxcrypt

This directory packages the official stable libxcrypt `4.5.2` release for
openEuler 24.03 LTS SP3 on `riscv64`/RVA23. The signed GitHub release asset is
pinned by SHA-256
`71513a31c01a428bccd5367a32fd95f115d6dac50fb5b60c779d5c7942aec071`.
Its 178 members have one `libxcrypt-4.5.2` root and no absolute path, parent
traversal, symlink, or hardlink. SHA-256 remains the source contract because
the review host had no OpenPGP verifier for the published detached signature.

Snapshot `discovery-20260808T165000Z-9a89920c269462cd` freezes Arch core
`4.5.2-1`, AUR `android-riscv64-libxcrypt` `4.5.2-1`, Debian stable
`1:4.4.38-1`, Fedora 44 GA `4.5.2-3.fc44`, openSUSE Tumbleweed `4.5.2-2.4`,
and Ubuntu 26.04 LTS `1:4.5.1-1`. The AUR row is metadata-only corroboration;
no PKGBUILD or distribution spec was executed. The official release asset
confirms stable `4.5.2`.

The target repository currently carries libxcrypt `4.4.36`; this build keeps
the compatible `libcrypt.so.1` ABI and all upstream hash methods. Every
declared BuildRequires, including the Perl modules used by the test generator,
is present in fixed RVA23 repodata. `%check` runs the complete upstream suite.
The installed smoke test performs a real SHA-512 password hash with `crypt_r`.
No downstream or RISC-V patch is included; RISC-V status stays `unknown` until
the locked QEMU CI image runs.

External source licenses remain those of upstream. Apache-2.0 covers only the
original packaging metadata, test, and documentation in this directory.
