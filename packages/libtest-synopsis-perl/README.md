<!-- SPDX-License-Identifier: Apache-2.0 -->
# perl-test-synopsis

This directory packages upstream `https://metacpan.org/dist/Test-Synopsis` version `0.18` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The upstream LICENSE offers Artistic-1.0-Perl or GPL-1.0-or-later. The fixed
source SHA-256 agrees with official MetaCPAN release metadata and the CPAN
publisher CHECKSUMS. The archive uses a generated ExtUtils::MakeMaker entry
point and does not vendor a dependency loader. No patch is applied.

`%check` runs the upstream default `t/*.t` suite unchanged (15 files, 19 TAP
assertions in host preflight). One assertion in `t/10-in-pod-skip.t`
intentionally exercises the module's support for SKIP in example code;
no test file is excluded. The separate installed smoke test checks that the
module compiles a Perl example in a POD SYNOPSIS section.
