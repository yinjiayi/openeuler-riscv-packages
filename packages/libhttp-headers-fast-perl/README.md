# HTTP::Headers::Fast 0.22

This directory maps the frozen Ubuntu `libhttp-headers-fast-perl` 0.22-3
lineage to official CPAN HTTP-Headers-Fast-0.22. The 19,730-byte HTTPS
archive SHA-256
`cc431db68496dd884db4bc0c0b7112c1f4a4f1dc68c4f5a3caa757a1e7481b48`
matches the publisher's `CHECKSUMS`. Archive entries are regular text files
and directories, without symlinks or path traversal.

The distribution `LICENSE` explicitly grants redistribution under Perl 5's
GPL version 1-or-later or Artistic License 1.0 terms; README and module POD
agree, and release metadata says `perl_5`. Text-only tests and auxiliary
benchmark scripts have no conflicting notices. The benchmark scripts are not
run or packaged as executables.

The checksum-bound official openEuler 24.03 LTS SP3 `riscv64` RVA23 primary
metadata has no `perl-HTTP-Headers-Fast` RPM or
`perl(HTTP::Headers::Fast)` provider. It supplies Module::Build::Tiny,
HTTP::Date, HTTP::Headers, URI and Test::Requires for all eight unchanged
default tests, plus Carp, MIME::Base64 and Storable for lazy runtime paths.
The local source run passed 8 files and 195 assertions without skips.

Installed-RPM smoke checks header access, PSGI flattening, date conversion,
basic authorization and cloning. These are functional checks only. No claim
about speed, native RISC-V performance, or public RPM publication follows
from hosted QEMU-user CI.
