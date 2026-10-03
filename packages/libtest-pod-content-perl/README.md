<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtest-pod-content-perl

The frozen inventory's exact key maps to official stable CPAN
Test::Pod::Content `v0.0.6`. The RPM version omits the upstream Perl
v-string prefix (`0.0.6`); the pinned source filename and archive root
retain it. Official HTTPS source SHA-256
`752bd838c75e113c176e36cb4a5f41b4b34b44bd13d607a92dc7bdf3c903975c`
matches the publisher's `CHECKSUMS`. The tar archive has one root and only
regular files/directories, without traversal, links or special files.

README and module POD grant redistribution/modification under the same
terms as Perl, and Build.PL declares Perl licensing. The RPM uses the
corresponding GPL or Artistic dual-license expression.

Official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata
(SHA-256 `fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
has neither `perl-Test-Pod-Content` nor `perl(Test::Pod::Content)`, but has
Module::Build, Pod::Simple, Test::More and version. This is a point-in-time
repository check, not a guarantee about later content.

Unmodified local upstream `Build test` passed all seven default test files:
four assertions in the functional license and synopsis tests, while five
author tests self-skipped unless `RELEASE_TESTING` is set. The SPEC preserves
those upstream conditions and the entire default test action. Installed-RPM
smoke checks the module provider, Perl v-string version and an installed POD
section. Target RPM build, complete test action and installed smoke require
exact-head CI evidence; PR artifacts alone do not prove public publication.
