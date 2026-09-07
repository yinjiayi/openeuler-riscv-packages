<!-- SPDX-License-Identifier: Apache-2.0 -->
# libgcrypt

This directory packages GNU libgcrypt 1.12.2 for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. CI fetches and verifies the official archive with networking enabled, builds the shared library and development tools, and runs the complete upstream check suite.

Exact-head CI run `33362923539` at commit `c6b6927b9bea4920f7916298b3d1162f54792fa9` compiled the RISC-V implementation and passed all 39 upstream tests, with two intentionally large test modes reported by upstream as not run. Packaging then failed because the devel manifest named `gcrypt-module.h`, while the verified 1.12.2 install log shows that upstream installs only the public `gcrypt.h` header. Release 2 removes only that nonexistent file entry. A fresh exact-head build and installed-RPM smoke remain authoritative; this evidence is not a published RPM or SRPM.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
