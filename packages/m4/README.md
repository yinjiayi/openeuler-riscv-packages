<!-- SPDX-License-Identifier: Apache-2.0 -->
# m4

This directory packages GNU M4 `1.4.21` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. Fedora 44 was the priority discovery source; Arch stable, Debian stable, and openSUSE Tumbleweed corroborated the same official stable release. The GNU release archive is pinned by SHA-256.

No external distribution recipe or AUR content was executed. All upstream functional checks remain mandatory, followed by an installed macro-expansion smoke test, with no build-time network access.

The upstream `stackovf.test` diagnostic depends on stack-overflow signal and guard-page semantics that Linux-user QEMU does not provide. The package therefore retains the complete upstream test suite and is explicitly routed to native RISC-V validation; no test is overwritten, excluded, or converted into a synthetic skip. Fedora 44's current dist-git was also used to cross-check the complete bundled-license expression, generated Info directory index removal, and `%find_lang` ownership of all installed translations. Gnulib's update-copyright test replaces the common cleanup trap and can leave a root-owned mode-0700 temporary directory; the SPEC makes that directory readable and traversable by the unprivileged CI artifact collector on shell exit without changing any test result.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
