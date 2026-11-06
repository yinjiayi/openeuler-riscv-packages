# Algorithm::IncludeExclude 0.01

Official source: `https://cpan.metacpan.org/authors/id/J/JR/JROCKWAY/Algorithm-IncludeExclude-0.01.tar.gz`.
The publisher `CHECKSUMS` in that directory records SHA-256
`e4ad04dc22049d29a119160e067c9b5e91765624c8f189a312cff1b87414a20d`.
The archive has one safe root, only regular files/directories and no patches.

The official README and module POD explicitly identify Jonathan Rockway and
grant redistribution under the same terms as Perl. The RPM maps this to
`GPL-1.0-or-later OR Artistic-1.0-Perl` and installs the README as its
license notice. The checksum-verified archive bundles `inc/Module/Install`;
configure-scoped `PERL5LIB=.` selects those exact helper bytes on modern Perl.

The official SP3 RVA23 primary has no `perl-Algorithm-IncludeExclude` name or
`perl(Algorithm::IncludeExclude)` provider. It uniquely supplies the declared
Carp, Test::More, Test::Exception, Test::Pod and Test::Pod::Coverage modules,
including the latter's Pod::Coverage, Pod::Parser, Pod::Find and Devel::Symdump
provider closure. The SPEC hard BuildRequires both POD test modules, so the
unmodified default 13-file suite must run fully on target.

Locally, all 70 executed assertions pass, but `t/pod-coverage.t` skips because
the macOS Perl 5.34.1 lacks optional `Test::Pod::Coverage`. This local pass is
partial test evidence, not proof of full target quality. Exact-head hosted
openEuler CI must show every default test file running without that skip,
followed by installed smoke, before this PR can be considered successful.

The frozen 151,852-row inventory records Fedora `0.01-47.fc44` lineage; that
row is not source, licensing, dependency or target-build proof.
