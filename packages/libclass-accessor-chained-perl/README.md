# Class::Accessor::Chained 0.01

This package preserves the original ordinary and Fast accessor modules. A
chained setter returns the same object; a getter returns its field value.
Read/write, write-only and read-only interface behavior is checked separately.
These are functional checks, not performance, security or native-RISC-V claims.

## Discovery and source identity

The frozen inventory keys are `libclass-accessor-chained-perl` and
`perl-Class-Accessor-Chained`. Ubuntu's `0.01.1~debian-5` and cross-distribution
version strings are lineage, not the version of the selected upstream archive.
Authorized CPAN publisher RCLAMP's official stable release is **0.01**:

- Source: <https://cpan.metacpan.org/authors/id/R/RC/RCLAMP/Class-Accessor-Chained-0.01.tar.gz>
- Size: 2,322 bytes.
- SHA-256: `a5bf49d3804f83ad25a1b16f327d14d4cbee2270132104b28705031dbccc34d2`.
- Official release API: <https://fastapi.metacpan.org/v1/release/Class-Accessor-Chained>.
- Publisher checksum index: <https://cpan.metacpan.org/authors/id/R/RC/RCLAMP/CHECKSUMS>.

API and author HTTPS CHECKSUMS agree with the physically hashed archive. The
CHECKSUMS document carries a PGP envelope, but its signature was not verified;
this package does not claim signed-source verification. All 16 ordinary archive
members, including ten regular files and original read-only modes, were reviewed.
No original source, fixture, helper or test is patched, stripped or repacked.

## Rights and notices

Both modules and original README explicitly preserve Richard Clamp's 2003
copyright and permission under the same terms as Perl itself. The package uses
`GPL-1.0-or-later OR Artistic-1.0-Perl` accounting and installs those original
notices plus Changes unchanged. Because the archive contains no complete license
texts, three byte-exact notice supplements come from official Perl 5.8.7 at
immutable commit `3eef4faaf8d7fa185749184afd7dc737b8039f42`: README (the original
copyright/grant/disclaimer), Artistic and Copying. They preserve the complete
terms, not a software dependency, a claimed code ancestor or a relicense.

The source describes its Fast interface as analogous to Class::Accessor::Fast.
The reviewed official target Class::Accessor 0.51 modules credit original author
Michael G Schwern and copyright 2017 Marty Pauley, explicitly granting Perl terms.
That target dependency is not evidence of the exact historical implementation
copied in 2003, and its later copyright date is not attributed to Chained. Original
Chained copyright/grants and both full Perl alternatives remain intact; no legal
certainty or reconstructed historical ownership is claimed.

## Target and version boundary

At the reviewed main commit, package paths and RPM/module aliases were absent.
Checksum-bound official SP3 RVA23 primary metadata has no Chained or Chained::Fast
RPM/module provider and supplies all declared runtime and default-test tools.
The actual target parent Class::Accessor and Class::Accessor::Fast are 0.51.
The proposed package is `noarch` for openEuler 24.03 LTS SP3 `riscv64`/RVA23 under
the fixed image digest, with network-enabled dependency/source retrieval.

Only Chained.pm declares its own `VERSION = '0.01'`. Fast.pm has no own version;
Perl method-based VERSION lookup may inherit the parent's 0.51. Neither that
inherited version nor an invented 0.01 is Fast's own release declaration. The
installed gate requires the main capability at 0.01 and Fast's unversioned
capability, and checks both exact installed module hashes.

## Complete tests and acceptance

The generated traditional Makefile.PL is retained. Original `make test` runs
`t/00compile.t` (two require assertions) and `t/chained.t` (six assertions checking
ordinary and Fast chaining, identity and getters): two files/eight assertions,
with no upstream skip branch. A mandatory additional Harness statistics gate
requires those same two files/eight passing assertions, zero failures, skips,
TODO or bonus assertions. No upstream tests are replaced or reduced.

Installed smoke additionally exercises both classes' scalar/multi-value setters,
chain identity, read/write and write-only/read-only behavior, rejection of invalid
access, unchanged read-only state and byte-exact original modules/seven notice
files. Errors are checked as genuine exceptions without inventing diagnostic text.

Preparation and static review do not establish target CI success. Acceptance
still requires exact-head disposable-hosted CI, source/RPM/SRPM physical and
schema audits, and installed smoke. No local upstream build/test, RPM/QEMU run,
main merge, trusted dispatch, native acceptance or public RPM/SRPM is claimed.
