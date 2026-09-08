<!-- SPDX-License-Identifier: Apache-2.0 -->
# md4c

This directory packages MD4C 0.5.3 for openEuler 24.03 LTS SP3 on
riscv64/RVA23. The immutable discovery snapshot is the fixed metadata capture
named `discovery-20260808T165000Z-9a89920c269462cd`; it records Arch stable
0.5.3, Fedora 44 GA 0.5.1, Debian stable 0.5.2, openSUSE Tumbleweed 0.5.3,
and Ubuntu GA 0.5.2 lineages. An exact-name read-only AUR RPC query on
2026-08-12 returned no result. No AUR or distribution packaging recipe was
read or executed.

The current stable `release-0.5.3` tag resolves to upstream commit
`472c417005c2c71b8617de4f7b8d6b30411d78f4`. Its official archive is pinned
by SHA-256. Pre-extraction inspection found one root, no links, no special
entries, and no absolute or parent-traversing path. The packaged parser is
MIT licensed. The bundled CommonMark corpus is CC-BY-SA-4.0, its test tools
are BSD-2-Clause, and the normalization helper is MIT; the RPM license
expression and installed license notices account for all three terms.

The full upstream check gate runs every bundled `spec*.txt` suite and all 29
pathological stress cases without a skip or ignored failure. Installed smoke
then compiles against the public parser API and exercises `md2html`. MD4C is
absent from the fixed target repository, and its BuildRequires are present;
target RPM, install, and smoke status remains unknown until exact-head QEMU
CI completes.

External source licenses remain upstream's. Apache-2.0 covers only this
repository's original packaging metadata, scripts, tests, and documentation.
