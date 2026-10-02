<!-- SPDX-License-Identifier: Apache-2.0 -->
# Data::Hexdumper 3.0001

The frozen Ubuntu `libdata-hexdumper-perl` 3.0001-2 inventory key maps to
official stable [Data-Hexdumper 3.0001](https://metacpan.org/dist/Data-Hexdumper).
Publisher CHECKSUMS and the independently downloaded 17,177-byte HTTPS
archive agree on SHA-256
`f9243cbe8affed5045fe4df505726a7a7289471e30c51ac065b3ed6ce0d1a604`.
The archive contains one top-level tree with regular files and directories.

The installed `lib/Data/Hexdumper.pm` POD explicitly grants the GPL version 2
or Artistic License choice from David Cantrell; `GPL2.txt` and `ARTISTIC.txt`
contain the full terms. Upstream's generic `license: other` metadata describes
that choice but is not a different grant. No file-level contradiction was
found.

The official openEuler 24.03 LTS SP3 riscv64/RVA23 primary has no
`perl-Data-Hexdumper` package or `perl(Data::Hexdumper)` provider. It supplies
Perl's core modules, ExtUtils::MakeMaker, Test::More, Test::Pod and
Test::Pod::Coverage.

The unchanged default `t/*.t` suite has five files. Locally on macOS,
four operational/POD files passed 28 assertions; `t/pod-coverage.t` self-skipped
only because local Test::Pod::Coverage is absent. The target SPEC hard-requires
that provider and requires all five files, at least 29 assertions, no skips,
and installation smoke for a representative hexadecimal dump. Exact-head
target CI must also build physical RPM/SRPM products and DNF-install the RPM.
PR CI is not repository publication.
