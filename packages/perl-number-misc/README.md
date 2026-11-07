<!-- SPDX-License-Identifier: Apache-2.0 -->
# Number::Misc 1.2

Pure-Perl utilities for interpreting and formatting numbers, zero padding,
random integers within a range, and even/odd classification.

## Source and license

The stable release is obtained from the author's official CPAN directory:
https://cpan.metacpan.org/authors/id/M/MI/MIKO/Number-Misc-1.2.tar.gz

The 12,322-byte archive has SHA-256
`77b9b68c600a069cf16f4d8126ecb32151e6bcd34b0edb17b78adee689dc91d8`.
The publisher's CHECKSUMS entry matches both its size and SHA-256. Its historical
2021 index signature has a mathematically valid SHA-1 signature from signing
subkey `33EAEF6DBA3865943BEE9D5BB6A1739063760CCA`, bound to official PAUSE primary
`2E66557AB97C19C791AF8E20328DA867450F89EC`, but GnuPG reports `EXPKEYSIG`.
This is not a current strong signature or a detached archive signature.
Source policy therefore requires the pinned archive SHA-256, with the index
signature recorded as advisory; no required signature has been weakened.

The original `LICENSE` opens with Miko O'Sullivan's explicit Perl-terms grant
and includes GPL-1.0-or-later / Artistic-1.0 text. The module and POD independently
repeat the author's Perl-terms grant. The original license file is preserved
without altering its additional copyright notices. The archive contains no
bundled third-party implementation.

Frozen discovery snapshot `discovery-20260808T165000Z-9a89920c269462cd` records
Arch extra `perl-number-misc` 1.2-11 and Fedora Everything-source
`perl-Number-Misc` 1.2-29.fc44. These are lineage evidence, not executed recipes.
Current managed packages, all open PR aliases/paths, and complete target
official/supplemental provider indexes were checked for namespace collisions.

## Recipe and verification

The recipe uses upstream's documented MakeMaker route and vendor installation
paths. Core Perl, MakeMaker, Test::More and the existing target RPM Perl macros
supply the build/test dependencies. No CPAN dependency installation is performed.
The unused alternative `Build.PL` does not require adding Module::Build to the
MakeMaker route. The package is `noarch`; no native-kernel or hardware test is
claimed, and no RISC-V source patch is needed.

`%check` runs the complete unchanged `make test` target: the single original
test file contains 31 assertions, including its random-range bounds check.
There are no test exclusions or failure suppression. Host Perl executed all
31 assertions successfully; this is host-language evidence, not an openEuler
RPM build or target installation result. The installed smoke test checks the
module version and representative numeric operations independently.

Local source-only verification and repository gates precede submission. Target
build, original tests, installation, and smoke results must come from the PR's
exact-head CI; physical RPM/SRPM acceptance is still required before merging.
