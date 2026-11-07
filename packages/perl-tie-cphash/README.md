<!-- SPDX-License-Identifier: Apache-2.0 -->
# Tie::CPHash 2.000

Case-insensitive Perl hashes preserving the most recent spelling of each key.
The unchanged [official source](https://cpan.metacpan.org/authors/id/C/CJ/CJM/Tie-CPHash-2.000.tar.gz)
is 15,828 bytes, SHA-256
`001eef7574f2c4057a193e95889903d5aedd412baea142003fa78707df6defdc`.
It matches the publisher's exact CHECKSUMS archive entry. The historical index
has a mathematically valid SHA-1 signature with an expired signing subkey,
anchored to official PAUSE primary
`2E66557AB97C19C791AF8E20328DA867450F89EC`. This is advisory historical metadata,
not a current strong or detached archive signature; source SHA-256 is mandatory.

## License and generated-file provenance

Original LICENSE, README, module and test headers grant Christopher J. Madsen's
distribution under Perl terms; the full original LICENSE is installed.
Generated files were reviewed separately rather than inferred from META.json:

- `t/00-all_prereqs.t` matches the fixed PrereqsFromMeta template in
  Dist-Zilla-Plugins-CJM 4.23 (SHA-256
  `77f7548b60197d1b8146b5acdcb63fc5e8835b7694ada46f10c5d91e957a65a3`).
  This is the same author's explicitly Perl-licensed source.
- `Makefile.PL` and the two short `xt/release` POD wrappers match the concrete
  templates in Dist-Zilla 5.029 (SHA-256
  `58d62f6608bdabe90a82f5f12a1678465f40af0c7ec3cc2cac1c95a12bf8b552`).
  Its original license offers the Artistic terms, whose clause 6 addresses
  scripts and library files generated as output and assigns them to their
  generator user. These specific verified outputs are distributed under CJM's
  original grant; this is not a blanket rule about copied or generated code.

The auxiliary releases were checked against their exact official MetaCPAN
archive hashes; no generator code is built, installed or added to the SRPM.
All original source notices and generated-file provenance comments remain
unchanged. There is no downstream source patch.

## Target dependencies and tests

Discovery snapshot `discovery-20260808T165000Z-9a89920c269462cd` retains Debian
stable and Arch lineage. Official source/license review resolves the discovery
snapshot's unresolved metadata; distro recipes were not executed. Normalized
module/RPM names and paths are checked against all open PRs, managed packages
and complete target official/supplemental provider indexes.

The locked openEuler target supplies make, Perl, perl-devel,
ExtUtils::MakeMaker, Test::Harness, Test::More (perl-Test-Simple), Carp and
perl-generators. This pure-Perl package uses vendorlib and builds a noarch RPM.

The original default `make test` target selects all three `t/*.t` files; it is
retained without overrides or skips. All 42 assertions pass on host Perl 5.34,
and all 13 original archive files remain hash-identical. The two original
`xt/release` checks remain untouched author-release tests, not default tests.
The installed smoke tests case-insensitive lookup, spelling preservation,
replacement, uniqueness and deletion.

Host tests and source-only verification are not openEuler/RISC-V RPM build,
installation or native-hardware evidence. Approved CI must provide actual
build/default-test/install/smoke and RPM/SRPM evidence before acceptance.
No local RPM/QEMU build or upstream writes were performed. Auto-merge is off;
`patches/series` is intentionally empty. Apache-2.0 covers original packaging
material only; upstream source retains its original licensing.
