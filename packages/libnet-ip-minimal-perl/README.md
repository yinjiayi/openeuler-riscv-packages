<!-- SPDX-License-Identifier: Apache-2.0 -->
# libnet-ip-minimal-perl

The frozen inventory's exact `libnet-ip-minimal-perl` key maps to Ubuntu
source 0.06-2 and official CPAN Net-IP-Minimal 0.06. The tarball SHA-256
`734767e83620eadd80dc466b67102cc55643a2278d20c304b75d401f075fbd13`
matches publisher `CHECKSUMS`; its MD5 also matches Ubuntu's original source
archive. The single-root archive contains no traversal path, link or special
file. The included LICENSE explicitly grants GPL-1-or-later or Artistic terms;
README and module POD repeat that grant and no shipped file contradicts it.

Official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata (SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
contains neither `perl-Net-IP-Minimal` nor `perl(Net::IP::Minimal)`. The module
uses Perl's core Exporter; target MakeMaker and Test::More providers are
available. This is a snapshot check, not a future-repository guarantee.

All four unchanged default upstream `t/*.t` files ran locally: the compile
and functional files passed six assertions; the two release-only POD files
were skipped under upstream's default `RELEASE_TESTING` policy. No test was
removed or disabled. Installed-RPM smoke additionally checks valid and invalid
IPv4/IPv6 strings and version reporting. These are parsing-function checks,
not a native RISC-V or performance claim. Target RPM build, original tests and
installed smoke remain for exact-head CI; PR artifacts do not establish public
repository publication.
