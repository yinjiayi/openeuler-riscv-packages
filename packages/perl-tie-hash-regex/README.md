<!-- SPDX-License-Identifier: Apache-2.0 -->
# perl-tie-hash-regex

Tie::Hash::Regex 2.0.0 adds regular-expression matching to tied Perl hashes.
The stable official CPAN release is used unchanged; no patch is required.

## Source and license

- Official source: <https://cpan.metacpan.org/authors/id/D/DA/DAVECROSS/Tie-Hash-Regex-2.0.0.tar.gz>.
- SHA-256: `9e32ce51de05c6c8f801612d3bb2976f517b14cfbbe6905d5b7f6d00e9a0701d`; 6,105 bytes.
- The physical archive matches the official release metadata and DAVECROSS
  publisher `CHECKSUMS` entry. That index was separately cryptographically
  verified against the officially published PAUSE primary fingerprint
  `2E66557AB97C19C791AF8E20328DA867450F89EC`. It is an index signature, not a
  detached archive signature. CI always requires the fixed archive SHA-256;
  index signature availability is advisory, never an exception to that digest.
- Original README and module notices copyright Magnum Solutions Ltd. and grant
  redistribution under the same terms as Perl: GPL-1.0-or-later OR
  Artistic-1.0-Perl. README is installed as the original license grant; the
  installed module retains its full original copyright and license text.
- The named Module::Build::Compat 0.4231 traditional Makefile.PL generator was
  inspected from its exact official archive (SHA-256
  `7e0f4c692c1740c1ac84ea14d7ea3d8bc798b2fb26c09877229e04f430b2b717`).
  This particular output contains only generic `require`, `use` and
  `WriteMakefile` calls plus serialized package metadata from Build.PL; no
  generator helper implementation is copied. This narrow observation is not a
  general waiver for copyrighted generated code. All original files remain in
  the source archive, including Build.PL and the generated Makefile.PL.

## Target compatibility and discovery

Discovery lineage is the frozen `discovery-20260808T165000Z-9a89920c269462cd`
snapshot's Debian stable `libtie-hash-regex-perl` 1.14-2 record. The current
official stable release is 2.0.0 (MetaCPAN reports version `v2.0.0`); no Debian
recipe was executed or copied.

Complete current managed/open-PR aliases and official/supplemental provider
indexes were checked for RPM, module and installed-path collisions before
admission. This pure-Perl package uses vendorlib and requires no native kernel,
hardware or architecture patch. Attribute::Handlers and Tie::Hash are supplied
by target Perl; the target supplies all declared build/test dependencies.
Test::Pod and Test::Pod::Coverage are explicit BuildRequires so the original
documentation tests can execute rather than acquire packaging-added skips.

## Validation boundary

`%check` runs the unchanged default `make test`: all four original `t/*.t`
files, including the malformed-pattern regression. No tests or features are
removed. Local Perl 5.34 source-level execution passed 26 top-level assertions;
the original pod-coverage test naturally skipped because that optional module
is absent on the host. This does not claim a complete target build or a
zero-skip upstream run. Metadata, source-only verification and the isolated
repository gates are run separately. Actual riscv64 RPM build, full target
tests, installation and installed smoke validation remain CI responsibilities.

The installed smoke checks the version, attribute interface, exact/regex
lookup, malformed patterns, existence and deletion without source-tree paths.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
