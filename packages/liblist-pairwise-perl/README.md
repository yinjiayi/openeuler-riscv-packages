# List::Pairwise 1.03

Official source: `https://cpan.metacpan.org/authors/id/T/TD/TDRUGEON/List-Pairwise-1.03.tar.gz`.
Publisher `CHECKSUMS` in the same CPAN directory records SHA-256
`96d716f2b2832cf42875e3a4f81752a025be94c3114a382887dc2eb4515a302e`.
The archive contains a single safe root and only regular files/directories.
Its embedded POD grants the same license terms as Perl 5; CPAN metadata says
`perl_5`. The frozen AUR record is stale and establishes lineage only, not
source authority.

The complete default upstream `make test` runs `t/*.t`: locally 12 files and
183 assertions passed. `t/warn3.t` skips by upstream design on Perl >= 5.19.006;
the target Perl is 5.38.0. `t/coverage.pl` is a development coverage driver,
not part of the default `make test` suite. The SPEC does not modify test files
or suppress failures. It uses the SHA-verified bundled `inc/Module/Install`
for configuration by adding only `.` to `PERL5LIB` for `Makefile.PL`.

The verified official SP3 RVA23 primary metadata has no
`perl(List::Pairwise)` provider or same-name RPM. Build-time providers include
`perl-ExtUtils-MakeMaker` 7.70 and `perl-Test-Simple` 1.302198.
