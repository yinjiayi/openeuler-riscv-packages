<!-- SPDX-License-Identifier: Apache-2.0 -->
# libhtml-entities-numbered-perl

This directory packages upstream `https://metacpan.org/dist/HTML-Entities-Numbered` version `0.04` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The PAUSE-signed fixed CPAN archive matches the Debian stable 0.04-4
original byte for byte. Keep Koichi Taniguchi's original grant and both
full Perl license texts. All 253 entity mappings and their 252-row test
fixture match HTML::Entities data from the pinned HTML-Parser 3.36 archive.
The package carries its separate Gisle Aas notice.

The original tests are unchanged, including the full cross-check of numeric
and named references. The installed smoke checks round-trip conversion and
that the XML mode preserves predefined and unknown entity references.
