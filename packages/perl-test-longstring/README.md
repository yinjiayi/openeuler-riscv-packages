<!-- SPDX-License-Identifier: Apache-2.0 -->
# Test::LongString 0.17

Noarch Perl assertions for long-string comparisons on openEuler 24.03
LTS SP3, riscv64/RVA23. Frozen Ubuntu and Debian stable identify
libtest-longstring-perl 0.17-3; no distribution recipe was executed.

The fixed CPAN archive matches MetaCPAN and the author's CHECKSUMS
SHA-256. The 2021 historical SHA-1 index signature and expired PAUSE
subkey are advisory, not a detached archive signature. The full archive
SHA-256 is mandatory. The original README carries Rafael Garcia-Suarez's
explicit same-terms-as-Perl grant and is installed as the license notice.

The original Makefile.PL is used without source patches. The complete
default `make test` suite is preserved, and the POD syntax and coverage
dependencies are checked to avoid the original optional self-skips.
Installed smoke exercises exact equality, presence and absence of text.
Host validation does not substitute for actual target build/install.
