<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtest-mocktime-perl

The frozen inventory's exact key maps to official stable CPAN
Test::MockTime 0.17. The official HTTPS tarball has SHA-256
`3363e118b2606f1d6abc956f22b0d09109772b7086155fb5c9c7f983350602f9`,
matching the publisher's `CHECKSUMS`. Its archive contains one root and only
regular files and directories, without traversal, links or special files.

README and module POD permit redistribution under the same terms as Perl;
Makefile.PL declares Perl licensing. The RPM uses the corresponding GPL or
Artistic dual-license expression.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata
(SHA-256 `fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
has neither `perl-Test-MockTime` nor `perl(Test::MockTime)`. Its required Perl
module providers and Test::Pod are available. This is a snapshot, not a
guarantee about later repository contents.

The unmodified upstream `make test` passed five files and 34 assertions on
the local host. The package keeps all default tests; the target installs
Test::Pod so the POD check is exercised. Installed-RPM smoke verifies the
module provider, version, fixed time and restoration. Target RPM build,
complete tests and installed smoke require CI evidence. PR artifacts do not
prove public repository publication.
