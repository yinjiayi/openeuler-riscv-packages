<!-- SPDX-License-Identifier: Apache-2.0 -->
# Time::Period 1.25

Frozen Debian `libtime-period-perl` 1.25-3 lineage maps to the official
stable PB OYD CPAN release. The 18,393-byte official HTTPS archive SHA-256
`d07fa580529beac6a9c8274c6bf220b4c3aade685df65c1669d53339bf6ef1e8`
matches the publisher's `CHECKSUMS`.

The top-level `LICENSE` grants redistribution of “This software” under
GPL-1-or-later or Artistic-1.0, and the only installed module and README
repeat same-as-Perl terms. The module credits Patrick Ryan as original
author and Paul Boyd for bug fixes; Paul also published this release.
There is no contrary per-file license notice or vendored code. The
distribution-wide grant is the redistribution basis; it is not a claim
that each contributor signed a separate document.

The SHA-bound official openEuler 24.03 LTS SP3 riscv64/RVA23 primary has
no `perl-Time-Period` name or `perl(Time::Period)` provider. Its core
Exporter and POSIX, ExtUtils::MakeMaker, Test::More and Test::Harness
providers close the build/runtime/default-test dependency set.

The unchanged ten upstream tests use a fixed 2011 date and passed locally
with 213 assertions, zero skips. Target `%check` requires the same scope.
The installed RPM smoke separately checks a matching weekday and year,
a nonmatching weekday and malformed period handling. Exact-head hosted
CI must establish target test, physical RPM/SRPM and DNF smoke results;
no local RPM/QEMU build or publication occurred.
