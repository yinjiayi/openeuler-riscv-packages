<!-- SPDX-License-Identifier: Apache-2.0 -->
# simple-password

This directory packages upstream `https://github.com/ESzPa/spass` version `0.1.1` release `7` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

Downstream release `3` adds the fixed-repository `vim-common` provider required by upstream's `xxd` source-generation command and configures explicit CMake source and out-of-source build directories. Release `4` adds the immutable supplemental repository's `argparse` provider for upstream's `argparse/argparse.hpp` include. Release `5` raises the package timeout to 180 minutes after both exact-head CI attempts resolved the complete 125-package, 177 MB dependency transaction but exhausted the former 60-minute budget during dependency downloads before `rpmbuild` began. Release `6` adds deterministic unit coverage for the generation primitives after exact-head artifact review showed that upstream registered zero CTest tests; release `7` corrects the downstream patch hunk length so the test source retains its return statement and closing brace. `%check` fails closed if CTest ever registers zero tests. The RISC-V build status remains `unknown` pending a successful exact-head CI build.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
