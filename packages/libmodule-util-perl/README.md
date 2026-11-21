<!-- SPDX-License-Identifier: Apache-2.0 -->
# perl-module-util

This directory packages upstream `https://metacpan.org/dist/Module-Util` version `1.09` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The fixed archive digest agrees with MetaCPAN and signed PAUSE CHECKSUMS.
The recipe runs the unmodified upstream Build.PL and both default test files,
including POD and POD coverage. The nondefault catalog-wide test is not run.

The notice-only patch retains the complete copyright and license paragraph
from the Module::Build::Compat 0.4003 donor that generated the shipped
Makefile.PL. The donor archive and the matching generated wrapper were
verified byte-for-byte; the patch does not modify source code or tests.
Remove the extra notice only if upstream no longer ships that generated
wrapper or includes its original notice in a release.

The installed smoke verifies that pm_which locates the same Module::Util
module as the Perl interpreter.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
