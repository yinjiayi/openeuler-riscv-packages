<!-- SPDX-License-Identifier: Apache-2.0 -->
# Data::Faker 0.10

The frozen Ubuntu `libdata-faker-perl` key maps to the official
[Data-Faker 0.10](https://metacpan.org/dist/Data-Faker) CPAN release. The
publisher's author-directory `CHECKSUMS` and an independent HTTPS download
agree on SHA-256 `caa5d56e05145ca093735adaaf5fe7389974c4334e44b68aec7a78c089c7443f`.
The archive contains one ordinary-file source tree and no traversal paths.
The release README and all seven installed module PODs explicitly grant
redistribution on Perl's GPL/Artistic terms. The bundled `datafaker` CLI is
by the same named author and is within the distribution-level grant.

The official openEuler 24.03 LTS SP3 riscv64/RVA23 primary has neither a
`perl-Data-Faker` RPM nor a `perl(Data::Faker)` provider. Its POSIX,
Getopt::Long, File::Spec, Carp, base, Test::More, and MakeMaker providers
are unique. All eight default upstream test files remain unchanged: local
`make test` passes 27 assertions without skips. A separate local CLI probe
using relative `-Iblib/lib` failed because this legacy module requires a
relative path rejected by modern Perl; the same CLI succeeds with an absolute
`PERL5LIB` path, as an installed vendor path will be. Target exact-head CI
must still prove the full default tests, RPM build, installed module/CLI
smoke, and physical products. PR artifacts are not public RPM publication.
