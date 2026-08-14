<!-- SPDX-License-Identifier: Apache-2.0 -->
# wdiff

This directory packages GNU wdiff 1.2.2 for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. `Source0` is the immutable archive named by GNU's official
release index as both the highest version and the current `wdiff-latest`
release. Its SHA-256 was calculated locally. All 463 archive members were
audited as one safe `wdiff-1.2.2/` tree with no links, special files, absolute
paths, parent-directory escapes, or additional top-level roots.

Frozen discovery snapshot `discovery-20260808T165000Z-9a89920c269462cd`
records Arch Extra `1.2.2-5`, Fedora 44 GA `1.2.2-57.fc44`, openSUSE
Tumbleweed `1.2.2-9.7`, Debian 13 stable `1.2.2-9`, and Ubuntu 26.04 LTS GA
`1.2.2-9build1`. A read-only AUR RPC name search returned only the distinct
`cwdiff`, `cwdiff-git`, and `dwdiff` projects; no AUR recipe or distribution
build script was fetched or executed.

The package runs upstream's complete four-case GNU Autotest suite, including
the pseudo-terminal pager acceptance case, without skips or expected failures.
All four cases passed in a fresh native RISC-V build after the supplemental
host was compiled for its actual hardware ISA. That host does not implement
RVA23 and therefore is not target-runtime evidence. The installed smoke checks
the version, the runtime `diffutils` dependency, the documented exit status for
changed input, and the exact deleted/inserted word markers. Target QEMU CI
remains authoritative and `target.riscv_status` stays `unknown` until it
finishes.

Upstream source headers and `COPYING` license the installed program under
GPL-3.0-or-later. Apache-2.0 covers only this repository's original packaging
metadata and smoke script.
