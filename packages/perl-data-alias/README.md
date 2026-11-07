<!-- SPDX-License-Identifier: Apache-2.0 -->
# perl-data-alias

Packages the official Data::Alias 1.30 source for openEuler 24.03 LTS SP3,
riscv64/RVA23. This is an architecture-specific XS extension, not a noarch RPM.

## Provenance and license

- Source: `https://cpan.metacpan.org/authors/id/X/XM/XMATH/Data-Alias-1.30.tar.gz`.
- SHA-256: `dfa9e341b086cd957df6675879a9cb120919408b85b48966dd240ab85333ed2e`.
- Debian stable trixie `libdata-alias-perl` 1.28-1 establishes distribution
  lineage; official stable CPAN 1.30 is the selected newer release. No distro
  recipe was executed, and no discovery catalog entry was fabricated.
- `README` and `lib/Data/Alias.pm` explicitly grant redistribution under the
  same terms as Perl itself, naming Matthijs van Duin and Andrew Main (Zefram).
  `Alias.xs` separately covers its authors and incorporated Perl portions
  credited to Larry Wall and others under the same GPL/Artistic terms. These
  notices are retained and README/Alias.xs are installed as license material.
- The test-only bundled `Test::Simple` and `Test::More` name Michael G Schwern
  (2001); `Test::Builder` names chromatic and Michael G Schwern (2002). Each
  file explicitly grants the same terms as Perl itself. All remain unmodified
  in the source/SRPM; no third-party installer is bundled. The combined declared
  license is `GPL-1.0-or-later OR Artistic-1.0-Perl`.
- The archive SHA-256 agrees with official release metadata and its exact-name
  `CHECKSUMS` entry. The March 2026 SHA-512 PAUSE index signature mathematically
  verifies under official primary `2E66557AB97C19C791AF8E20328DA867450F89EC`,
  but its signing subkey is now expired. This is recorded as an advisory signed
  index, not a current valid detached archive signature. Archive SHA-256 is
  mandatory; no required signature policy has been relaxed.

## Build and validation

Use ordinary MakeMaker, target GCC and target perl-devel, with distro optimization
flags. The recipe does not require network access; this does not assert that the
CI container is network-isolated. The required compiler, Perl build/test modules,
runtime Carp/Exporter and packaging generators are supplied by the target
repositories. Normalized managed/open-PR identities, actual Perl Provides and
`Data/Alias.pm`/`auto/Data/Alias/` paths were screened. Unrelated Python/Go
identifiers containing the words data and alias are not Perl namespace providers.

`%check` runs the entire original `make test` with no file filters, removed tests
or modified skip conditions. On macOS arm64 / Perl 5.34.1 / Apple Clang 21, the
unchanged host suite reports 33 files and 637 harness tests, with the original
optional Devel::CallParser and Test::Pod::Coverage file skips. Legacy pseudo-hash
checks also retain upstream's unsupported-Perl condition; the reported harness
count must not be described as 637 non-skipped assertions. The host compiler
emitted macro-expansion warnings but exited successfully; warnings were not
silenced. This is host XS evidence only, not target compatibility or an RPM build.

The installed smoke checks the actual XS load/version, scalar and array aliases,
and independent copies. No patch is introduced. Because this module integrates
with Perl parser internals, target Perl 5.38 and riscv64 support remain unverified
until approved CI runs the real build, original suite, RPM install and smoke.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
