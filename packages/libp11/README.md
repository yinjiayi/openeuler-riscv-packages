<!-- SPDX-License-Identifier: Apache-2.0 -->
# libp11

This directory packages the OpenSC libp11 0.4.21 release for openEuler 24.03
LTS SP3 on `riscv64`/RVA23. The release asset is downloaded from the official
GitHub project and verified against SHA-256
`efdb523aef8613d447e6a2d38227d4b389866f4bcf4b503130acd7f759490847`.
Its 216 archive entries are regular files or directories under the
`libp11-0.4.21/` root with no parent traversal.

The frozen discovery snapshot records older libp11 versions in Arch, Debian,
openSUSE, and Ubuntu, plus Fedora's `openssl-pkcs11` package for the same
upstream component. The official 0.4.21 release is newer than that snapshot.
The source carries LGPL-2.1-or-later terms in `COPYING`.

The package builds the wrapper library and the OpenSSL 3 provider and engine.
The complete upstream `make check` suite uses the SoftHSM software token and
OpenSC's `pkcs11-tool`; both dependencies exist in the target openEuler RVA23
repository. The installed smoke test links a C client and creates/frees a
public libp11 context. Neither test path requires a physical smart card.
Target build and installation status remain unknown until CI runs on the
pinned openEuler RISC-V image.
