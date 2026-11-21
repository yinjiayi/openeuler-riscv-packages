<!-- SPDX-License-Identifier: Apache-2.0 -->
# perl-test-api

This directory packages upstream `https://metacpan.org/dist/Test-API` version `0.010` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The fixed CPAN archive SHA-256 matches MetaCPAN and signed PAUSE CHECKSUMS.
The build retains the original Apache-2.0 license and reads the following
notices verbatim from verified source archives:

- Dist-Zilla 6.011: same-Perl terms for the generated MakeMaker wrapper.
- Dist-Zilla-Plugin-Test-ReportPrereqs 0.027: Apache-2.0 terms for the
  generated prerequisite test.
- version 0.9908: John Peacock's same-Perl notice for the version::LAX
  regular expression embedded in that test. The expression matches this
  contemporary release; the generated test does not pin the donor version.

No donor code is executed or installed. The four unchanged upstream test
files include the prerequisite audit. Installed smoke checks the public
API of a deterministic fixture.
