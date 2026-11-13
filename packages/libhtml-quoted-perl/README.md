<!-- SPDX-License-Identifier: Apache-2.0 -->
# libhtml-quoted-perl

This directory packages upstream `https://metacpan.org/release/BPS/HTML-Quoted-0.05` version `0.05` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

HTML::Quoted extracts nested quotation structure from HTML email. The module
returns the original markup; it is not an HTML sanitizer.

The official CPAN archive matches the authorized release digest and the
PAUSE-signed CHECKSUMS record. Debian stable is discovery lineage only; no
distribution recipe was used. The original source states the Perl terms.
Eight bundled Module::Install 1.06 helpers and the ReadmeFromPod 0.20
helper match their CPAN donor files byte for byte. The package preserves
their attribution, the original README and full pinned license texts.

The original installer is invoked with `-I.` only for its bundled
helpers, without downloading dependencies. The three original default
test files remain untouched (26 assertions, no skips in host validation).
Hosted CI must independently demonstrate target build, tests, install,
smoke and actual RPM/SRPM before acceptance.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
