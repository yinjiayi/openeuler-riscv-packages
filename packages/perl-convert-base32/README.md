<!-- SPDX-License-Identifier: Apache-2.0 -->
# perl-convert-base32

This directory packages upstream `https://metacpan.org/dist/Convert-Base32` version `0.06` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

## Source, license, and admission

The fixed official CPAN archive `Convert-Base32-0.06.tar.gz` has SHA-256
`4ba82c167c41f455aa8284738727e4c94a2ebcb1c4ce797f6fda07245a642115`, matching
MetaCPAN and publisher CHECKSUMS. README and `lib/Convert/Base32.pm` explicitly
grant Perl's dual-license terms; those grants resolve META.yml's older
`unknown` field and are retained with `%license`. No vendor code is bundled.

No bundled SIGNATURE or detached archive signature was identified. The
historical signed CHECKSUMS verifies to official PAUSE primary fingerprint
`2E66557AB97C19C791AF8E20328DA867450F89EC` with an expired historical subkey
and SHA-1 caveat. It is advisory signed-index evidence, not a current detached
archive signature; exact archive SHA-256 remains mandatory.

Ubuntu resolute `libconvert-base32-perl` 0.06-3 provides distribution lineage.
Normalized component aliases were checked against current canonical packages,
all open PR files and target provider/file indexes. Official target packages
supply the build dependencies, including Test::Exception 0.43 and its
Sub::Uplevel dependency. Upstream Makefile.PL treats Test::Exception and
Test::More as build requirements with modern ExtUtils::MakeMaker; they are
not runtime requirements of the module itself. No distribution recipe ran.

## Generic correctness patch and tests

Upstream 0.06's large-input encoding paths map only complete five-bit groups.
For inputs of at least 1024 bytes whose length is not divisible by five, the
final partial group remains literal `0`/`1` characters, yielding invalid output.
Patch 0001 changes both paths to map one-to-five-bit groups using the existing
zero-padding table, exactly as the small-input path does. This is a generic
correctness fix, not RISC-V-specific. The official Debian 0.06-3 packaging
archive contains no patch for this issue; no upstream write was performed.

The complete original default suite remains intact (1072 assertions). The
patch adds 32 assertions to default `make test`, covering both encoders, both
decoders, alphabet and encoded length at 1023/1024/1025/1026 bytes. Before the
patch, 1024/1026-byte results disagree with independent Python standard-library
Base32 output; after it, both encoder paths match all boundary vectors and
the full 1104-assertion suite passes on the host. Remove the patch once an
official stable release incorporates equivalent correct tail-bit handling
and passes these regressions.

The patch uses balanced three-line unified-diff context and is verified with
GNU patch `--fuzz=0`, matching RPM `%autosetup`. The initial PR's asymmetric
context was accepted by the host's Apple patch but rejected in target `%prep`;
regenerating context leaves both the patched module and added test unchanged.

Installed smoke checks known vectors, uppercase decoding, malformed input,
and the large-input boundaries. Host/source-only checks do not establish
target RPM success. Exact-head target build and installed smoke remain CI
gates; no native performance, merge, or public-publication claim is made.
