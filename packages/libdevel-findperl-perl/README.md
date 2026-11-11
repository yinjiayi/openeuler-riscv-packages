<!-- SPDX-License-Identifier: Apache-2.0 -->
# Devel::FindPerl 0.016

Frozen Debian `libdevel-findperl-perl` 0.016-2 lineage maps to the official
stable LEONT CPAN release. The 14,449-byte fixed HTTPS archive SHA-256
`43a2bf2f787a3f1b881179063162b2aa3e7cb044f6e5e76ec6466ae90a861138`
matches the publisher's `CHECKSUMS`.

The top-level `LICENSE` covers “This software” under GPL-1-or-later or
Artistic-1.0 and names both rightsholders, Randy Sims and Leon Timmermans.
The only installed module repeats the same-as-Perl grant; there are no
conflicting notices or vendored files.

The SHA-bound official openEuler 24.03 LTS SP3 riscv64/RVA23 primary has
no `perl-Devel-FindPerl` name or `perl(Devel::FindPerl)` provider. It has
all runtime and default-test providers, including Config, Scalar::Util,
IPC::Open2 and Test::More.

The unchanged default suite contains only two files and two assertions.
Locally both pass with zero skips, including `t/11-tainted.t`; that is a
narrow coverage claim, not broad behavioral validation. Target `%check`
rejects a skip in either file. The installed smoke separately starts Perl
in taint mode, discovers the actual matching interpreter, checks that it
is executable and configuration-equivalent, and rejects a tainted path.
Target exact-head CI must prove physical RPM/SRPM and DNF installed smoke.
No local RPM/QEMU build or publication occurred.
