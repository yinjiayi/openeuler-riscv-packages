<!-- SPDX-License-Identifier: Apache-2.0 -->
# libfile-util-perl

The frozen Ubuntu `libfile-util-perl` 4.201720-2 source maps to the official
CPAN File-Util 4.201720 release. The full archive SHA-256
`d4491021850d5c5cbd702c7e4744858079841d2fa93f1c2d09ddc9a7863608df`
matches the publisher's `CHECKSUMS`. The archive has a single root and only
regular text source, documentation and test files; no traversal paths,
symlinks or special files were found.

The distribution LICENSE names GPL version 1 or later and Artistic License
1.0 as alternatives. README and the shipped module/documentation POD grant
the same terms as Perl and refer back to LICENSE. No conflicting notice was
found in the shipped source or tests. Both license texts accompany the source;
the binary RPM includes the distribution LICENSE.

The official openEuler 24.03 LTS SP3 `riscv64` RVA23 primary metadata
(SHA-256 `fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
has no `perl-File-Util` or `perl(File::Util)` provider and supplies the used
core modules, Module::Build and Test::NoWarnings. This is a snapshot, not a
guarantee about later repository changes.

The complete unchanged upstream `t/*.t` default suite is retained. Local
macOS lacks Test::NoWarnings, so no local claim is made about the full suite;
exact-head target CI must run it. A source-tree functional smoke passed with a
private File::Temp directory. The installed-RPM smoke checks the same
write/read round-trip in its own cleaned private temporary directory. This
does not establish native RISC-V kernel, performance or publication behavior.
