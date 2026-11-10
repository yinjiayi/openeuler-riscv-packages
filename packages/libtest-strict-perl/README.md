<!-- SPDX-License-Identifier: Apache-2.0 -->
# perl-test-strict

This directory packages upstream `https://metacpan.org/dist/Test-Strict` version `0.54` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The fixed source SHA-256 matches MetaCPAN metadata and the publisher's
CHECKSUMS. The archive includes the original dual-license notice and full
Artistic-1.0-Perl and GPL-1.0-or-later terms. No patch is applied.

The original default `t/*.t` harness is unchanged. Its ten files produced 85
TAP results in the host preflight, including the original TODO for matching
`use strict` inside a print string. The optional coverage and version files
self-skipped without `cover` and `Test::Version` respectively; POD, POD
coverage, manifest and change tests ran. The installed smoke checks syntax,
strict and warnings handling on a temporary Perl fixture.
