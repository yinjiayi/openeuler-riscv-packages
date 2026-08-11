<!-- SPDX-License-Identifier: Apache-2.0 -->
# m4

This directory packages GNU M4 `1.4.21` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. Fedora 44 was the priority discovery source; Arch stable, Debian stable, and openSUSE Tumbleweed corroborated the same official stable release. The GNU release archive is pinned by SHA-256.

No external distribution recipe or AUR content was executed. All upstream functional checks remain mandatory and are run serially, followed by an installed macro-expansion smoke test, with no build-time network access.

The upstream `stackovf.test` diagnostic depends on stack-overflow signal semantics that Linux-user QEMU does not provide. The SPEC records only that test as the upstream-standard `77` skip, matching the independently reviewed openSUSE Tumbleweed QEMU policy; 242 manual checks and the installed-package smoke test remain mandatory. Remove the skip when CI moves to native RISC-V validation. Fedora 44's current dist-git was also used to cross-check the complete bundled-license expression and removal of the generated Info directory index. A test-exit trap only restores owner access to gnulib's deliberately restricted temporary directory so failed CI runs can retain their evidence; it does not alter any test result.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
