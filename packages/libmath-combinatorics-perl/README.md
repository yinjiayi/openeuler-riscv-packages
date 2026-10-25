# Math::Combinatorics for openEuler RVA23

This package pins official CPAN Math-Combinatorics 0.09 at SHA-256
`6ef15a1003fe4d7f49d54380b5d7995f5950d799e46aad285d758a12e36da647`,
matching publisher `A/AL/ALLENDAY/CHECKSUMS`. Frozen Ubuntu discovery lists
`libmath-combinatorics-perl` 0.09-6. Official openEuler 24.03-LTS-SP3 riscv64
RVA23 primary metadata has neither `perl-Math-Combinatorics` nor
`perl(Math::Combinatorics)` and supplies Data::Dumper, Exporter, Test::More
and MakeMaker providers.

The upstream README and module POD explicitly grant the same terms as Perl.
The archive contains one module, three tests, Makefile.PL, Changes, MANIFEST,
README and META.yml; none has a conflicting file-specific license notice.
The distribution-wide README grant applies to the tests as well as the
installed module. The RPM installs the module and man page, not the tests.

`%check` runs all three unchanged original `t/*.t` files and their 25
assertions without skips. The local source run passed these, while target
CI must establish the RVA23 result. Installed smoke checks the RPM/module
provider, version and a four-element two-at-a-time combination iterator.
PR CI artifacts do not establish public repository publication.
