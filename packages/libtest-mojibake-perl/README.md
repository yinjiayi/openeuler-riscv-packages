<!-- SPDX-License-Identifier: Apache-2.0 -->
# perl-test-mojibake

This directory packages upstream `https://metacpan.org/dist/Test-Mojibake` version `1.3` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The upstream LICENSE includes both complete alternative terms:
Artistic-1.0-Perl or GPL-1.0-or-later. The fixed source SHA-256 agrees with
MetaCPAN release metadata and publisher CHECKSUMS. No patch is applied.

The original default `t/*.t` suite remains unchanged (31 files; 55 executed
assertions and no assertion skips in the host preflight). Ten author-only and
seven release-only files self-skip under the upstream default. The installed
smoke invokes the packaged `scan_mojibake` CLI on a valid Perl file and checks
its TAP result.
