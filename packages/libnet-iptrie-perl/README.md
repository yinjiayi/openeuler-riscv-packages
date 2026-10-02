<!-- SPDX-License-Identifier: Apache-2.0 -->
# libnet-iptrie-perl

The frozen inventory's `libnet-iptrie-perl` key maps to Debian source
0.7-4 and official CPAN Net-IPTrie 0.7. The publisher `CHECKSUMS` SHA-256
is `1ccd1eea53a06d0524efc42fd465dfc5997149d77f87d86f1ccf0e2e05d58e05`.
The single-root archive contains only ordinary files and directories, no
traversal path, links, or special files. README and both Perl module PODs
explicitly grant the same terms as Perl itself. No separate third-party
copyright or contradictory notice appears in the build metadata or test.

Official openEuler 24.03 LTS SP3 RVA23 primary metadata (SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
contains neither `perl-Net-IPTrie` nor `perl(Net::IPTrie)`. It provides
NetAddr::IP 4.79, Module::Build 0.4234, Scalar::Util 1.63,
Class::Struct 0.68, and bigint 0.66, satisfying the source requirements.

The sole unchanged upstream default test passed 28 assertions locally.
It also emitted `Reference is already weak` warnings from upstream
`Net/IPTrie/Node.pm:60`, without test failure. A source-level boundedness
probe inserting and looking up 0, 1, 2, 4, and 8 same-prefix IPv4 hosts
observed 0, 32, 34, 38, and 46 such warnings respectively, no other
warnings and no lookup errors. One IPv6 /32 insertion and lookup emitted
32 of the same warnings. The package retains them; neither tests nor smoke
suppress them. Installed-RPM smoke checks IPv4 and IPv6 closest-prefix
lookup. Target CI must establish RPM build, original test, and installed
smoke results; none of this establishes native RISC-V or performance behavior.

The first PR head built and passed 28 original assertions but DNF installation
failed twice before smoke: RPM auto-Requires detected
`perl(Net::IPTrie::_Node)` from the `use base` in `Node.pm`, while no separate
file supplies an auto-generated Provides. `Class::Struct` actually creates
`Net::IPTrie::_Node` at module load time (`BEGIN` in `Node.pm`), confirmed
by loading the unchanged module and calling its generated constructor.
The SPEC therefore explicitly Provides that exact dynamically created class.
This does not remove the dependency or change the upstream source/tests.
