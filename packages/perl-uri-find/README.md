# URI::Find for openEuler RISC-V

This package carries the official CPAN `URI-Find` 20160806 source for openEuler
24.03 LTS SP3 `riscv64` RVA23. It provides `perl(URI::Find)` and the `urifind`
utility. The frozen inventory calls out both `perl-URI-Find` (release page) and
`perl-uri-find` (module page); these are aliases for this one distribution, not
two independent packages. The Debian `liburi-find-perl` source is lineage only;
the shipped bytes come directly from the CPAN author directory.

The pinned tarball is
`https://cpan.metacpan.org/authors/id/M/MS/MSCHWERN/URI-Find-20160806.tar.gz`.
Its SHA-256 is
`e213a425a51b5f55324211f37909d78749d0bacdea259ba51a9855d0d19663d6`,
matching the publisher `CHECKSUMS` in the same directory. The archive contains
only ordinary files and directories under one root. Its `LICENSE` grants the
same terms as Perl: GPL-1.0-or-later or Artistic-1.0-Perl.

The checksum-bound official openEuler SP3 RVA23 `everything` primary metadata
(`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
has `perl-Module-Build` and `perl-URI`, but no `perl-URI-Find` RPM or
`perl(URI::Find)` provider. `%check` preserves all eight recursive upstream
default tests. The installed smoke checks module discovery and the CLI without
network use. Exact-head CI must establish the target build, complete test
results, installed smoke, and physical PR products; PR artifacts are not public
RPM/SRPM repository URLs. This module is a candidate dependency for a later
`Test::Pod::No404s` package, not proof that dependent tests already pass.
