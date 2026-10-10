<!-- SPDX-License-Identifier: Apache-2.0 -->
# libnet-dhcpv6-duid-parser-perl

The frozen inventory's exact `libnet-dhcpv6-duid-parser-perl` key maps to
Debian source 1.01-4 and official CPAN Net-DHCPv6-DUID-Parser 1.01. The
publisher `CHECKSUMS` SHA-256 is
`913a98ca32f05a0ee3ba84d11dc8f6da81f3bfa53e0d77257a256a8f62c515e6`.
The single-root archive contains only regular files and directories, no
traversal path, link, or special file.

Upstream `META.yml` says `license: unknown`; that metadata limitation is
retained here rather than silently treated as an SPDX grant. The author's
README contains the full two-clause source/binary redistribution conditions,
disclaimer, and additional views-and-conclusions sentence. The same full
notice appears at the start of `Parser.pm`. This text matches the official
[SPDX BSD-2-Clause-Views](https://spdx.org/licenses/BSD-2-Clause-Views.html)
identifier, including its views sentence. The only test is 46 static DUID
assertions with no separate notice or third-party fixture; build metadata
and other archive files likewise have no conflicting notice. The RPM retains
the complete README as license material.

Official openEuler 24.03 LTS SP3 RVA23 primary metadata (SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
has neither `perl-Net-DHCPv6-DUID-Parser` nor
`perl(Net::DHCPv6::DUID::Parser)`. The module imports only Perl core Carp;
the target also provides MakeMaker and Test::More.

The sole unchanged upstream default test passed all 46 assertions locally,
without network or filesystem mutation. Installed-RPM smoke checks DUID-LLT,
DUID-EN, DUID-LL, and malformed input. Exact-head target RPM build/test and
installed smoke remain CI evidence, not native RISC-V or public repository
publication evidence.
