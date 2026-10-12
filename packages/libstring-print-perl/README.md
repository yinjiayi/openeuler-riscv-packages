<!-- SPDX-License-Identifier: Apache-2.0 -->
# libstring-print-perl

The frozen inventory's exact `libstring-print-perl` key maps to Ubuntu
source 1.02-1 and official stable CPAN String::Print 1.02. The official
HTTPS archive SHA-256
`3049536486459e38e1d791c07ce022326a91a302beaf01dcdb0e7b703a5da6cc`
matches publisher `CHECKSUMS`. All 33 archive entries are regular files or
directories beneath one root, with no links or traversal paths.

The main module carries an explicit
`Artistic-1.0-Perl OR GPL-1.0-or-later` SPDX notice and grants the same
terms as Perl 5; its POD and archived META confirm Perl 5 licensing. The
RPM records the equivalent repository-standard expression
`GPL-1.0-or-later OR Artistic-1.0-Perl` and installs that module as its
license notice. The archived OODoc configuration is development metadata;
the published CPAN source already contains its generated POD.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata
(compressed SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
has no same-name RPM or `perl(String::Print)` provider. It supplies the
declared target providers for HTML::Entities, Date::Parse,
Unicode::GCString, Encode, Data::Dumper, Scalar::Util and Test::More.
This snapshot check does not guarantee future repository contents.

All 19 unmodified default `t/*.t` files remain in `%check`. The separate
`xt/99pod.t` is a development-only test outside upstream's default
`make test`; it is not claimed as executed. `t/52m_dates.t` contains extra
developer/time-zone-dependent assertions under `MARKOV_DEVEL`; the default
test path is preserved without enabling that private mode. Installed-RPM
smoke checks version, generated Provides and both interpolation interfaces.
No local RPM/QEMU build was run. Target build, default tests and installed
smoke remain unverified until exact-head CI. PR artifacts are not public
repository publication.
