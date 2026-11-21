<!-- SPDX-License-Identifier: Apache-2.0 -->
# Devel::StrictMode 0.003

The noarch `perl-devel-strictmode` RPM supplies the Perl constants `STRICT` and `LAX` on openEuler 24.03 LTS SP3 riscv64/RVA23. `STRICT` is false by default and true when the caller enables the documented testing environment flags.

The official CPAN archive SHA-256 matches MetaCPAN and the publisher checksum list. The historic archive manifest signature is supplementary evidence only. The upstream `LICENSE` contains both complete license texts; `LICENSE` and `COPYRIGHT` are installed verbatim.

The original MakeMaker default test command runs both upstream test files. The installed smoke check exercises the default and explicitly enabled constants in separate Perl processes. No RISC-V patch or native-only dependency is known; target RPM build and install evidence must come from CI.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
