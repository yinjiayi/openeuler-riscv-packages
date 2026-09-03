<!-- SPDX-License-Identifier: Apache-2.0 -->
# simpleini

This directory packages upstream `https://github.com/brofield/simpleini` version `4.26` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

Release 3 retains the upstream-supported system GoogleTest path and raises the
package timeout to 180 minutes. Exact-head CI resolved the complete 124-package,
170 MB dependency transaction, but the former 60-minute budget expired during
dependency downloads before `rpmbuild` began; it therefore provided no package
compilation or test result. The registered CTest suite remains enabled and runs
during `%check`, and the RISC-V build status remains `unknown` pending fresh CI
evidence.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
