# Math::Quaternion for openEuler RVA23

This package pins official CPAN Math-Quaternion 0.07 at SHA-256
`de5b0c411c7bd03578090cf10f8b4c1783348beebd00b22a04fceb7402258ef8`,
matching publisher `J/JC/JCHIN/CHECKSUMS`. Frozen Ubuntu discovery lists
`libmath-quaternion-perl` 0.07-3. Official openEuler 24.03-LTS-SP3 riscv64
RVA23 primary metadata has neither `perl-Math-Quaternion` nor
`perl(Math::Quaternion)` and supplies Math::Trig, Carp, Test::More and
MakeMaker providers.

The upstream README and module POD explicitly grant the same terms as Perl.
The module credits named contributors for patches; no file in the archive
asserts a conflicting license. The archive contains one module, two test
files, Makefile.PL, Changes, MANIFEST, README and metadata; the distribution
grant covers its tests as well as its installed module. The RPM installs
the module and man page, not the tests.

`%check` runs both unchanged upstream `t/*.t` files with 108 assertions.
Local source `make test` passed all 108 with zero skips; target CI must
establish the RVA23 result. Installed smoke checks the RPM/module provider,
version and multiplication by the identity quaternion. PR CI artifacts
do not establish public repository publication.
