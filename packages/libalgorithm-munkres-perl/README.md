# Algorithm::Munkres 0.08

Official source: `https://cpan.metacpan.org/authors/id/T/TP/TPEDERSE/Algorithm-Munkres-0.08.tar.gz`.
The publisher `CHECKSUMS` in the same CPAN directory records SHA-256
`196bcda3984b179cedd847a7c16666b4f9741c07f611a65490d9e7f4b7a55626`.
The archive has one safe root and only regular files/directories.

The official source README and module POD identify the copyright holders and
expressly grant GPL version 2 or later. Legacy CPAN `META.yml` has a null
license. The frozen AUR row says `GPL AND PerlArtistic`, which conflicts with
the official source; it is used only as stale lineage, not license authority.
The SPEC therefore uses `GPL-2.0-or-later` without inventing an Artistic grant.

The unmodified default `make test` passes all 13 files and 130 assertions
locally. `%check` runs that same suite. The verified official SP3 RVA23 primary
metadata has no same-name RPM or `perl(Algorithm::Munkres)` provider. It has
unique MakeMaker 7.70 and Test::More 1.302198 providers, with no other
non-core requirements in the source.
