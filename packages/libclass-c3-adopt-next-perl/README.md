<!-- SPDX-License-Identifier: Apache-2.0 -->
# Class::C3::Adopt::NEXT 0.14

Frozen `libclass-c3-adopt-next-perl`/`perl-Class-C3-Adopt-NEXT` inventory
lineage includes Debian 0.14-2, Fedora 0.14-31.fc44 and openSUSE 0.14. The
official stable CPAN archive is 29,971 bytes; SHA-256
`85676225aadb76e8666a6abe2e0659d40eb4581ad6385b170eea4e1d6bf34bf7`
matches publisher ETHER `CHECKSUMS`.

Top-level `LICENSE` grants same-as-Perl redistribution for this software.
Installed `lib/Class/C3/Adopt/NEXT.pm` and README repeat that grant. All
default tests, fixtures and generated build files have no conflicting notice
or vendored code. The RPM expression records the GPL-1-or-later or Artistic-1
choice.

Official openEuler 24.03 LTS SP3 riscv64/RVA23 primary has no
`perl-Class-C3-Adopt-NEXT` name or `perl(Class::C3::Adopt::NEXT)` provider.
It supplies MRO::Compat 0.15, NEXT 0.69, List::Util 1.63,
Module::Build::Tiny 0.047, Test::Exception 0.43 and the other default test
providers. The unmodified `t/*.t` suite has eight files/26 assertions and
no skips. `PERL5LIB=.` in `%check` lets unchanged `t/00-report-prereqs.t`
load the SHA-verified bundled `t/00-report-prereqs.dd` on Perl versions
without `.` in `@INC`; this restores the original dependency-report branch
without suppressing assertions. Local original tests passed 8/26 with that
path. `xt/` author/release tests remain in the source but are not part of the
default suite. Target CI must prove all eight files/26 assertions, physical
RPM/SRPM products, DNF installation and installed NEXT dispatch smoke. No
local RPM/QEMU build or publication occurred.
