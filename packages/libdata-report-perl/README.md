<!-- SPDX-License-Identifier: Apache-2.0 -->
# Data::Report 1.001

The frozen Ubuntu `libdata-report-perl` key maps to the official
[Data-Report 1.001](https://metacpan.org/dist/Data-Report) CPAN release. The
publisher's author-directory `CHECKSUMS` and an independent HTTPS download
agree on SHA-256 `d50c89dbd0eaebbaba31c0ede60356607ed56d5f7060d303550bfc2a72cc944d`.
The archive has one top-level tree containing ordinary files and directories,
without traversal paths. Its distribution `README` and principal module POD
grant redistribution under Perl's GPL/Artistic terms. The bundled Base and
three plugins share the same copyright holder and show no conflicting grant.

The official openEuler 24.03 LTS SP3 riscv64/RVA23 primary has neither a
`perl-Data-Report` RPM nor any of the five installed module providers. It
uniquely supplies all upstream hard dependencies, including `perl(Text::CSV)`
2.04, `perl(Test::More)` 1.302198 and MakeMaker 7.70. All 23 default upstream
test files remain unchanged. Local macOS Perl lacks Text::CSV, so local
upstream tests were not run; this is not a test-success claim. Exact-head
target CI must prove all 23 files run without skips, then the RPM build,
installed functional smoke and physical products. PR CI products do not
establish public RPM publication.
