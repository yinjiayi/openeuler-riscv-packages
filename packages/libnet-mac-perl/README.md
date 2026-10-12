<!-- SPDX-License-Identifier: Apache-2.0 -->
# libnet-mac-perl

The frozen inventory's `libnet-mac-perl` key maps to Debian source
2.103622-3 and official CPAN Net-MAC 2.103622. The publisher `CHECKSUMS`
SHA-256 is `8a27d222b6f675a4f638039e59d3257095d5b90c7c1cb54920659f0bf1fe1f30`.
The single-root tarball contains no traversal path, link, or special file.

Distribution LICENSE, README, and module POD explicitly grant GNU GPL
version 2; the module header separately permits version 2 or later. The
package records the common GPL-2.0-only path, and retains the license text.
The remaining Perl tests and generated MAC-address fixtures are distributed
in this archive under the distribution grant; no separate third-party
rights notice was found. Official SP3 RVA23 primary metadata lacks both
`perl-Net-MAC` and `perl(Net::MAC)` and supplies required Perl core/runtime,
MakeMaker, Test::More, Test::Pod, and Test::Pod::Coverage providers.

All seven unchanged default upstream tests ran locally: 964 assertions
passed and `t/pod-coverage.t` skipped because local Test::Pod::Coverage is
absent. The SPEC requires that target-available module so target CI must
exercise the coverage test; it also requires Test::Pod. Installed smoke
checks address construction, format conversion, and invalid input. Target
RPM build, complete target test outcome, and DNF-installed smoke remain
exact-head CI evidence. These checks do not establish native RISC-V,
performance, or public repository publication.
