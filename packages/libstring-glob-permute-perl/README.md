<!-- SPDX-License-Identifier: Apache-2.0 -->
# libstring-glob-permute-perl

The frozen inventory's exact `libstring-glob-permute-perl` key maps to
official stable CPAN String::Glob::Permute 0.01. The HTTPS release tarball
SHA-256 `1d449fe8156ab13d16d02d8c4ad8757165942e4e221d5952d06d02416cf7ecca`
matches publisher `CHECKSUMS`. The archive has one root and only regular
files and directories, without traversal, links or special files.

The archived `LICENSE.TXT` is the Artistic License dated 15 August 1997.
Module, README and test copyright notices explicitly identify the Perl
Artistic License of that date for the Yahoo-owned material. This resolves
the frozen `license-blocked` historical marker for this exact release;
the RPM declares `Artistic-1.0-Perl` and installs the full license text.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata
(SHA-256 `fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
contains neither `perl-String-Glob-Permute` nor a
`perl(String::Glob::Permute)` provider. Its runtime modules are Perl core
only. This snapshot check does not guarantee future repository contents.

Unmodified upstream `make test` ran the sole default `t/001Basic.t` file:
all 15 assertions passed locally without skips. A source-level staged
installation yielded the module and manual page listed in the SPEC;
source-level smoke verified deterministic brace and bracket expansion.
Installed-RPM smoke checks version, generated Provides, four permutations
and literal handling. Target RPM build, complete default test and installed
smoke remain for CI to verify; PR artifacts alone do not prove public
repository publication.
