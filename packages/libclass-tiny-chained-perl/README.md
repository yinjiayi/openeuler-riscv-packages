<!-- SPDX-License-Identifier: Apache-2.0 -->
# libclass-tiny-chained-perl

This packages the fixed Class::Tiny::Chained 0.004 CPAN release for openEuler 24.03 LTS SP3 on riscv64/RVA23. The archive SHA-256 agrees with authorized MetaCPAN metadata and the PAUSE-signed CHECKSUMS entry; Debian stable lineage identifies the same component.

The original Artistic-2.0 terms and Dan Book attribution are retained. The generated MakeMaker front end and original author-only POD tests match Ricardo Signes's Dist-Zilla 6.007 templates. The original default prerequisite test matches David Golden's ReportPrereqs 0.025 template and is separately Apache-2.0; the original contribution guide retains its own Apache attribution. The INSTALL guide matches Marcel Grünauer's InstallGuide 1.200007 template. Complete license files for the three donors are individually pinned and shipped.

The recipe uses the original MakeMaker build, test and staged install targets without network. Both default test files are unchanged; the test harness alone adds the release root so the old generated prerequisite test can resolve its fixed `t/00-report-prereqs.dd` on modern Perl. The existing non-default `xt/author` tests remain outside the default test target. The smoke check verifies the installed chained setter and ordinary getter. No source patch is needed.
