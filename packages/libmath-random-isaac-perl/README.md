# Math::Random::ISAAC for openEuler RVA23

This package pins official CPAN Math-Random-ISAAC 1.004 at SHA-256
`2773f02fbf207e9745e76a037df08bf5a8cc987ed23c57040ce7f7b1561f2b7c`,
matching publisher `J/JA/JAWNSY/CHECKSUMS`. Frozen Ubuntu discovery lists
`libmath-random-isaac-perl` 1.004-2. Official openEuler 24.03-LTS-SP3 riscv64
RVA23 primary metadata lacks `perl-Math-Random-ISAAC` and
`perl(Math::Random::ISAAC)`, while providing MakeMaker, Test::More,
Test::NoWarnings 1.04 and Test::LeakTrace 0.17. It has no optional
`Math::Random::ISAAC::XS` provider; the complete pure-Perl implementation is
installed and used.

The upstream LICENSE attributes copyright 2011 to Jonathan Yu and expressly
allows the MIT/X11 alternative, whose full terms it includes. README and the
two installed modules repeat the author's public-domain intent; bundled tests
and examples have no contrary per-file notice. We select MIT for the RPM and
install LICENSE and README as license files. No upstream source or test is
changed.

`%check` runs the unchanged 11-file upstream default suite. A clean local
source run with a verified temporary Test::NoWarnings 1.04 passed 607
assertions; eight files skipped by upstream conditions: memory leak testing
needs Test::LeakTrace, uniformity is author-only, fallback testing needs the
optional XS backend, and five release tests are release-candidate-only. The
target SPEC includes the official Test::LeakTrace package to exercise both
original memory assertions; target CI must establish the final counts and
skips. Installed smoke verifies the RPM/module provider, exact version, pure
Perl backend, deterministic seeded output and 32-bit integer bounds. Neither
the local test nor PR CI establishes cryptographic suitability or public
repository publication.
