<!-- SPDX-License-Identifier: Apache-2.0 -->
# libstring-crc-cksum-perl

The frozen inventory's exact `libstring-crc-cksum-perl` key maps to the
official stable CPAN String::CRC::Cksum 0.91 release. Its HTTPS tarball
SHA-256 `1091aeebaefa9057cbc209e85151833f96e2aace5540e878700974c88a984671`
matches publisher `CHECKSUMS`. The inspected archive has one root and
only regular files and directories, without traversal, links or special
files. Its README and module POD explicitly permit redistribution and
modification under the same terms as Perl itself. This resolves the
frozen `license-blocked` historical marker for this exact release; the
RPM maps that grant to `GPL-1.0-or-later OR Artistic-1.0-Perl` and
installs README as the license notice.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata
(SHA-256 `fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
contains neither `perl-String-CRC-Cksum` nor a
`perl(String::CRC::Cksum)` provider. Its runtime modules are Perl core
only. This snapshot check does not guarantee future repository contents.

Unmodified upstream `make test` ran its only default `t/1.t` file: all
10 assertions passed locally without skips. Assertion 9 conditionally
skips unless `/etc/profile` is readable and `/usr/bin/cksum` exists;
`coreutils` is a target build requirement, but target test coverage is
not presumed before CI logs are reviewed. The test also writes an
isolated temporary file and compares the module against the system
`cksum`, without modifying that system file. A source-level staged
install yielded the module and manual page listed in the SPEC.
Installed-RPM smoke checks version, generated Provides, a fixed CRC
vector and incremental/one-shot agreement. Target RPM build, complete
default test and installed smoke remain for CI to verify; PR artifacts
alone do not prove public repository publication.
