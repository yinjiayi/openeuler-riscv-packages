<!-- SPDX-License-Identifier: Apache-2.0 -->
# julius-speech

This directory packages upstream `https://github.com/julius-speech/julius` version `4.6` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The source root is the top-level directory entered by the RPM `%prep` stage after extracting the verified archive. Downstream release `2` selects the archive's exact `julius-4.6` source root instead of the RPM name-derived `julius-speech-4.6` path. The source, build features, and complete upstream `%make_build check` command remain unchanged; the RISC-V build status remains `unknown` pending fresh exact-head CI evidence.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
