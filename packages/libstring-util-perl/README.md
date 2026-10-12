<!-- SPDX-License-Identifier: Apache-2.0 -->
# libstring-util-perl

The frozen inventory's exact `libstring-util-perl` key records Ubuntu
`1.35-1`. This package advances to the official latest stable
[String-Util 1.36](https://metacpan.org/dist/String-Util) CPAN release. Its
official HTTPS archive SHA-256 is
`517b1ab32566fd4d5e8be23d99339ce3bffee2912c5ff29f5dc95870ff4fcb0e`,
identical to the publisher's `CHECKSUMS` entry. All 15 archive entries are
regular files or directories beneath one root, without traversal paths or
links. The bundled LICENSE and module POD expressly grant GPL version 1 or
later or Artistic License. Makefile.PL and META label this release MIT; the
RPM uses the explicit substantive grant in LICENSE and installs that text.

The official openEuler 24.03 LTS SP3 `riscv64`/RVA23 `everything` primary
metadata SHA-256 is
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`.
It contains neither `perl-String-Util` nor a `perl(String::Util)` provider and
includes the declared Perl build/test toolchain. This is a snapshot check,
not a future guarantee.

`%check` retains both default upstream tests (92 assertions passed on local
Perl 5.34.1). The installed-RPM smoke checks the module version and key
string operations. Exact-head target CI must still establish the SP3 RVA23
RPM build, complete suite, and installed smoke; no local RPM/QEMU result is
claimed.
