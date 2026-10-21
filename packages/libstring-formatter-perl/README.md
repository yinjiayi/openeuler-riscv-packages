<!-- SPDX-License-Identifier: Apache-2.0 -->
# libstring-formatter-perl

The frozen inventory's exact `libstring-formatter-perl` key maps to Ubuntu
and official CPAN source version 1.235. The official HTTPS tarball SHA-256
`08236a913b911ce652cf08598e7c07d2df3f369fc47bf401a485a504a1660783`
matches the publisher's `CHECKSUMS`. The inspected archive has one root and
only regular files and directories, with no traversal, links or special
files. Included LICENSE, README and both module POD files grant GNU GPL
version 2 only, consistent with the release's `GPL-2.0-only` metadata.
`dist.ini` records that this licensing was inherited from co-author Darren
Chamberlain. The RPM installs the full LICENSE file.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata
(SHA-256 `fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
has neither `perl-String-Formatter` nor a `perl(String::Formatter)` provider.
It supplies the upstream runtime dependencies Params::Util 1.07 (riscv64)
and Sub::Exporter 0.990. This snapshot check is not a guarantee about
future repository contents.

All six unmodified default upstream `t/*.t` files ran locally: 22 tests
passed. They cover direct formatting, imported formatter functions,
parameter styles, conversion errors and configuration. Two `xt/`
author/release files are outside upstream's default `make test` target and
are not counted as passed. A source-level staged install yielded both modules
and both manual pages, all enumerated in the SPEC. Installed-RPM smoke loads
both modules, checks a formatting result and rejects an unknown conversion.
Target RPM build, full default suite and installed smoke remain for CI to
verify; successful PR artifacts alone do not prove public publication.
