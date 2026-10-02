# Hash::WithDefaults for openEuler RVA23

This package pins official CPAN Hash-WithDefaults 0.05 at SHA-256
`6e1df2778355c1a5ca4a9421ecccfd1d109d2e20fbc5f070562a8736ddfaea97`,
matching publisher `J/JE/JENDA/CHECKSUMS`. Frozen Ubuntu discovery lists
`libhash-withdefaults-perl` 0.05-4. The upstream distribution does not name a
separate VCS; its official CPAN author directory is the release source.
Official openEuler 24.03-LTS-SP3 riscv64 RVA23 primary metadata has neither
`perl-Hash-WithDefaults` nor `perl(Hash::WithDefaults)` and supplies the
MakeMaker, Test::More, Test::Pod, Test::Pod::Coverage and Pod::Coverage
providers needed for the unchanged default test suite.

The upstream README and sole module POD attribute copyright 2002-2009 to
Jan (Jenda) Krynicky and expressly grant the same terms as Perl. The RPM uses
the repository's Perl-terms SPDX expression and installs that README as its
license notice; other bundled source and tests carry no conflicting notice.
No upstream source or test is changed.

`%check` runs all five original t files. Clean local `make test` with official
checksum-verified temporary POD test dependencies passed 685 assertions,
including POD syntax and coverage, with zero skips. Target CI must establish
its own exact result. Installed smoke checks the RPM/module provider and
version, case-insensitive lookup, mutable inherited defaults and deletion
semantics. PR CI does not establish public repository publication.
