<!-- SPDX-License-Identifier: Apache-2.0 -->
# perl-lingua-en-numbers-ordinate

Packages the official Lingua::EN::Numbers::Ordinate 1.05 release for openEuler
24.03 LTS SP3, riscv64/RVA23. This pure-Perl module adds English numeric ordinal
suffixes: it does not spell numbers as words or provide multilingual grammar.

## Source and license

- Fixed official archive: <https://cpan.metacpan.org/authors/id/N/NE/NEILB/Lingua-EN-Numbers-Ordinate-1.05.tar.gz>.
- SHA-256: `6a2839f4773991a7d0d059e2222a4b713ad3fae75140ea04831c17aeb83a7025`.
- Discovery lineage: Debian stable `liblingua-en-numbers-ordinate-perl` 1.05-2;
  distribution packaging was not executed.
- Sean Burke explicitly grants the software under Perl 5 terms in LICENSE,
  README and module POD. The complete original GPL and Artistic license texts
  are installed unchanged. The standard Dist::Zilla 6.012 MakeMaker output
  retains its generator provenance; no bundled installer library or generated
  auxiliary ReportPrereqs template is present.
- The available PAUSE CHECKSUMS index signature was verified against the
  officially published PAUSE primary fingerprint. This is checksum-index
  advisory evidence, not a detached archive signature; source SHA-256 remains
  mandatory. Historical expired certificate subkeys do not change the verified
  current signing-subkey status.

## Build and verification

The SPEC invokes the original Makefile.PL and the complete default `make test`.
Both original test files are preserved: 49 assertions, including the upstream
environment-diagnostic test. Host-language verification observed all 49 pass
without skips and all 11 original archive files unchanged. Host verification
is not target-RPM or native RISC-V evidence.

BuildRequires are supplied by the fixed target repositories; Test::More is
provided by perl-Test-Simple. No dependency installer or source patch is used.
The recipe requires no network access, but does not claim that CI physically
isolates the target container network.

The installed smoke checks the actual RPM, module version, ordinal/alias
results, suffix exceptions and undefined/empty inputs. Original behavior for
non-numeric input remains as documented upstream. CI must independently build
the RPM/SRPM, run the original tests, install the RPM and execute this smoke
on the locked target. No successful target build, merge or release is claimed
by this recipe alone.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
