<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtest-hexdifferences-perl

This directory packages upstream `https://metacpan.org/release/STEFFENW/Test-HexDifferences-1.001` version `1.001` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The signed CPAN publisher digest and MetaCPAN metadata agree on the fixed
archive. The README and both modules grant the Perl terms; the package
installs the full Artistic and GPL license texts. The generated
`Makefile.PL` uses the traditional Module::Build::Compat 0.4218 template.
The exact donor release and its copyright/grant are retained in the
installed notice. The formatter cites Data::Hexdumper as inspiration;
review of the cited formatter found compatible format conventions and a
different parser and implementation, with the original attribution intact.

The original `make test TEST_VERBOSE=1` suite runs unchanged, including
POD and POD coverage when supplied. Release/author guards stay untouched.
The installed smoke checks the main comparison API and actual formatting.
