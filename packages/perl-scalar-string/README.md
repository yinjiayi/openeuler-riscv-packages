# Scalar::String 0.003

This module inspects and changes Perl scalar string encoding. The package keeps
the upstream XS implementation and pure-Perl fallback; neither is disabled.

## Provenance and license

- Official source: https://cpan.metacpan.org/authors/id/Z/ZE/ZEFRAM/Scalar-String-0.003.tar.gz
- SHA-256: `f54a17c9b78713b02cc43adfadf60b49467e7634d31317e8b9e9e97c26d68b52`.
- Discovery lineage: Debian stable `libscalar-string-perl` 0.003-2; current official
  MetaCPAN release and exact CPAN CHECKSUMS filename bind these bytes.
- Andrew Main (Zefram) explicitly grants the same terms as Perl in README and
  module POD: `GPL-1.0-or-later OR Artistic-1.0-Perl`. The small XS implementation,
  Build.PL subclass and tests contain no separately attributed bundled helpers.
  Original notices and all source files remain unchanged. No patches are needed.
- The available PAUSE-signed CHECKSUMS index was verified against the primary
  fingerprint published by CPAN. The bundled historical SHA-1 SIGNATURE also
  matched all 15 original member hashes and verified mathematically; its keyserver
  certificate is not independent proof of author identity. These are advisory
  index/member signatures, not detached signatures of the archive. Pinned
  archive SHA-256 verification remains mandatory.

## Build and tests

The recipe uses the original `perl Build.PL`, `./Build`, and complete
`./Build test`. A C compiler and Perl development files are required, and the
recipe checks for the actual XS shared object so a compiler failure cannot
silently deliver only the fallback. Both original grading suites are retained.
All target build dependencies, including Module::Build, ExtUtils::CBuilder,
Test::More and the optional POD test providers, exist in the verified target
repository. Runtime dependencies are Perl core modules; namespace/provider
checks found no existing Scalar::String component.

On the macOS Perl 5.34.1 host the original suite passed 5 test files / 1,059
assertions with the XS module compiled. The two original Test::Pod::Coverage
checks self-skipped because that optional host module was unavailable; their
conditions and files were not changed, and the target recipe supplies it.
Host results are not target, RPM, native-RISC-V, or publication evidence.

`%check` preserves the complete default suite. Installed smoke checks Latin-1
and embedded-NUL round trips and wide-character downgrade rejection. The
recipe needs no build-time network; `network_during_build: false` states this
requirement and does not assert physical network isolation by CI. Actual target
build, original tests, installation and physical RPM/SRPM acceptance remain
required from the exact-head openEuler 24.03 LTS SP3 riscv64/RVA23 CI.
