# Lingua::EN::Syllable 0.31

This pure-Perl module estimates syllables using English spelling heuristics.
It is not a pronunciation dictionary or a guarantee of exact counts. Upstream
documents inaccuracies for contractions, silent-e compounds, punctuation and
nonalphabetic inputs; no accuracy benchmark is claimed here.

## Provenance and licensing

- Official source: https://cpan.metacpan.org/authors/id/N/NE/NEILB/Lingua-EN-Syllable-0.31.tar.gz
- SHA-256: `17981deb8d484d1c1bdea8bf6a6a541303b190093c06b41b2a9d51765c7704cd`.
- Debian stable lineage: `liblingua-en-syllable-perl` 0.310-2, with the current
  official CPAN stable release independently verified as 0.31.
- Greg Fast's explicit whole-software Perl 5 grant is retained in LICENSE,
  README and module POD: `GPL-1.0-or-later OR Artistic-1.0-Perl`. Complete license
  texts and original source notices remain unmodified.
- There is no vendored helper tree, separately attributed copied C implementation
  or generated auxiliary test suite. The original standard Dist::Zilla 6.017
  MakeMaker output retains its generator provenance and explicit Perl license.
- MetaCPAN and the exact CHECKSUMS filename bind the archive SHA-256. The available
  checksum index has a valid SHA-512 PAUSE signature from subkey
  `4584D789E682F9F53B392F1837D079412CC9032E`, bound to the primary fingerprint
  published by CPAN. This index signature is advisory and is not a detached
  archive signature; the full pinned archive checksum remains mandatory.

## Recipe and evidence boundary

The SPEC uses upstream Makefile.PL, builds without downloading dependencies,
and runs the entire original `make test`. The unchanged default test file passed
31 assertions with no skips on the macOS Perl 5.34.1 host. All original archive
members remained byte-identical. This host result is not target RPM evidence.

The verified target repositories supply MakeMaker, Test::More and all Perl core
dependencies. Canonical package, complete open-PR title/file and exact Perl
provider checks found no duplicate component. No patch is needed. The manifest's
`network_during_build: false` describes recipe requirements, not physical CI
network isolation.

Installed smoke covers representative known heuristic cases. Exact-head target
build, original tests, installation, and physical RPM/SRPM verification remain
required from openEuler 24.03 LTS SP3 riscv64/RVA23 CI. No native-specific or
public-release result is claimed by this recipe.
