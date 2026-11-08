<!-- SPDX-License-Identifier: Apache-2.0 -->
# perl-tie-function

This directory packages [Tie::Function 0.02](https://metacpan.org/dist/Tie-Function)
for openEuler 24.03 LTS SP3 on RISC-V/RVA23. Fedora 44 GA source
lineage and the fixed source checksum are retained. The checksum matches
the signed PAUSE index in the author's release directory.

The two author copyright and license lines in the original Function.pm are
copied verbatim to a plain-text license file; the installed module is
unchanged. The upstream README is an unedited template and is not used as
license evidence.

MakeMaker runs the original test.pl unchanged. Installed smoke verifies a
tied hash lookup invokes the function with both arguments.
