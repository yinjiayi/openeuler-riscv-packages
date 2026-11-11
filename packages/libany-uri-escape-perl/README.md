<!-- SPDX-License-Identifier: Apache-2.0 -->
# Any::URI::Escape

This directory packages [Any::URI::Escape 0.01](https://metacpan.org/dist/Any-URI-Escape) for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. Ubuntu's `libany-uri-escape-perl` is the discovery lineage. The fixed upstream CPAN archive matches the PAUSE publisher's signed CHECKSUMS and the release SHA-256. Its README and module preserve Fred Moyer's Perl-terms grant; both complete license texts are pinned separately.

The package adds no patch. The default `t/Any-URI-Escape.t` suite runs all four original assertions, including both directions of URI conversion. The installed smoke independently checks percent encoding and round-trip decoding. The existing target `perl-URI` provides the original pure-Perl fallback. The upstream optional XS selection is unchanged; no XS provider, performance, or native validation is claimed.
