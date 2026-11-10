<!-- SPDX-License-Identifier: Apache-2.0 -->
# Test::Script 1.31

Noarch Perl test support for script execution and stdout/stderr capture.
Target: openEuler 24.03 LTS SP3, riscv64/RVA23.

The official CPAN archive SHA-256 agrees with MetaCPAN and the author's
CPAN CHECKSUMS. Discovery lineage is the frozen Ubuntu resolute/universe
libtest-script-perl 1.31-1 row and Debian stable libtest-script-perl 1.29-2;
no distribution recipe was executed.

The original project LICENSE and module grant Perl terms. Dist::Zilla 6.033's
MakeMaker template is the parent of Author::Plicease::MakeMaker 2.79, which
adds Perl-version setup, the PM map and formatting. Its companion Tests.pm
contains the eight shipped author/release templates and the Test2 diagnostic
template (the shipped default t/00_diag.t has the generated prerequisite list).
There is no bundled inc/ directory. Both fixed generator sources grant the
same Perl terms. The notice-only patch adds their distinct original grants and
copyrights without changing executable code, generated tests, or the upstream
LICENSE. The official generator archives are audit inputs, not build inputs.

The SPEC runs the unchanged complete upstream default `make test` from the
fixed release. Upstream author/release checks under xt/ stay outside the default
target as shipped. Installed smoke exercises compilation, execution, stdout,
and stderr using a private fixture. No native-hardware or performance claim is
made; host checks and source verification do not establish target CI success.
