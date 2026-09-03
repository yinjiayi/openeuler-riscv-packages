<!-- SPDX-License-Identifier: Apache-2.0 -->
# simpleini

This directory packages upstream `https://github.com/brofield/simpleini` version `4.26` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

Release 3 retains the upstream-supported system GoogleTest path and raises the
package timeout to 180 minutes. Exact-head CI resolved the complete 124-package,
170 MB dependency transaction within the enlarged budget; run `33712645713`
compiled and passed the registered CTest suite. RPM assembly then failed because
automatic debuginfo generation emitted an empty file list: SimpleIni is a
header-only library and installs no compiled object containing debug symbols.

Release 4 disables only the inapplicable automatic debuginfo subpackage. The
complete upstream GoogleTest/CTest suite and all library functionality remain
enabled. The RISC-V build status remains `unknown` pending fresh exact-head RPM
and installed-smoke evidence.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
