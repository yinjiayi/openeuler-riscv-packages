<!-- SPDX-License-Identifier: Apache-2.0 -->
# libuv

This directory packages upstream `https://github.com/libuv/libuv` version `1.52.1` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The immutable discovery snapshot cross-checks all six configured distribution sources. Only the official stable tag archive and independently calculated SHA-256 are build inputs; no AUR recipe or distribution build hook is read or executed.

The official Fedora 44 `libuv` dist-git SPEC was retrieved as read-only reference evidence on 2026-08-11 (SHA-256 `20d9f98dc751d9a1a31247f0b409fb1efc7f6da639df2acc9158bc01681fd994`). Its current Fedora 44 version is also `1.52.1`; it corroborates the composite source license, the shared/development/static payload, both upstream test executables, a tenfold test timeout allowance, and removal of CMake-installed duplicate license files. The Fedora SPEC was not executed or copied as trusted instructions.

The official upstream archive `libuv-1.52.1.tar.gz` independently verifies as SHA-256 `478baf2599bfbc882c355288c9cb6f92e0e7dda435fa04031fa5b607cf3f414c`. `%check` exports upstream's explicit root-test opt-in before `%ctest`; this fixes shell scoping demonstrated by the earlier exact-head CI artifact while retaining both shared and static upstream suites. QEMU-specific skips remain only those already implemented by upstream under its `QEMU` build option.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
