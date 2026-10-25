# Math::Base36 for openEuler RVA23

This package pins official CPAN Math-Base36 0.14 at SHA-256
`eedcc8cb22b8f6b6c07742e55931f6e9d03771d221d0b76639f18a3b7d19f47f`,
matching publisher `B/BR/BRICAS/CHECKSUMS`. Frozen Ubuntu discovery lists
`libmath-base36-perl` 0.14-3; its original archive MD5
`cb08eb9dcf4f00a5ac7b91863ca602e5` equals the official CPAN archive's
MD5. Official openEuler 24.03-LTS-SP3 riscv64 RVA23 primary metadata has
neither `perl-Math-Base36` nor `perl(Math::Base36)` and supplies the Perl,
Math::BigInt, Test::Exception, POD, and MakeMaker providers required here.

Upstream module POD and README expressly grant the same terms as Perl.
Debian's source copyright separately assigns the original module to Rune
Henssel and Brian Cassidy, and the bundled `inc/Module/*` build helpers to
Adam Kennedy, Audrey Tang, and Brian Ingerson, all under Artistic or GPL-1+
terms. No file has a conflicting notice. The bundled Module::Install helper
is used only to configure the build: a local staged MakeMaker installation
contained the module and its man page, not the `inc/` tree; the RPM file
list likewise excludes `inc/`. Upstream's `Makefile.PL` imports
`inc::Module::Install` from that tree. Perl 5.38 excludes the current
directory from `@INC` by default, so the SPEC adds the source directory to
`PERL5LIB` only for the configuration command while retaining any existing
`PERL5LIB`; the upstream source and test files remain unchanged.

`%check` runs all five unchanged original `t/*.t` files, with target
BuildRequires enabling both optional POD tests. A local source run passed
40 assertions but explicitly skipped POD coverage because that module was
absent; target CI must show whether it ran. Installed smoke checks the
RPM/module provider, version, base-36 round trip, and padding behavior.
PR CI artifacts do not establish public repository publication.
