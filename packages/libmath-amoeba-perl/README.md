# Math::Amoeba for openEuler RVA23

This package pins official CPAN Math-Amoeba 0.05 at SHA-256
`b862cfd4dc6cb584cc2c84ed47661d8e4777ad6b6032d97d9b395ca5abb6ef15`,
matching publisher `T/TO/TOM/CHECKSUMS`. Frozen Ubuntu discovery lists
`libmath-amoeba-perl` 0.05-3. Official openEuler 24.03-LTS-SP3 riscv64 RVA23
primary metadata has neither `perl-Math-Amoeba` nor `perl(Math::Amoeba)` and
supplies the Perl, MakeMaker, Test::More, Test::Pod and Test::Pod::Coverage
providers used here.

The upstream README and module POD explicitly grant the same terms as Perl;
the module calls this `PERL`. The archive contains one module, three tests,
one example, Makefile.PL, Changes, MANIFEST, README and META.yml; none has a
conflicting file-specific license notice. The distribution-wide README grant
applies to the test and example files as well as the installed module. The RPM
installs the module and its man page, not the example or tests.

`%check` runs all three unchanged original `t/*.t` files, including optional
POD and POD-coverage tests, with target BuildRequires enabling both. Local
source `make test` passed 12 assertions across three files but explicitly
skipped POD coverage because the module was absent on macOS; target CI must
show that it ran. The numerical upstream test starts from random guesses;
installed smoke uses a deterministic two-dimensional fixture to check the
module provider, version, convergence cost and optimum point. PR CI artifacts
do not establish public repository publication.
