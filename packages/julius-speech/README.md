<!-- SPDX-License-Identifier: Apache-2.0 -->
# julius-speech

This directory packages upstream `https://github.com/julius-speech/julius` version `4.6` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The source root is the top-level directory entered by the RPM `%prep` stage after extracting the verified archive. Downstream release `2` selects the archive's exact `julius-4.6` source root instead of the RPM name-derived `julius-speech-4.6` path. Exact-head CI for release `2` then reached compilation and showed that upstream includes GCC's x86-only `cpuid.h` on RISC-V even though no x86 SIMD implementation is enabled. Release `3` restricts that header to x86 targets, preserving the existing scalar DNN implementation and complete upstream `%make_build check` command. The RISC-V build status remains `unknown` pending fresh exact-head CI evidence for this repair.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
