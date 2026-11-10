<!-- SPDX-License-Identifier: Apache-2.0 -->
# perl-cpan-perl-releases

This directory packages upstream `https://metacpan.org/dist/CPAN-Perl-Releases` version `5.20261022` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The fixed CPAN release is checked against PAUSE-signed CHECKSUMS and the
byte-identical Debian sid orig archive; Fedora Rawhide supplies matching
version lineage. The unmodified upstream LICENSE contains the full GPL
and Artistic terms. The released Makefile and author POD test templates
are attributed to Ricardo SIGNES and contributors from Dist-Zilla 6.040
(SHA-256 `d8d6f304022ec984612e816780336f84d0bc79036ab08621b71b26321db0bc73`).
The generated compile test comes from Jérôme Quelin and contributors,
Dist-Zilla-Plugin-Test-Compile 2.059 (SHA-256
`e1e2212efac068d62bc5e7a8104c4f1aeb97027f58cf37e4a8e589f9ea37eb9b`).
Both donor distributions retain compatible Perl dual grants.

The MakeMaker default suite is unmodified. Its two author-only POD files
self-skip in a normal build; no tests are filtered or disabled by packaging.
The installed smoke checks known tarball mapping and version enumeration.
