<!-- SPDX-License-Identifier: Apache-2.0 -->
# Data::Validate::IP 0.31

The frozen Ubuntu `libdata-validate-ip-perl` 0.31-1 key maps to the official
[Data-Validate-IP 0.31](https://metacpan.org/dist/Data-Validate-IP) CPAN
release. The publisher's author-directory `CHECKSUMS` and an independent
HTTPS download agree on the 43,477-byte archive SHA-256
`734aff86b6f9cad40e1c4da81f28faf18e0802c76a566d95e5613d4318182fc1`.
Ubuntu's original archive MD5 agrees with the same publisher record. The
archive contains regular files and directories under one source tree.

The release `LICENSE` grants Perl 5 terms (GPL version 1 or later, or Artistic
1.0); the installed module POD and `README.md` repeat that grant. The
release-wide license covers the shipped default tests and helper files; no
bundled file states conflicting redistribution terms.

The official openEuler 24.03 LTS SP3 riscv64/RVA23 primary has neither a
`perl-Data-Validate-IP` RPM nor a `perl(Data::Validate::IP)` provider. It
uniquely supplies NetAddr::IP 4.079, Socket, Scalar::Util, Exporter,
Test::More, Test::Requires, Test::Taint, and MakeMaker. All four default
upstream test files remain unchanged. Local `make test` passes three files and
4,171 assertions; `t/Untaint.t` skips solely because this Mac lacks
Test::Taint. The SPEC hard-requires target `perl(Test::Taint)` so exact-head
target CI must prove all four files run without skips, plus RPM build, DNF
installation, installed fast/fallback function smoke, and physical products.
PR CI does not establish public RPM publication.
