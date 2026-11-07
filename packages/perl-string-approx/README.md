<!-- SPDX-License-Identifier: Apache-2.0 -->
# String::Approx 3.28

This directory packages upstream `https://metacpan.org/dist/String-Approx` version `3.28` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

## Source and provenance

The fixed official archive is
`https://cpan.metacpan.org/authors/id/J/JH/JHI/String-Approx-3.28.tar.gz`.
Its 45,093 bytes have SHA-256
`43201e762d8699cb0ac2c0764a5454bdc2306c0771014d6c8fba821480631342`,
matching MetaCPAN and the publisher's CHECKSUMS entry. The historical 2021
CHECKSUMS signature verifies mathematically with `VALIDSIG` but has
`EXPKEYSIG` and uses SHA-1. Its signing subkey is
`33EAEF6DBA3865943BEE9D5BB6A1739063760CCA`, under official PAUSE primary
`2E66557AB97C19C791AF8E20328DA867450F89EC`. This is neither a current strong
signature nor a detached archive signature. The pinned archive SHA-256 is
mandatory; the signed index is explicitly advisory.

Frozen discovery `discovery-20260808T165000Z-9a89920c269462cd` retains Debian
`libstring-approx-perl` 3.28-2 and Fedora `perl-String-Approx` 3.28-32.fc44.
No external distribution recipe was executed. Canonical/module/RPM aliases,
all current open PR titles and current/previous file paths, managed packages
and full official/supplemental provider namespaces were screened for collision.

## License closure

The metadata's `unknown` value is not used as a license grant. The package
selects the LGPL-2.0-only option common to the actual original grants:

- `Approx.pm` POD and `README` explicitly offer LGPL version 2 (or Artistic 2).
- `apse.c` and `apse.h` headers offer LGPL version 2 or later (or Perl Artistic).
- The package-wide `COPYRIGHT` grants LGPL version 1 or later; the bundled
  `LGPL` is version 2, the first published Library GPL. Remaining XS glue,
  typemap, build description and original tests have no different notices.
- The 3.27 `ChangeLog` explicitly records the LGPL 2 / Artistic 2 clarification.

`README.apse` and `README` explicitly state that the implementation shares no
code with agrep and was written from the published algorithm descriptions;
upstream records Udi Manber's concurrence. `COPYRIGHT.agrep` is retained as
upstream's academic acknowledgement, not treated as a license for this code.
No agrep source or other vendored implementation is present. All original
`COPYRIGHT`, `COPYRIGHT.agrep`, `LGPL`, `Artistic` and `README.apse` notices are
installed unchanged. This packaging choice does not rewrite upstream grants.

## Recipe and tests

This is an architecture-specific C/XS module, not a noarch package. The recipe
uses the shipped Makefile.PL, target compiler flags and normal vendor Perl
paths. Target repositories supply GCC, Perl development files, MakeMaker and
Test::More. No source patch or build-time network access is required.

The complete original `%check` is `make test`: seven files and 140 assertions,
including matching, indexing, substitutions, Unicode and empty inputs. No
default test is removed or disabled. All 140 assertions passed using host
Perl/Clang, which is source-level evidence, not a RISC-V RPM build or install.
The installed smoke exercises the loaded XS implementation and version.
Exact-head CI and subsequent physical RPM/SRPM acceptance remain necessary.
