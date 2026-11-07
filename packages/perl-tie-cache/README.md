<!-- SPDX-License-Identifier: Apache-2.0 -->
# perl-tie-cache

This directory packages the official stable Tie::Cache 0.21 release for
openEuler 24.03 LTS SP3, riscv64/RVA23. The RPM is noarch; its build, original
tests, installation and smoke checks still require target CI verification.

## Source, lineage and license

- Official archive: `https://cpan.metacpan.org/authors/id/C/CH/CHAMAS/Tie-Cache-0.21.tar.gz`.
- SHA-256: `d7eaa22f35a21b226f2bfd17782cd4226a584a2364659cd7bf8b24fe37f6fe89`.
- Debian stable trixie lineage: `libtie-cache-perl` 0.21-3; the distribution
  recipe was not executed or substituted for the upstream source.
- `Cache.pm` and `README` name Joshua Chamas, Chamas Enterprises Inc., copyright
  1999-2012, and explicitly grant the same terms as Perl itself. This is the
  basis for `GPL-1.0-or-later OR Artistic-1.0-Perl`; the generated META.yml's
  `unknown` field is not the license authority. There is no bundled installer
  or third-party generated build helper. The explicit grant and notices ship
  in `%license Cache.pm`.
- The exact-name SHA-256 in the official author's `CHECKSUMS` agrees with the
  downloaded bytes. Its historical 2021 SHA-1 signature mathematically verifies
  under PAUSE primary `2E66557AB97C19C791AF8E20328DA867450F89EC`, anchored by the
  official CPAN PAUSE information page, but GnuPG reports the signing subkey
  expired. It is an advisory signed index, not a current strong detached
  archive signature. The archive SHA-256 remains mandatory.

## Build and tests

The ExtUtils::MakeMaker build does not require network access and does not
install CPAN dependencies automatically. This is a recipe requirement, not
an assertion that the CI container is network-isolated. The target provides
make, perl, ExtUtils::MakeMaker and perl-generators; Benchmark and the other
core Perl modules used by the default driver are in the target perl package.
Current managed packages, all
open PR names/files and official/supplemental provider names/files were checked
for the canonical ID, RPM name and `Tie/Cache.pm` namespace before submission.

`%check` executes the complete original `make test`, with the original test.pl
unchanged. That custom driver performs 11 reachable functional checks and 13
fixed-iteration timing diagnostics. No performance threshold is asserted, and
these timings are not native RISC-V or performance evidence. Upstream's existing
`exit` leaves five later subclass example checks unreachable; it is preserved,
and those examples are not claimed as executed tests. The separate optional
`tie-cache-bench.pl` comparison requires Tie::Cache::LRU and is not a default
test: its accidental vendorlib installation is removed, and it is retained as
non-executable documentation, not run as an acceptance benchmark.

The original test helper only prints `ERROR` on a false result. In addition to
propagating the original make exit status, the recipe rejects such error output
and requires exactly 11 `OK ...` lines. This strengthens result checking without
replacing or filtering tests. Positive actual output plus error, missing-check,
extra-check and nonzero-make negative fixtures validate that guard. Host Perl
5.34.1 executes all 11 checks without errors; this is source-level evidence,
not a target RPM result. The installed smoke checks version, read/write,
read-refresh eviction, deletion, reference values and clearing.

No source patch is needed. The implementation is architecture-independent Perl;
target build/install evidence remains unknown until CI finishes. No native
timing or hardware validation claim is made.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
