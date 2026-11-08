# Math::Bezier for openEuler RVA23

This package pins the official CPAN Math-Bezier 0.01 release at SHA-256
`11a815fc45fdf0efabb1822ab77faad8b9eea162572c5f0940c8ed7d56e6b8b8`,
matching publisher `A/AB/ABW/CHECKSUMS`. Frozen Ubuntu discovery lists
`libmath-bezier-perl` 0.01-4; the Ubuntu original archive MD5
`ba6874d8754e2d64ab9c7d15e0eb56c2` equals the publisher's MD5 for this
release. The official openEuler 24.03-LTS-SP3 riscv64 RVA23 primary metadata
has neither `perl-Math-Bezier` nor `perl(Math::Bezier)`, and contains the Perl
runtime, `perl(strict)`, `perl(vars)`, `perl(constant)`, and the build tools.

Upstream `Bezier.pm` explicitly names Andy Wardley as copyright holder and
grants the same terms as Perl. Debian's source copyright file independently
attributes the complete original distribution to Wardley under Artistic or
GPL-1-or-later; the `Graphics Gems V` citation identifies the published
algorithm, not an included code file. No upstream file contains a conflicting
license notice. The RPM installs the grant-bearing `Bezier.pm` as license
evidence.

`%check` calls the original MakeMaker `make test` target, which executes the
unmodified legacy `test.pl`: 27 planned assertions, 27 passed locally without
skips. The installed smoke checks the RPM/provider, version, midpoint of a
cubic curve, and the default 20-point curve. Only exact-head hosted target CI
can establish target test and installed-smoke results. PR artifacts do not
establish public repository publication.
