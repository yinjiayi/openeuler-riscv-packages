<!-- SPDX-License-Identifier: Apache-2.0 -->
# libfile-monitor-perl

The frozen Ubuntu `libfile-monitor-perl` 1.00-3 source maps to the official
CPAN File-Monitor 1.00 release. Its full archive SHA-256
`32e3df1cef2ba4932c3e0e6f7baedb01d3dd472aebc238cdadbd6635414ffaef`
matches the publisher's `CHECKSUMS`. The archive has one root, regular text
files and directories only, and no traversal path or symlink.

README and every shipped File::Monitor module POD grant the same terms as
Perl itself. The auxiliary source, build helper and examples carry no
contradictory grant. The RPM uses the standard Perl GPL-1.0-or-later or
Artistic-1.0-Perl choice. No third-party binary fixtures are bundled.

The official openEuler 24.03 LTS SP3 `riscv64` RVA23 primary metadata
(SHA-256 `fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
has no same-name RPM or `perl(File::Monitor)` provider. It supplies the used
core modules and the POD test dependencies. This is snapshot evidence only.

All eight unchanged default upstream test files are retained. Local tests
passed 930 assertions; `t/pod-coverage.t` skipped because local macOS lacks
Test::Pod::Coverage. The target SPEC declares that provider, so exact-head
target CI must exercise the complete suite. Three tests create and delete
`fmtest-$$` trees below File::Spec's temporary directory; `%check` confines
`TMPDIR` to a fresh private build directory before running any test.

The installed-RPM smoke watches a file in its own cleaned private tempdir,
checks a baseline scan, then checks detection after changing file size. This
is functional evidence under hosted QEMU user mode; it does not validate
native RISC-V kernel metadata, timing, performance or public publication.
