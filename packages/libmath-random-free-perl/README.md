# Math::Random::Free for openEuler RVA23

This package pins official CPAN Math-Random-Free 0.2.0 at SHA-256
`6dd10b241d08fded923359cf09f028d9ab6a8664f391740e90a7b0836d6548ed`,
matching publisher `M/ME/MERKYS/CHECKSUMS`. Frozen Ubuntu discovery lists
`libmath-random-free-perl` 0.2.0-2. Official openEuler 24.03-LTS-SP3 riscv64
RVA23 primary metadata has neither `perl-Math-Random-Free` nor
`perl(Math::Random::Free)` and supplies Digest::SHA, List::Util, Test::More
and MakeMaker providers.

The upstream README attributes 2021 copyright to Andrius Merkys and grants
BSD-3-Clause. Bundled LICENSE contains the three-clause BSD template with
Regents attribution; both notices are installed as license files. The module
and test carry no conflicting per-file grant. The archive also includes
Makefile.PL, Changes, MANIFEST and metadata. The RPM installs the module and
man page, not the test or build metadata.

`%check` runs the unchanged original `t/01_basic.t` with four assertions.
Local source `make test` passed all four without skips; target CI must
establish the RVA23 result. Installed smoke checks the RPM/module provider,
version, deterministic reseeding, integer bounds and a valid permutation.
This module explicitly does not claim cryptographic security; PR CI artifacts
do not establish public repository publication.
