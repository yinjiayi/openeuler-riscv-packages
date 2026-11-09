<!-- SPDX-License-Identifier: Apache-2.0 -->
# libhttp-request-ascgi-perl

This directory packages upstream `https://metacpan.org/dist/HTTP-Request-AsCGI` version `1.2` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The fixed CPAN archive matches Debian stable's original source for
`libhttp-request-ascgi-perl` 1.2-4 byte for byte. PAUSE's signed checksum
identifies the archive; its historical signature is checked at signing time.
The unmodified upstream `LICENSE` contains both license texts. The generated
MakeMaker file and two release-only test wrappers match the Dist::Zilla
1.093400 templates, whose separate copyright notice is retained.

The default upstream tests run unchanged, including the fork/descriptor test.
The two release-only POD files skip by upstream default. The installed smoke
constructs a CGI request, checks method/path/query, then restores descriptors
and parses the captured response without a network request.
