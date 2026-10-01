# Data::BitMask 1.00

Official source: `https://cpan.metacpan.org/authors/id/T/TE/TEVERETT/Data-BitMask-1.00.tar.gz`.
The publisher `CHECKSUMS` records SHA-256
`11a5775ca7d7ef2452e2a6a96a4d91f92e31131ea47c24d0d99975e8aed584ae`,
matching the downloaded archive. Its root contains ordinary files and no patches.

The frozen inventory's `license-blocked` and `unverified-upstream` decisions
reflect incomplete discovery metadata, not an upstream prohibition. The
official archive's README and module carry Toby Ovod-Everett's explicit
redistribution/modification grant under the same terms as Perl itself; its
first-party Build.PL declares `perl` licensing. No conflicting per-file grant
was found. This package records those dual terms as
`GPL-1.0-or-later OR Artistic-1.0-Perl`.

The official openEuler 24.03-LTS-SP3 riscv64 RVA23 primary has neither
`perl-Data-BitMask` nor `perl(Data::BitMask)`. It uniquely provides
`perl(Module::Build) = 0.4234` (minimum 0.42), `perl(Test)`,
`perl(Data::Dumper)` and `perl(Carp)`. Those hard build dependencies are
declared in the SPEC; target DNF must confirm their closure.

The sole default upstream test file is unchanged and plans 137 assertions.
It passed locally on macOS (`Files=1, Tests=137`, no skips). That is not a
target-build claim: exact-head hosted CI must confirm all 137 under the
locked SP3 RVA23 image, RPM/SRPM integrity, and installed functional smoke.
