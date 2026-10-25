# Net::LDAP::SID 0.001

`libnet-ldap-sid-perl` packages the official CPAN 0.001 release for
openEuler 24.03 LTS SP3 `riscv64` / RVA23. The frozen inventory key derives
from Ubuntu `resolute/universe` source `libnet-ldap-sid-perl` 0.001-2; that
lineage is not a source or packaging recipe. The official archive's complete
SHA-256 in `sources.yaml` matches the publisher's `KARMAN/CHECKSUMS` entry.

## Rights and scope

The author-controlled `README` and the only shipped module
`lib/Net/LDAP/SID.pm` directly grant Artistic License 2.0. `Makefile.PL`
initially declares `artistic_2`, but conditionally writes broader `perl`
metadata on newer MakeMaker, explaining the inconsistent META label. RPM
metadata conservatively records only `Artistic-2.0`; it does not infer a GPL
grant from that generated metadata. Original tests and build files have no
conflicting separate notice. The archive contains no vendored third-party
code or binary/data fixture.

## Verification

The checksum-bound official SP3 RVA23 primary has no
`perl-Net-LDAP-SID` or `perl(Net::LDAP::SID)` provider and supplies Perl,
Carp, MakeMaker and Test::More. Both unchanged functional test files passed
locally, totaling 19 assertions. The three other unchanged `t/*.t` files
are upstream author/release-only tests that self-skip without
`RELEASE_TESTING`; this is not full author-suite coverage. The installed-RPM
smoke additionally checks text-to-binary-to-text SID round-trip. Exact-head
target CI is still required before claiming that build or smoke passed;
QEMU-user evidence is not native RISC-V validation.
