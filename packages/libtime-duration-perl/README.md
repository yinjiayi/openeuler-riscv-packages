<!-- SPDX-License-Identifier: Apache-2.0 -->
# Time::Duration 1.21

Frozen Ubuntu `resolute/main` `libtime-duration-perl` 1.21-2 lineage maps to
the official stable NEILB CPAN release. The fixed HTTPS source is 16,205 bytes,
SHA-256 `fe340eba8765f9263694674e5dff14833443e19865e5ff427bbd79b7b5f8a9b8`,
matching the publisher's `CHECKSUMS`.

The top-level `LICENSE` and `README` grant same-as-Perl redistribution for
the software. The only installed PM names both Sean M Burke and Avi Finkel
and directly grants same-as-Perl for that program; this matters because the
top-level generated copyright notice names Sean alone. Other archive files
have no contrary notices or vendored code.

The SHA-bound official openEuler 24.03 LTS SP3 riscv64/RVA23 primary has no
`perl-Time-Duration` name or `perl(Time::Duration)` provider. It supplies
`perl(Test)` 1.31, MakeMaker 7.70, Test::Harness 3.48 and all core runtime
modules declared by upstream.

All four default upstream test files remain unchanged. Locally, the two
functional files passed 250 assertions; the two `RELEASE_TESTING`-only POD
files self-skipped as released. Target `%check` requires precisely that
functional count and those two named release-only self-skips, with no
functional assertion skip. Installed smoke separately checks rounded, exact
and relative English output. Target exact-head CI must prove the physical
RPM/SRPM and DNF-installed behavior. No local RPM/QEMU build or publication
occurred.
