<!-- SPDX-License-Identifier: Apache-2.0 -->
# julius-speech

This directory packages upstream `https://github.com/julius-speech/julius` version `4.6` release `5` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The source root is the top-level directory entered by the RPM `%prep` stage after extracting the verified archive. Downstream release `2` selects the archive's exact `julius-4.6` source root instead of the RPM name-derived `julius-speech-4.6` path. Exact-head CI for release `2` then reached compilation and showed that upstream includes GCC's x86-only `cpuid.h` on RISC-V even though no x86 SIMD implementation is enabled. Release `3` restricts that header to x86 targets, preserving the existing scalar DNN implementation and complete upstream `%make_build check` command. Exact-head run `33676018135` verified the release `3` source and dependencies, then failed first in `%prep` because strict GNU patch could not apply the hand-written hunk. Release `4` regenerates the semantically unchanged hunk with standard three-line unified-diff context; it applies to the verified archive with GNU patch and `--fuzz=0`.

Exact-head run `33678330024` for commit `0b8632e6e2aa97766a139765e86cfac25d6f0961` applied the CPUID patch and compiled on RISC-V until `libsent/src/phmm/calc_dnn.c` called `omp_get_max_threads` and `omp_get_thread_num` without declarations. Configure had enabled OpenMP with `-fopenmp`, but upstream includes `omp.h` only inside a SIMD conditional that is false on RISC-V even though the calls are guarded solely by `_OPENMP`. Release `5` includes `omp.h` whenever `_OPENMP` is defined. OpenMP remains enabled, scalar DNN behavior and the full `%make_build check` command remain unchanged, and the RISC-V build status remains `unknown` pending fresh exact-head CI evidence for release `5`.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
